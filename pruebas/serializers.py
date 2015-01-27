from rest_framework import serializers
import json


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
        return {
            'id': instance.pk,
            'document_count': related_documents.count(),
            'scoring_result': instance.scoring_result,
            'running_date': instance.created,
        }


class DocumentAnnotationSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'raw_results': instance.raw_result
        }
