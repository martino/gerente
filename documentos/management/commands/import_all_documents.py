from glob import glob
from django.core.management import BaseCommand
from codecs import open
import json
from documentos.models import BaseDocument


class Command(BaseCommand):
    args = '<dir_path> <goal standard>'
    help = 'Load all txt documents into dir_path'

    def handle(self, *args, **options):
        try:
            dir_path = args[0]
        except IndexError:
            self.stderr.write('Missing document path')
            return

        try:
            gs_path = args[1]
            with open(gs_path) as f:
                gs = json.load(f)
        except IndexError:
            self.stderr.write('Missing goal standard path')
            return

        file_list = glob("{}/*.txt".format(dir_path))
        for file_path in file_list:
            file_name = file_path.split('/')[-1]
            try:
                goal_standard = gs[file_name]
            except KeyError:
                self.stderr.write('Missing file {}'.format(file_name))
                goal_standard = {}
            with open(file_path) as f:
                original_text = f.read()
            # text = original_text
            # headers_split = original_text.split('\t\t\n\t\t\n')
            # if len(headers_split) == 2:
            #     text = headers_split[1]
            doc = BaseDocument()
            doc.file_name = file_name
            doc.goal_standard = json.dumps(goal_standard)
            doc.original_text = original_text
            doc.save()
            # for part in text.split('.\n'):
            #     dp = DocumentPart()
            #     dp.document = doc
            #     dp.text = part
            #     dp.save()
