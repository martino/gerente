from django.contrib import admin
from documentos.models import BaseDocument, Node, Frame, \
    SuperNode, GoalStandard, DocumentGroup


admin.site.register(DocumentGroup)
admin.site.register(BaseDocument)
admin.site.register(Node)
admin.site.register(Frame)
admin.site.register(SuperNode)
admin.site.register(GoalStandard)
