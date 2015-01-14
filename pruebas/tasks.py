from __future__ import absolute_import
from collections import defaultdict

import grequests
import json

from celery import shared_task
from django.conf import settings

from documentos.models import BaseDocument, Frame
from gerente.datatxt_helpers import Datatxt
from pruebas.helpers import compute_confusion_matrix
from pruebas.models import BaseTestResult, DocumentAnnotation, FrameAnnotation


def compute_class_mapping():
    mappings = defaultdict(list)

    for mapping in settings.MODEL_MAPPINGS:
        for topic, sn in mapping.iteritems():
            if topic not in mappings[sn]:
                mappings[sn].append(topic)
    mappings['developemental state'] = 'developmental state'
    return mappings


def score_result(right_class, founded_class):
    classes_count = 8
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    if right_class == founded_class:
        tp = 1
    elif founded_class == '':
        fn = 1
    else:
        fp = 1

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


def score_result_complex(gs, res, mappings):
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


# def analyze_frames(frames, model_id, dt, threshold=0.3):


def analyze_frame(frame, model_id, dt, threshold=0.3):
    res = dt.classify(model_id, frame.text)
    res_topics = res.json().get('categories', {})
    result = ''
    if len(res_topics):
        best_obj = sorted(
            res_topics, key=lambda x: x.get('score', 0), reverse=True)[0]
        if best_obj.get('score', 0) >= threshold:
            result = best_obj.get('name')
        else:
            print best_obj.get('score', 0)
    return result, res.json()


def analyze_doc(doc, model_id, dt, threshold=0.25):
    all_results = defaultdict(int)
    reqs = []
    #TODO parallelize this
    for part in doc.documentpart_set.all():
        reqs.append(dt.classify(model_id, part.text, True))

    raw_responses = []
    for res in grequests.map(reqs):
        res_json = res.json()
        raw_responses.append(res_json)
        res_topics = res_json.get('categories', {})
        if len(res_topics):
            best_obj = sorted(
                res_topics, key=lambda x: x.get('score', 0), reverse=True)[0]
            if best_obj.get('score', 0) >= threshold:
                #TODO introduce weigth based on frame length
                all_results[best_obj.get('name')] += best_obj.get('score')

    return all_results, raw_responses


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
def test_model_with_docs(datatxt_id, model, threshold=0.32):
    print 'Testing {}'.format(datatxt_id)
    docs = BaseDocument.objects.all()
    dt = Datatxt()
    classes_mapping = compute_class_mapping()

    test_result = BaseTestResult()
    test_result.json_model = model.json_model
    test_result.model_version = model
    test_result.save()

    try:
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

            score = score_result_complex(
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
    except:
        [doc_a.delete() for doc_a in test_result.documentannotation_set.all()]
        test_result.delete()
    finally:
        #delete model
        dt.delete_model(datatxt_id)
        model.testing_task_id = None
        model.save()

    return 0


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


@shared_task
def test_model(datatxt_id, model, threshold=0):
    # get frame to test
    generator_frames = model.generation_frames.all()\
        .values_list('pk', flat=True)

    frame_to_analyze = Frame.objects.exclude(pk__in=generator_frames)
    # grouped_frames = chunks(frame_to_analyze, 50)
    dt = Datatxt()
    test_result = BaseTestResult()
    test_result.json_model = model.json_model
    test_result.model_version = model
    test_result.save()

    # tests all frames
    try:
        all_scores = []
        all_count = frame_to_analyze.count()
        count = 1
        # TODO split into blocks of 10 elements and paralellize
        for frame in frame_to_analyze:
            print "{}/{}".format(count, all_count)
            count += 1
            current_class = frame.node.alternative_names
            found_class, raw_res = analyze_frame(frame, datatxt_id, dt, threshold)
            print 'frame: {} compute score: {} - {}'.format(frame.pk, current_class, found_class)
            score = score_result(current_class, found_class)
            all_scores.append(score)
            # score this annotation
            FrameAnnotation.objects.create(
                test_results=json.dumps(score),
                raw_scoring=found_class,
                raw_result=json.dumps(raw_res),
                frame=frame,
                test_running=test_result
            )
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
        confusion_matrix = compute_confusion_matrix(test_result)
        test_result.confusion_matrix = confusion_matrix
        test_result.save()
    except Exception, e:
        print e
        [frame_a.delete() for frame_a in test_result.frameannotation_set.all()]
        test_result.delete()
    finally:
        dt.delete_model(datatxt_id)
        model.testing_task_id = None
        model.save()

    return 0
