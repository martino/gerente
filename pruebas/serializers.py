from rest_framework import serializers
from documentos.models import BaseDocument


class BaseTestResultSerializer(serializers.ModelSerializer):
    datatxt_id = serializers.StringRelatedField(many=True)

    def to_representation(self, instance):
        return {
            'results': instance.get_result(),
            'json': instance.json_model,
            'date': instance.created,
            'id': instance.pk,
        }


class DocumentTestResultSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        related_documents = instance.document_group.basedocument_set.all()
        enriched_scoring_result = {
            key: BaseDocument.objects.filter(pk__in=values).values(
                'id', 'file_name')
            for key, values in instance.scoring_result.iteritems()
        }

        return {
            'id': instance.pk,
            'scoring_result': enriched_scoring_result,
            'running_date': instance.created,
            'classifier_model': {
                'id': instance.model_version.datatxt_id,
                'name': instance.model_version.name
            },
            'document_group': {
                'id': instance.document_group.pk,
                'document_count': related_documents.count(),
                'name': instance.document_group.name
            }
        }


class DocumentTestResultSmallSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'running_date': instance.created,
            'classifier_model': {
                'id': instance.model_version.datatxt_id,
                'name': instance.model_version.name
            },
            'document_group': {
                'id': instance.document_group.pk,
                'name': instance.document_group.name
            }
        }


class DocumentAnnotationSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):

        document = instance.document
        doc_serialized = {
            'id': document.pk,
            'name': document.file_name,
        }

        if document.group is not None:
            doc_serialized['group'] = {
                'id': document.group.pk,
                'name': document.group.name,
            }

        try:
            threshold = instance.raw_result[0].get('threshold', None)
        except IndexError:
            threshold = None

        return {
            'id': instance.pk,
            'document': doc_serialized,
            'test': {
                'id': instance.test_running.pk,
                'created': instance.test_running.created,
                'model_id': instance.test_running.model_version.datatxt_id
            },
            'threshold': threshold,
            'raw_results': instance.raw_result
        }
