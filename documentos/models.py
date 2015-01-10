from django.db import models
from django_extensions.db.models import TimeStampedModel


class BaseDocument(TimeStampedModel):
    file_name = models.TextField()
    original_text = models.TextField()
    goal_standard = models.TextField()


class DocumentPart(TimeStampedModel):
    document = models.ForeignKey(BaseDocument)
    text = models.TextField()


class Node(TimeStampedModel):
    name = models.TextField()
    alternative_names = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Frame(TimeStampedModel):
    node = models.ForeignKey(Node)
    text = models.TextField()
    annotations = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.text
