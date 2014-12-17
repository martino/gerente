from django.contrib import admin
from documentos.models import BaseDocument, DocumentPart


admin.site.register(BaseDocument)
admin.site.register(DocumentPart)
