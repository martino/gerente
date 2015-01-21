from django.http import Http404, HttpResponse
from rest_framework import generics
from clasificador.models import ClassifierModel
from gerente.datatxt_helpers import Datatxt
from pruebas.models import BaseTestResult
from pruebas.serializers import BaseTestResultSerializer
from pruebas.tasks import test_model
import json


def model_test(request, datatxt_id):
    try:
        model = ClassifierModel.objects.get(datatxt_id=datatxt_id)
    except ClassifierModel.DoesNotExist:
        raise Http404

    #create a new classifier on datatxt
    dt = Datatxt()
    req = dt.create_model(model.json_model)
    res = req.json()
    model_id = res.get('id')
    #launch a celery task with this model
    task = test_model.delay(model_id, model)
    model.testing_task_id = task
    model.save()
    return HttpResponse(
        json.dumps({'task': task.id}), 'application/json'
    )


class ClassifierModelList(generics.ListAPIView):
    serializer_class = BaseTestResultSerializer

    def get_queryset(self):
        datatxt_id = self.kwargs['datatxt_id']
        return BaseTestResult.objects.filter(
            model_version__datatxt_id=datatxt_id).order_by('created')

    def check_permissions(self, request):
        return True

    def perform_authentication(self, request):
        pass



# class ClassifierModelDetail(generics.RetrieveAPIView):
#     queryset = ClassifierModel.objects.all()
#     serializer_class = BaseTestResultSerializer
#
#     def get_queryset(self):
#         datatxt_id = self.kwargs['datatxt_id']
#         return BaseTestResult.objects.filter(model_version__datatxt_id=datatxt_id)
