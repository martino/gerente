from django.db import models
from django_extensions.db.models import TimeStampedModel


class ClassifierModel(TimeStampedModel):
    json_model = models.TextField()
    name = models.TextField()
    datatxt_id = models.TextField(blank=True, null=True)
    testing_task_id = models.TextField(blank=True, null=True)
