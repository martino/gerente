from django.contrib import admin
from documentos.models import BaseDocument, DocumentPart, Node, Frame, \
    SuperNode, GoalStandard


admin.site.register(BaseDocument)
admin.site.register(DocumentPart)
admin.site.register(Node)
admin.site.register(Frame)
admin.site.register(SuperNode)
admin.site.register(GoalStandard)
