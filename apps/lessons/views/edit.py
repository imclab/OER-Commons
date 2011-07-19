from annoying.decorators import JsonResponse
from common.models import StudentLevel, GeneralSubject
from django import forms
from django.forms.util import flatatt
from django.http import HttpResponse, Http404
from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils.decorators import method_decorator
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, View
from lessons.models import Lesson
from lessons.views import LessonViewMixin
from sorl.thumbnail.shortcuts import delete
from utils.decorators import login_required
from utils.views import OERViewMixin
import json
import string
import time


class GoalsWidget(forms.widgets.Input):

    input_type = "text"
    EXTRA_INPUTS = 3

    def render(self, name, value, attrs=None):
        if value is None: value = []
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        id_ = final_attrs.get('id', None)
        inputs = []
        for i, v in enumerate(value + ([u""] * self.EXTRA_INPUTS)):
            input_attrs = dict(value=force_unicode(v), **final_attrs)
            if id_:
                # An ID attribute was given. Add a numeric index as a suffix
                # so that the inputs don't all have the same ID attribute.
                input_attrs['id'] = '%s_%s' % (id_, i)
            inputs.append(u'<li><input%s /></li>' % flatatt(input_attrs))
        return mark_safe(u'<ul>%s</ul> <a href="#" class="dashed">Add another</a>' % u'\n'.join(inputs))

    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            value = data.getlist(name)
        else:
            value = data.get(name, None)
        if value is None:
            return value
        return filter(bool, map(string.strip, value))


class EditLessonForm(forms.ModelForm):

    title = forms.CharField(label=u"Name your lesson")

    student_levels = forms.ModelMultipleChoiceField(StudentLevel.objects.all(),
                        label=u"Level:",
                        widget=forms.CheckboxSelectMultiple())

    subjects = forms.ModelMultipleChoiceField(GeneralSubject.objects.all(),
                        label=u"Primary subject",
                        widget=forms.CheckboxSelectMultiple())

    summary = forms.CharField(widget=forms.Textarea(),
                        label=u"Summary",
                        help_text=u"Quick description of your lesson")

    goals = forms.Field(widget=GoalsWidget(),
                        label=u"Lesson goals",
                        help_text=u"What do you hope students will learn?")

    class Meta:
        fields = ["title", "student_levels", "subjects", "summary", "goals"]
        model = Lesson


class EditLesson(LessonViewMixin, OERViewMixin, TemplateView):

    template_name = "lessons/authoring/edit-lesson.html"
    restrict_to_owner = True

    def get_page_title(self):
        if self.lesson.title:
            return u'Edit "%s"' % self.lesson.title
        return u"Edit Lesson"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditLesson, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if getattr(self, "form", None) is None:
            self.form = EditLessonForm(instance=self.lesson)
        return super(EditLesson, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if "upload-image" in request.POST:
            form = LessonImageForm(request.POST, request.FILES, instance=self.lesson)
            response = dict(status="error", message=u"")
            if form.is_valid():
                if self.lesson.image:
                    delete(self.lesson.image)
                image = form.cleaned_data["file"]
                if image.content_type == "image/jpeg":
                    extension = ".jpg"
                elif image.content_type == "image/png":
                    extension = ".png"
                elif image.content_type == "image/gif":
                    extension = ".gif"
                else:
                    extension = ""
                filename = "%i%s" % (self.lesson.id, extension)
                self.lesson.image.save(filename, image)
                response["status"] = "success"
                response["message"] = u"Your picture is saved."
                response["url"] = self.lesson.get_thumbnail().url + "?" + str(int(time.time()))
            else:
                response["message"] = form.errors["file"][0]
            # We don't use application/json content type here because IE misinterprets it.
            return HttpResponse(json.dumps(response))
        elif "remove-image" in request.POST:
            if self.lesson.image:
                delete(self.lesson.image)
            return JsonResponse(dict(status="success",
                                     message=u"Image was removed."))

        self.form = EditLessonForm(request.POST, instance=self.lesson)
        if self.form.is_valid():
            self.form.save()
            if request.is_ajax():
                return JsonResponse(dict(status="success", message=u"Changes were saved."))
        else:
            if request.is_ajax():
                errors = {}
                for field_name, errors_list in self.form.errors.items():
                    errors[field_name] = errors_list[0]
                return JsonResponse(dict(status="error", errors=errors))

        return self.get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        data = super(EditLesson, self).get_context_data(*args, **kwargs)
        data["form"] = self.form
        return data


class LessonImageForm(forms.Form):

    file = forms.FileField()


class LessonImage(LessonViewMixin, View):

    restrict_to_owner = True
    action = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LessonImage, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.action == "upload":
            form = LessonImageForm(request.POST, request.FILES)
            response = dict(status="error", message=u"")
            if form.is_valid():
                if self.lesson.image:
                    delete(self.lesson.image)
                image = form.cleaned_data["file"]
                if image.content_type == "image/jpeg":
                    extension = ".jpg"
                elif image.content_type == "image/png":
                    extension = ".png"
                elif image.content_type == "image/gif":
                    extension = ".gif"
                else:
                    extension = ""
                filename = "%i%s" % (self.lesson.id, extension)
                self.lesson.image.save(filename, image)
                response["status"] = "success"
                response["message"] = u"Your picture is saved."
                response["url"] = self.lesson.get_thumbnail().url + "?" + str(int(time.time()))
            else:
                response["message"] = form.errors["file"][0]
            # We don't use application/json content type here because IE misinterprets it.
            return HttpResponse(json.dumps(response))
        elif self.action == "remove":
            if self.lesson.image:
                delete(self.lesson.image)
                self.lesson.image = None
                self.lesson.save()
            return JsonResponse(dict(status="success",
                                     message=u"Image was removed."))
        raise Http404()
