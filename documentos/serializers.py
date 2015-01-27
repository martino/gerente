from rest_framework import serializers


class DocumentGroupSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        documents_count = instance.basedocument_set.all().count()
        tests_results = instance.documenttestresult_set.all()\
            .order_by('-created')
        last_test = None
        if tests_results.count():
            last_test = tests_results[0].pk

        return {
            'id': instance.pk,
            'name': instance.name,
            'documents_count': documents_count,
            'last_test': last_test,
            'testing_task_id': instance.testing_task_id,
        }
