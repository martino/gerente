import simplejson as json
from codecs import open
from django.core.management import BaseCommand
from clasificador.models import ClassifierModel
from clasificador.serializers import ClassifierModelSerializer


class Command(BaseCommand):
    args = '<model_id> <model_data_path>'
    help = 'Update model_id with data in model_data_path'

    def handle(self, *args, **options):
        try:
            model = ClassifierModel.objects.get(pk=args[0])
        except IndexError:
            self.stderr.write('Missing classifier pk')
            return
        except ClassifierModel.DoesNotExist:
            self.stderr.write("This models doesn't exists")
            return

        try:
            model_path = args[1]
            with open(model_path) as f:
                new_model = json.load(f)
        except IndexError:
            self.stderr.write('Missing model path')
            return
        except IOError:
            self.stderr.write('Issue opening this file')
            return

        serializer = ClassifierModelSerializer()
        serializer.update(
            model, {'json_model': json.dumps(new_model, use_decimal=True)})
