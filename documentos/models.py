from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_extensions.db.fields.json import JSONField


class DocumentGroup(TimeStampedModel):
    name = models.TextField()
    testing_task_id = models.TextField(blank=True, null=True)
    importing_task_id = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name


class BaseDocument(TimeStampedModel):
    file_name = models.TextField()
    original_text = models.TextField()
    goal_standard = JSONField()
    group = models.ForeignKey(DocumentGroup, null=True, blank=True)


class GoalStandard(TimeStampedModel):
    name = models.TextField()

    def __unicode__(self):
        return self.name


class SuperNode(TimeStampedModel):
    name = models.TextField()
    verbose_name = models.TextField(blank=True, null=True)
    # TODO this can be a foreignkey?
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
    annotations = JSONField(null=True, blank=True)
    key_entities = JSONField(null=True, blank=True)

    def __unicode__(self):
        return self.text
