from django.http import Http404, HttpResponse
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from clasificador.models import ClassifierModel
from documentos.models import DocumentGroup
from gerente.datatxt_helpers import Datatxt
from pruebas.models import BaseTestResult, DocumentTestResult, \
    DocumentAnnotation
from pruebas.serializers import BaseTestResultSerializer, \
    DocumentTestResultSerializer, DocumentAnnotationSerializer, \
    DocumentTestResultSmallSerializer
from pruebas.tasks import test_model, test_document_set
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


def model_document_group(request, dg_pk, datatxt_id):
    try:
        model = ClassifierModel.objects.get(datatxt_id=datatxt_id)
    except ClassifierModel.DoesNotExist:
        raise Http404
    try:
        dg = DocumentGroup.objects.get(pk=dg_pk)
    except DocumentGroup.DoesNotExist:
        raise Http404
    try:
        threshold = float(request.GET.get('threshold'))
    except ValueError:
        threshold = 0.25

    #launch a celery task with this model
    task = test_document_set.delay(model, dg, threshold)
    dg.testing_task_id = task
    dg.save()
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


class BaseDocumentTestDetails(generics.RetrieveAPIView):
    serializer_class = DocumentTestResultSerializer
    queryset = DocumentTestResult.objects.all()

    def check_permissions(self, request):
        return True

    def perform_authentication(self, request):
        pass


class BaseDocumentTestList(generics.ListAPIView):
    serializer_class = DocumentTestResultSmallSerializer
    queryset = DocumentTestResult.objects.all().order_by('-created')

    def check_permissions(self, request):
        return True

    def perform_authentication(self, request):
        pass

class DocumentAnnotationDetails(generics.RetrieveAPIView):
    serializer_class = DocumentAnnotationSerializer

    def get_object(self):
        test_results = DocumentTestResult.objects.get(
            pk=self.kwargs['test_pk'])
        queryset = test_results.documentannotation_set.filter()

        filter = {
            'document__pk': self.kwargs['doc_pk']
        }
        return get_object_or_404(queryset, **filter)

    def check_permissions(self, request):
        return True

    def perform_authentication(self, request):
        pass
