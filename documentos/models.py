from django.db import models
from django_extensions.db.models import TimeStampedModel


class BaseDocument(TimeStampedModel):
    file_name = models.TextField()
    original_text = models.TextField()
    goal_standard = models.TextField()


class DocumentPart(TimeStampedModel):
    document = models.ForeignKey(BaseDocument)
    text = models.TextField()
