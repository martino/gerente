from django.core.management import BaseCommand
import json
from documentos.models import DocumentGroup, BaseDocument


def compare_score_with_gs(matrix, score):
    res = {}
    # print matrix.keys()
    # print score.keys()
    for (k, v) in matrix.iteritems():
        s1 = set(v)
        s2 = set(score.get(k, []))
        intersection = s1.intersection(s2)
        # print "{} {} {} {}".format(k, len(s1), len(s2), len(intersection))
        if len(s1):
            res[k] = (len(intersection)*100)/len(s1)
    return res


class Command(BaseCommand):
    args = '<document_group_id> <gs_matrix>'
    help = 'Compare dcoument group classification with a gs'

    def handle(self, *args, **options):
        matrix = {}
        try:
            dg = DocumentGroup.objects.get(pk=args[0])
        except IndexError:
            self.stderr.write('Missing DocumentGroup pk')
            return
        except DocumentGroup.DoesNotExist:
            self.stderr.write("This DocumentGroup doesn't exists")
            return

        try:
            matrix_path = args[1]
            with open(matrix_path) as f:
                matrix = json.load(f)
        except IndexError:
            self.stderr.write('Missing matrix path')
            return
        except IOError:
            self.stderr.write('Issue opening this file')
            return

        print " & ".join(matrix.keys())

        for results in dg.documenttestresult_set.all().order_by('created'):
            score = {
                key: BaseDocument.objects.filter(pk__in=values)
                    .values_list('file_name', flat=True)
                for key, values in results.scoring_result.iteritems()
            }
            print '\hline'
            # print results
            res = compare_score_with_gs(matrix, score)
            # print res
            latex_value = " & ".join([str(v) for (k, v) in res.iteritems()])
            print "{} \\\\".format(latex_value)


