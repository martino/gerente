from rest_framework import generics
from clasificador.models import ClassifierModel
from clasificador.serializers import ClassifierModelSerializer


class ClassifierModelList(generics.ListCreateAPIView):
    queryset = ClassifierModel.objects.all().order_by('created')
    serializer_class = ClassifierModelSerializer

    def check_permissions(self, request):
        return True

    def perform_authentication(self, request):
        pass


class ClassifierModelDetail(generics.RetrieveUpdateAPIView):
    queryset = ClassifierModel.objects.all()
    serializer_class = ClassifierModelSerializer
    lookup_field = 'datatxt_id'

    def check_permissions(self, request):
        return True

    def perform_authentication(self, request):
        pass

