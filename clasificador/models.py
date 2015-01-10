from django.db import models
from django_extensions.db.models import TimeStampedModel
from documentos.models import Frame


class ClassifierModel(TimeStampedModel):
    json_model = models.TextField()
    name = models.TextField()
    datatxt_id = models.TextField(blank=True, null=True)
    testing_task_id = models.TextField(blank=True, null=True)
    generation_frames = models.ManyToManyField(Frame)

    def __unicode__(self):
        return self.name
