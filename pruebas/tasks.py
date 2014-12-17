from __future__ import absolute_import
from collections import defaultdict
from django.db import transaction

import grequests
import json

from celery import shared_task
from django.conf import settings

from documentos.models import BaseDocument
from gerente.datatxt_helpers import DatatxtCL
from pruebas.models import BaseTestResult, DocumentAnnotation


def compute_class_mapping():
    mappings = defaultdict(list)

    for mapping in settings.MODEL_MAPPINGS:
        for topic, sn in mapping.iteritems():
            if topic not in mappings[sn]:
                mappings[sn].append(topic)
    mappings['developemental state'] = 'developmental state'
    return mappings


def score_result(gs, res, mappings):
    right_values = gs.keys()
    founded_values = [mappings.get(val) for val in res.keys()]

    right_match = [
        True
        for val in founded_values
        if len(set(val).intersection(set(right_values)))
    ]
    tp = len(right_match)
    tn = 8 - len(founded_values)
    fp = len(founded_values) - tp
    fn = len(right_values) - tp
    #print "tp {} fp {} tn {} right_values {}".format(tp, fp, tn, len(right_values))
    try:
        precision = tp/float(tp + fp)
    except ZeroDivisionError:
        precision = 1

    try:
        recall = tp/float(tp + fn)
    except ZeroDivisionError:
        recall = 1

    accuracy = (tp + tn)/float(tp + tn + fp + fn)

    fscore = (2 * tp)/float(2 * tp + fp + fn)

    return {
        'tp': tp,
        'tn': tn,
        'fp': fp,
        'fn': fn,
        'precision': precision,
        'recall': recall,
        'accuracy': accuracy,
        'fscore': fscore
    }


def analyze_doc(doc, model_id, dt, threshold=0.3):
    all_results = defaultdict(int)
    reqs = []
    #TODO parallelize this
    for part in doc.documentpart_set.all():
        reqs.append(dt.classify(model_id, part.text, True))

    for res in grequests.map(reqs):
        res_topics = res.json().get('categories', {})
        if len(res_topics):
            best_obj = sorted(
                res_topics, key=lambda x: x.get('score', 0), reverse=True)[0]
            if best_obj.get('score', 0) >= threshold:
                #TODO introduce weigth based on frame length
                all_results[best_obj.get('name')] += best_obj.get('score')
    return all_results, res.json()


def compute_micro(scores):
    tmp = {
        'tp': [],
        'fp': [],
        'fn': []
    }
    for score in scores:
        tmp['tp'].append(score.get('tp'))
        tmp['fp'].append(score.get('fp'))
        tmp['fn'].append(score.get('fn'))

    recall = sum(tmp['tp'])/float(sum(tmp['tp']) + sum(tmp['fp']))
    precision = sum(tmp['tp'])/float(sum(tmp['tp']) + sum(tmp['fn']))
    fscore = 2 / (1 / recall + 1 / precision)
    ret_val = {
        'recall': recall,
        'precision': precision,
        'fscore': fscore
    }
    return ret_val


def compute_macro(scores):
    tmp = {
        'recall': [],
        'precision': []
    }
    for score in scores:
        tmp['recall'].append(score.get('recall'))
        tmp['precision'].append(score.get('precision'))

    recall = sum(tmp['recall'])/float(len(tmp['recall']))
    precision = sum(tmp['precision'])/float(len(tmp['precision']))
    fscore = 2 / (1 / recall + 1 / precision)
    ret_val = {
        'recall': recall,
        'precision': precision,
        'fscore': fscore
    }
    return ret_val


@shared_task
def test_model(datatxt_id, model, threshold=0.32):
    print 'Testing {}'.format(datatxt_id)
    docs = BaseDocument.objects.all()
    dt = DatatxtCL()
    classes_mapping = compute_class_mapping()
    try:
        with transaction.atomic():
            test_result = BaseTestResult()
            test_result.json_model = model.json_model
            test_result.model_version = model
            test_result.save()
            all_scores = []
            all_count = docs.count()
            count = 1
            for doc in docs:
                print "{}/{}".format(count, all_count)
                count += 1
                current_gs = json.loads(doc.goal_standard)
                if current_gs == {}:
                    continue

                res, raw_res = analyze_doc(doc, datatxt_id, dt, threshold)
                score = score_result(
                    current_gs, res, classes_mapping
                )

                all_scores.append(score)
                # create a document Annotation
                doc_ann = DocumentAnnotation()
                doc_ann.test_results = json.dumps(score)
                doc_ann.document = doc
                doc_ann.test_running = test_result
                doc_ann.raw_result = json.dumps(raw_res)
                doc_ann.save()

            #compute mico/macro precision
            micro = compute_micro(all_scores)
            test_result.micro_f1 = micro.get('fscore')
            test_result.micro_precision = micro.get('precision')
            test_result.micro_recall = micro.get('recall')
            macro = compute_macro(all_scores)
            test_result.macro_f1 = macro.get('fscore')
            test_result.macro_precision = macro.get('precision')
            test_result.macro_recall = macro.get('recall')
            test_result.save()
    finally:
        #delete model
        dt.delete_model(datatxt_id)
        model.testing_task_id = None
        model.save()

    return 0