from django.contrib import admin
from pruebas.models import BaseTestResult
from pruebas.models import DocumentAnnotation


admin.site.register(BaseTestResult)
admin.site.register(DocumentAnnotation)
