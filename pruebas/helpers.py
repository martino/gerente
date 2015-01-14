from documentos.models import Node


def compute_confusion_matrix(test_results):
    all_nodes_names = list(Node.objects.all().values_list(
        'alternative_names', flat=True))
    all_nodes_names.append('empty')

    confusion_matrix = {
        label: {} for label in all_nodes_names
    }

    for fa in test_results.frameannotation_set.all():
        score = fa.raw_scoring
        current_entry = confusion_matrix[fa.frame.node.alternative_names]
        if score == '':
            score = 'empty'
        if score not in current_entry:
            current_entry[score] = {'count': 0, 'pks': []}
        current_entry[score]['count'] += 1
        current_entry[score]['pks'].append(fa.frame.pk)

    return confusion_matrix

