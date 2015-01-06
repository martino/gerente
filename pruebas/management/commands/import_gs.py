import json
from django.core.management import BaseCommand
from documentos.models import BaseDocument
from gerente.datatxt_helpers import Datatxt
from pruebas.models import ModelClass, GoalStandard


class Command(BaseCommand):
    help = 'Convert old style goal standard into a new one'

    def handle(self, *args, **options):
        dt = Datatxt()
        for document in BaseDocument.objects.all():
            gs = json.loads(document.goal_standard)
            for class_name, value in gs.iteritems():
                mc = ModelClass.objects.get_or_create(name=class_name)[0]
                for frame in value['frames']:
                    annotations = {}
                    res = dt.nex(frame)
                    if res.ok:
                        annotations = res.json().get('annotations')
                    GoalStandard.objects.create(
                        class_obj=mc,
                        frame=frame,
                        annotations=json.dumps(annotations)
                    )
