from django.db import models
from django_extensions.db.models import TimeStampedModel
from clasificador.models import ClassifierModel
from documentos.models import BaseDocument


class BaseTestResult(TimeStampedModel):
    json_model = models.TextField()
    micro_f1 = models.FloatField(null=True, blank=True)
    macro_f1 = models.FloatField(null=True, blank=True)
    micro_precision = models.FloatField(null=True, blank=True)
    macro_precision = models.FloatField(null=True, blank=True)
    micro_recall = models.FloatField(null=True, blank=True)
    macro_recall = models.FloatField(null=True, blank=True)
    model_version = models.ForeignKey(ClassifierModel, related_name='test')

    def get_result(self):
        return {
            'micro': {
                'fscore': self.micro_f1,
                'precision': self.micro_precision,
                'recall': self.micro_recall
            },
            'macro': {
                'fscore': self.macro_f1,
                'precision': self.macro_precision,
                'recall': self.macro_recall
            }
        }


class DocumentAnnotation(TimeStampedModel):
    test_results = models.TextField()
    document = models.ForeignKey(BaseDocument, null=True)
    test_running = models.ForeignKey(BaseTestResult)
    raw_result = models.TextField(blank=True, null=True)