from rest_framework import serializers


class DocumentGroupSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        documents_count = instance.basedocument_set.all().count()
        tests_results = instance.documenttestresult_set.all()\
            .order_by('-created')
        last_test = None
        if tests_results.count():
            last_test = tests_results[0].pk
        document_list = instance.basedocument_set.all().values(
            'id', 'file_name')
        return {
            'id': instance.pk,
            'name': instance.name,
            'documents_count': documents_count,
            'document_list': document_list,
            'last_test': last_test,
            'testing_task_id': instance.testing_task_id,
        }


class BaseDocumentSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        serialization = {
            'name': instance.file_name,
            'text': instance.original_text,
        }

        if instance.group is not None:
            serialization['group'] = {
                'id': instance.group.pk,
                'name': instance.group.name,
            }

        return serialization
