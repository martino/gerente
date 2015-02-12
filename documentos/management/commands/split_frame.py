from django.core.management import BaseCommand
from django.db import transaction
import requests
from django.conf import settings
from documentos.models import GoalStandard, Frame, SuperNode, Node
from gerente.datatxt_helpers import Datatxt


def split_frame(text):
    return [t for t in text.strip().split('.') if t]


class Command(BaseCommand):
    help = 'Convert old style goal standard into a new one'

    def handle(self, *args, **options):
        dt = Datatxt()
        with transaction.atomic():
            gs = GoalStandard.objects.create(name='Protezionismo v4')
            old_gs = GoalStandard.objects.get(pk=2)
            old_frames = [
                (b.name, b.verbose_name, b.node_set.all().values_list('pk', 'name'))
                for b in old_gs.supernode_set.all()
            ]

            for sn in old_frames:
                new_sn = SuperNode.objects.create(name=sn[0], verbose_name=sn[1])
                new_sn.goal_standard.add(gs)

                for fr in sn[2]:
                    print 'creating {}'.format(fr[1])
                    new_node = Node.objects.create(name=fr[1])
                    new_node.super_node.add(new_sn)
                    frame_list = list(Frame.objects.filter(node__pk=fr[0]))
                    for frame in frame_list:
                        new_texts = split_frame(frame.text)
                        for nt in new_texts:
                            annotations = {}
                            key_annotations = {}
                            # use keyword entities:
                            res = requests.post(
                                settings.KEYWORDS_SERVICE,
                                data={'max': 15, 'text': nt},
                                auth=settings.KEYWORDS_SERVICE_AUTH
                            )
                            # anntoate with datatxt
                            dt_res = dt.nex(nt)

                            if res.ok:
                                clusters = res.json().get('clusters')
                                key_annotations = {
                                    e: r
                                    for cluster in clusters
                                    for (e, r) in cluster.iteritems()
                                }

                            if dt_res.ok:
                                annotations = res.json().get('annotations')
                            Frame.objects.create(
                                node=new_node,
                                text=nt,
                                annotations=annotations,
                                key_entities=key_annotations
                            )
