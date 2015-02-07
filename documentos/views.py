import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from rest_framework import generics
from documentos.models import DocumentGroup, BaseDocument
from documentos.serializers import DocumentGroupSerializer, \
    BaseDocumentSerializer
from documentos.tasks import import_documents


class DocumentGroupList(generics.ListCreateAPIView):
    # TODO optimize with prefetch related?
    queryset = DocumentGroup.objects.all().order_by('created')
    serializer_class = DocumentGroupSerializer

    def check_permissions(self, request):
        return True

    def perform_authentication(self, request):
        pass


class DocumentGroupDetails(generics.RetrieveAPIView):
    # TODO optimize with prefetch related?
    queryset = DocumentGroup.objects.all()
    serializer_class = DocumentGroupSerializer

    def check_permissions(self, request):
        return True

    def perform_authentication(self, request):
        pass


class BaseDocumentDetails(generics.RetrieveAPIView):
    queryset = BaseDocument.objects.all()
    serializer_class = BaseDocumentSerializer

    def check_permissions(self, request):
        return True

    def perform_authentication(self, request):
        pass


class DocumentImporter(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(DocumentImporter, self).dispatch(
            request, *args, **kwargs)

    def post(self, request, dg_pk):
        try:
            file_url = request.POST.get('url')
        except ValueError:
            return HttpResponse(
                json.dumps({'error': 'Missing url field'}),
                'application/json',
                400
            )
        try:
            dg = DocumentGroup.objects.get(pk=dg_pk)
        except DocumentGroup.DoesNotExist:
            return HttpResponse(
                json.dumps({'error': 'This DocumentGroup doesn\'t exists'}),
                'application/json',
                404
            )

        task = import_documents.delay(dg, file_url)
        dg.importing_task_id = task.id
        dg.save()
        return HttpResponse(
            json.dumps({'task': task.id}), 'application/json'
        )

