from rest_framework import generics
from clasificador.models import ClassifierModel
from clasificador.serializers import ClassifierModelSerializer


class ClassifierModelList(generics.ListCreateAPIView):
    queryset = ClassifierModel.objects.all()
    serializer_class = ClassifierModelSerializer


class ClassifierModelDetail(generics.RetrieveUpdateAPIView):
    queryset = ClassifierModel.objects.all()
    serializer_class = ClassifierModelSerializer
    lookup_field = 'datatxt_id'
