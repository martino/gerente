from rest_framework import serializers
import json
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
            'document_count': related_documents.count(),
            'scoring_result': enriched_scoring_result,
            'running_date': instance.created,
        }


class DocumentAnnotationSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'raw_results': instance.raw_result
        }
