from rest_framework import generics
from documentos.models import DocumentGroup, BaseDocument
from documentos.serializers import DocumentGroupSerializer, \
    BaseDocumentSerializer


class DocumentGroupList(generics.ListAPIView):
    # TODO optimize with prefetch related?
    queryset = DocumentGroup.objects.all()
    serializer_class = DocumentGroupSerializer


class DocumentGroupDetails(generics.RetrieveAPIView):
    # TODO optimize with prefetch related?
    queryset = DocumentGroup.objects.all()
    serializer_class = DocumentGroupSerializer


class BaseDocumentDetails(generics.RetrieveAPIView):
    # TODO optimize with prefetch related?
    queryset = BaseDocument.objects.all()
    serializer_class = BaseDocumentSerializer
