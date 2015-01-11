from collections import defaultdict
import json
import operator
from clasificador.models import ClassifierModel
from clasificador.serializers import ClassifierModelSerializer
from documentos.models import Node, Frame
from datetime import datetime


def get_sample():
    flat_values = set(
        Node.objects.all().values_list('alternative_names', flat=True))

    grouped_class = [
        Node.objects.filter(alternative_names=a_name)
        for a_name in flat_values
    ]

    grouped_frames = [
        (
            Frame.objects.filter(node__in=node),
            node[0].alternative_names
        )
        for node in grouped_class
    ]

    smallest_group = min([group[0].count() for group in grouped_frames])
    sample_size = int((smallest_group/3)*2)
    print "sample size: {}".format(sample_size)
    sample_frames = []
    for frame_group in grouped_frames:
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


def create_new_model(description='', topic_limit=20):
    # create a new model
    model_data = {
        "description": description,
        "lang": "it"
    }
    new_model = ClassifierModel()
    new_model.name = "AutoGen Model {}".format(datetime.now().isoformat())
    new_model.json_model = json.dumps(model_data)
    new_model.save()

    # generate a new sample set
    sample_set = get_sample()

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



