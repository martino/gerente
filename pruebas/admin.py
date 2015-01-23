from django.contrib import admin
from pruebas.models import BaseTestResult, DocumentTestResult, \
    FrameAnnotation, DocumentAnnotation


admin.site.register(BaseTestResult)
admin.site.register(FrameAnnotation)
admin.site.register(DocumentTestResult)
admin.site.register(DocumentAnnotation)
