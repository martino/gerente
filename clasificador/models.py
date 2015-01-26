from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_extensions.db.fields.json import JSONField
from documentos.models import Frame, GoalStandard


class ClassifierModel(TimeStampedModel):
    json_model = JSONField()
    name = models.TextField()
    datatxt_id = models.TextField(blank=True, null=True)
    testing_task_id = models.TextField(blank=True, null=True)
    generation_frames = models.ManyToManyField(Frame)
    goal_standard = models.ForeignKey(GoalStandard)

    def __unicode__(self):
        return self.name
