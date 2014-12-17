from rest_framework import serializers
import json


class BaseTestResultSerializer(serializers.ModelSerializer):
    datatxt_id = serializers.StringRelatedField(many=True)

    def to_representation(self, instance):
        return {
            'results': instance.get_result(),
            'json': json.loads(instance.json_model),
            'date': instance.created,
            'id': instance.pk,
        }
