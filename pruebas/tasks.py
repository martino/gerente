from __future__ import absolute_import
from collections import defaultdict

import grequests
import json

from celery import shared_task
from django.conf import settings
from documentos.helpers import split_document

from documentos.models import BaseDocument, Frame
from gerente.datatxt_helpers import Datatxt
from pruebas.helpers import compute_confusion_matrix
from pruebas.models import BaseTestResult, DocumentAnnotation, FrameAnnotation, \
    DocumentTestResult


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
    for part in split_document(doc.original_text):
        reqs.append(dt.classify(model_id, part, True))

    for res in grequests.map(reqs):
        res_json = res.json()
        res_topics = res_json.get('categories', {})
        if len(res_topics):
            best_obj = sorted(
                res_topics, key=lambda x: x.get('score', 0), reverse=True)[0]
            if best_obj.get('score', 0) >= threshold:
                #TODO introduce weigth based on frame length
                all_results[best_obj.get('name')] += best_obj.get('score')
    return all_results


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
def test_document_set(model, document_group, threshold=0.32):
    print 'Testing {}'.format(document_group)
    docs = document_group.basedocument_set.all()
    dt = Datatxt()
    #create a new classifier on datatxt
    dt = Datatxt()
    req = dt.create_model(model.json_model)
    res = req.json()
    datatxt_id = res.get('id')

    test_result = DocumentTestResult.objects.create(
        json_model=model.json_model,
        model_version=model,
        document_group=document_group
    )
    global_results = defaultdict(int)
    all_done = True
    try:
        all_count = docs.count()
        count = 1
        for doc in docs:
            print "{}/{}".format(count, all_count)
            count += 1
            res = analyze_doc(doc, datatxt_id, dt, threshold)
            for key, value in res.iteritems():
                global_results[key] += 1

            # create a document Annotation
            DocumentAnnotation.objects.create(
                test_results=json.dumps(res),
                document=doc,
                test_running=test_result
            )
    except Exception, e:
        print "huston we have a problem"
        print e
        [doc_a.delete() for doc_a in test_result.documentannotation_set.all()]
        test_result.delete()
        all_done = False
    finally:
        #delete model
        dt.delete_model(datatxt_id)
        document_group.testing_task_id = None
        document_group.save()
        if all_done:
            test_result.scoring_result = json.dumps(global_results)
            test_result.save()
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

    frame_nodes_pk_list = set(model.generation_frames.all()
                              .values_list('node__pk', flat=True))

    frame_to_analyze = Frame.objects.filter(node__pk__in=frame_nodes_pk_list)\
        .exclude(pk__in=generator_frames)

    current_gs = model.goal_standard

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
            current_class = frame.node.super_node\
                .get(goal_standard=current_gs).name
            found_class, raw_res = analyze_frame(
                frame, datatxt_id, dt, threshold)
            print 'frame: {} compute score: {} - {}'.format(
                frame.pk, current_class, found_class)
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
        confusion_matrix = compute_confusion_matrix(test_result, current_gs)
        test_result.confusion_matrix = json.dumps(confusion_matrix)
        test_result.save()
    except Exception, e:
        print 'Huston we have a problem!'
        print e
        [frame_a.delete() for frame_a in test_result.frameannotation_set.all()]
        test_result.delete()
    finally:
        dt.delete_model(datatxt_id)
        model.testing_task_id = None
        model.save()

    return 0
