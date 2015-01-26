from rest_framework import serializers
from rest_framework.exceptions import APIException
from clasificador.models import ClassifierModel
from gerente.datatxt_helpers import Datatxt

import json
from pruebas.models import BaseTestResult


class DataTXTErrors(APIException):
    status_code = 504
    default_detail = 'DataTXT error.'


class ClassifierModelSerializer(serializers.BaseSerializer):
    @staticmethod
    def update_on_datatxt(model_id, model):
        dt = Datatxt()
        req = dt.update_model(model_id, model)
        if req.status_code != 200:
            print req.content
            raise DataTXTErrors()

    @staticmethod
    def create_on_datatxt(model):
        dt = Datatxt()
        req = dt.create_model(model)
        if req.status_code == 200:
            res = req.json()
            return res.get('id')
        raise DataTXTErrors()

    def to_internal_value(self, data):
        model = data.get('data')
        name = data.get('name')
        return {
            'json_model': model,
            'name': name,
        }

    def to_representation(self, instance):
        tests = BaseTestResult.objects.filter(model_version=instance)\
            .order_by('-created')
        last_test = {}
        len_tests = len(tests)
        if len_tests:
            i = 0
            while tests[i].macro_f1 is None and i <= len_tests:
                i += 1
            if i < len_tests:
                test = tests[i]

                last_test = {
                    'f1': '{0:.2f}'.format(test.macro_f1),
                    'precision': '{0:.2f}'.format(test.macro_precision),
                    'recall': '{0:.2f}'.format(test.macro_recall),
                }
        return {
            'id': instance.datatxt_id,
            'name': instance.name,
            'data': instance.json_model,
            'testing_task': instance.testing_task_id,
            'last_test': last_test,
        }

    def create(self, validated_data):
        datatxt_id = self.create_on_datatxt(validated_data.get('json_model'))
        validated_data['datatxt_id'] = datatxt_id
        return ClassifierModel.objects.create(**validated_data)

    def update(self, instance, validated_data, init_dt=False):
        new_data = validated_data.get('json_model')
        if init_dt:
            datatxt_id = self.create_on_datatxt(new_data)
            instance.datatxt_id = datatxt_id
        else:
            self.update_on_datatxt(
                instance.datatxt_id, new_data
            )
        instance.json_model = json.loads(new_data)
        if validated_data.get('name') is not None:
            instance.name = validated_data.get('name')
        instance.save()
        return instance
