import json
from collections import defaultdict
from documentos.helpers import get_gs_node_labels


def compute_most_popular_entities(raw_score):
    categories = json.loads(raw_score).get('categories')
    if len(categories) == 0:
        return []
    selected_topic = sorted(
        categories, key=lambda x: x.get('score', 0), reverse=True)[0]
    score_details = sorted(
        selected_topic.get('scoreDetails'),
        key=lambda x: x.get('weight', 0),
        reverse=True)
    return [score_details[0]]


def compute_confusion_matrix(test_results, gs):
    all_nodes_names = get_gs_node_labels(gs)
    all_nodes_names.append('empty')

    confusion_matrix = {
        label: {} for label in all_nodes_names
    }

    for fa in test_results.frameannotation_set.all():
        score = fa.raw_scoring
        current_entry = confusion_matrix[
            fa.frame.node.super_node.get(goal_standard=gs).name]
        try:
            decisive_topics = compute_most_popular_entities(fa.raw_result)[0]
        except IndexError:
            decisive_topics = {}

        if score == '':
            score = 'empty'
        if score not in current_entry:
            current_entry[score] = {
                'count': 0, 'pks': [], 'entities': defaultdict(int)
            }
        current_entry[score]['count'] += 1
        current_entry[score]['pks'].append(fa.frame.pk)

        current_entry[score]['entities'][decisive_topics.get('entity')] += 1
    return confusion_matrix

