from rest_framework import serializers


class DocumentGroupSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        tests_results = instance.documenttestresult_set.all()\
            .order_by('-created')
        last_scoring = None
        if tests_results.count():
            last_scoring = tests_results[0].scoring_result
        return {
            'name': instance.name,
            'documents_ids': instance.basedocument_set.all().values_list(
                'pk', flat=True),
            'last_scoring': last_scoring,
            'testing_task_id': instance.testing_task_id,
        }
