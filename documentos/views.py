from rest_framework import generics
from documentos.models import DocumentGroup
from documentos.serializers import DocumentGroupSerializer


class DocumentGroupList(generics.ListAPIView):
    # TODO optimize with prefetch related?
    queryset = DocumentGroup.objects.all()
    serializer_class = DocumentGroupSerializer
