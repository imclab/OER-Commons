from autoslug import AutoSlugField
from common.fields import SeparatedValuesField
from common.models import StudentLevel, GeneralSubject
from django.contrib.auth.models import User
from django.db import models


class Lesson(models.Model):

    author = models.ForeignKey(User, null=True)
    is_new = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    title = models.CharField(max_length=200, default=u"")
    slug = AutoSlugField(populate_from="title")

    student_levels = models.ManyToManyField(StudentLevel)
    subjects = models.ManyToManyField(GeneralSubject)

    summary = models.TextField(default=u"")

    goals = SeparatedValuesField(default=u"")

    def __unicode__(self):
        return self.title or self.id

    def save(self, *args, **kwargs):
        if not self.title and not self.summary:
            self.is_new = True
        else:
            self.is_new = False
        super(Lesson, self).save(*args, **kwargs)