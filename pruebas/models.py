from django.db import models
from django.db.models import TextField
from django_extensions.db.fields.json import JSONField
from django_extensions.db.models import TimeStampedModel
from clasificador.models import ClassifierModel
from documentos.models import BaseDocument, Frame, DocumentGroup


class BaseTestResult(TimeStampedModel):
    json_model = JSONField()
    micro_f1 = models.FloatField(null=True, blank=True)
    macro_f1 = models.FloatField(null=True, blank=True)
    micro_precision = models.FloatField(null=True, blank=True)
    macro_precision = models.FloatField(null=True, blank=True)
    micro_recall = models.FloatField(null=True, blank=True)
    macro_recall = models.FloatField(null=True, blank=True)
    model_version = models.ForeignKey(ClassifierModel, related_name='test')
    confusion_matrix = JSONField(null=True, blank=True)

    def get_result(self):
        result = {
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
        if self.confusion_matrix is not None:
            result['cmatrix'] = self.confusion_matrix

        return result


class DocumentTestResult(TimeStampedModel):
    document_group = models.ForeignKey(DocumentGroup)
    json_model = JSONField()
    model_version = models.ForeignKey(ClassifierModel, related_name='doc_test')
    scoring_result = JSONField(null=True)

    def __unicode__(self):
        return "{}".format(self.created)


class DocumentAnnotation(TimeStampedModel):
    test_results = JSONField()
    document = models.ForeignKey(BaseDocument, null=True)
    test_running = models.ForeignKey(DocumentTestResult)
    raw_result = JSONField(blank=True, null=True)


class FrameAnnotation(TimeStampedModel):
    test_results = JSONField()
    raw_scoring = TextField(blank=True, null=True)
    raw_result = JSONField(blank=True, null=True)
    frame = models.ForeignKey(Frame, null=True)
    test_running = models.ForeignKey(BaseTestResult)
