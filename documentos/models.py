from django.db import models
from django_extensions.db.models import TimeStampedModel


class BaseDocument(TimeStampedModel):
    file_name = models.TextField()
    original_text = models.TextField()
    goal_standard = models.TextField()


class DocumentPart(TimeStampedModel):
    document = models.ForeignKey(BaseDocument)
    text = models.TextField()


class GoalStandard(TimeStampedModel):
    name = models.TextField()

    def __unicode__(self):
        return self.name


class SuperNode(TimeStampedModel):
    name = models.TextField()
    verbose_name = models.TextField(blank=True, null=True)
    goal_standard = models.ManyToManyField(GoalStandard)

    def __unicode__(self):
        ret_value = self.name
        if self.verbose_name is not None:
            ret_value = "{} [{}]".format(self.verbose_name, ret_value)
        return ret_value


class Node(TimeStampedModel):
    name = models.TextField()
    alternative_names = models.TextField(null=True, blank=True)  # TODO remove
    super_node = models.ManyToManyField(SuperNode, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Frame(TimeStampedModel):
    node = models.ForeignKey(Node)
    text = models.TextField()
    annotations = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.text
