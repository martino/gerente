import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from rest_framework import generics
from clasificador.models import ClassifierModel
from clasificador.serializers import ClassifierModelSerializer
from documentos.helpers import create_new_model
from documentos.models import GoalStandard


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


class ClassifierCreate(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ClassifierCreate, self).dispatch(
            request, *args, **kwargs)

    def post(self, request):
        gs = GoalStandard.objects.all().order_by('-created')[0]
        res = create_new_model(
            gs,
            request.POST.get('name'),
            request.POST.get('description'),
            int(request.POST.get('topic_limit')),
            True,
            request.POST.get('use_keyentities'),
        )

        return HttpResponse(
            json.dumps({'result': res}), 'application/json'
        )
