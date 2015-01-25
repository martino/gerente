from collections import defaultdict
import json
import operator
from random import sample
from clasificador.models import ClassifierModel
from clasificador.serializers import ClassifierModelSerializer
from documentos.models import Frame
from datetime import datetime


def split_document(text, use_paragraph=True):

    headers_split = text.split('\t\t\n\t\t\n')
    if len(headers_split) == 2:
        text = headers_split[1]

    return text.split('.\n')


def get_gs_node_labels(gs):
    return [super_node.name for super_node in gs.supernode_set.all()]


def get_sample(gs, random=False):
    grouped_class = [(super_node.name, super_node.node_set.all())
                     for super_node in gs.supernode_set.all()]

    grouped_frames = [
        (
            Frame.objects.filter(node__in=node[1]),
            node[0]
        )
        for node in grouped_class
    ]

    smallest_group = min([group[0].count() for group in grouped_frames])
    sample_size = int((smallest_group/3)*2)
    sample_frames = []
    for frame_group in grouped_frames:
        if random:
            pk_list = frame_group[0].values_list('pk', flat=True)
            sample_size = int(len(pk_list)/2)
            selected_pks = sample(pk_list, sample_size)
            print 'sample size for {} {}'.format(frame_group[1], sample_size)
            selected_frames = Frame.objects.filter(pk__in=selected_pks)
            sample_frames.append((selected_frames, frame_group[1]))
        else:

            sample_frames.append((frame_group[0][:sample_size], frame_group[1]))
    return sample_frames


def normalize_weight(topics):
    max_value = topics[0][1]
    normalized_topic = [[k, max((v * 10) / max_value, 1)]
                        for (k, v) in topics if v > 0]
    return normalized_topic


def normalize_topics_with_freq(topics, topic_len):
    from math import log
    topics_count = float(len(topics.keys()))
    tmp_topics = {}
    return_topic = {}
    for tname, topic in topics.iteritems():
        tmp_topics[tname] = {}
        for entity, count in topic.iteritems():
            entity_repetition = len(
                [True for name, topic in topics.iteritems() if entity in topic])

            new_score = count * log(topics_count / entity_repetition)
            # print "{} {} {} {}".format(
            #     tname, entity, count, entity_repetition, new_score)
            tmp_topics[tname][entity] = new_score

    for name, new_topic in tmp_topics.iteritems():
        ordered_topic = sorted(
            new_topic.items(), key=operator.itemgetter(1), reverse=True)
        topic_to_take = topic_len
        return_topic[name] = normalize_weight(ordered_topic[:topic_to_take])

    return return_topic


def create_new_model(gs, description='', topic_limit=20, random_sample=True):
    # create a new model
    model_data = {
        "description": description,
        "lang": "it"
    }
    new_model = ClassifierModel()
    new_model.name = "AutoGen Model {}".format(datetime.now().isoformat())
    new_model.json_model = json.dumps(model_data)
    new_model.goal_standard = gs
    new_model.save()

    # generate a new sample set
    sample_set = get_sample(gs, random_sample)

    # extract topic list
    topics = {}
    for frame_group in sample_set:
        cluster = defaultdict(int)
        for frame in frame_group[0]:
            new_model.generation_frames.add(frame)
            entities = json.loads(frame.annotations)
            for entity in entities:
                url = entity.get('uri', '')
                cluster[url] += 1
        topics[frame_group[1]] = cluster
    new_model.save()

    # adjust topic list with
    final_topics = normalize_topics_with_freq(topics, topic_limit)

    categories = []
    for name, topic in final_topics.iteritems():
        categories.append({
            'name': name,
            'topics': {t[0]: t[1] for t in topic}
        })

    model_data['categories'] = categories
    serializer = ClassifierModelSerializer()
    serializer.update(
        new_model, {'json_model': json.dumps(model_data)}, init_dt=True)



