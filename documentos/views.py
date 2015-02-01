from rest_framework import generics
from documentos.models import DocumentGroup, BaseDocument
from documentos.serializers import DocumentGroupSerializer, \
    BaseDocumentSerializer


class DocumentGroupList(generics.ListAPIView):
    # TODO optimize with prefetch related?
    queryset = DocumentGroup.objects.all()
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
    # TODO optimize with prefetch related?
    queryset = BaseDocument.objects.all()
    serializer_class = BaseDocumentSerializer

    def check_permissions(self, request):
        return True

    def perform_authentication(self, request):
        pass
