from itertools import chain
from authoring.models import AuthoredMaterial
from django import forms
from django.contrib import messages
from django.forms import ModelMultipleChoiceField
from django.forms.widgets import CheckboxInput
from django.shortcuts import  get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.views.generic.base import  TemplateView
from materials.models import GeneralSubject, Language
from utils.decorators import login_required
from utils.forms import MultipleAutoCreateField


class SubjectsWidget(forms.CheckboxSelectMultiple):

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<ul>']
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            if i == (len(self.choices) / 2):
                output.append(u'</ul>')
                output.append(u'<ul>')

            cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(option_label))
            output.append(u'<li><label%s>%s %s</label></li>' % (label_for, rendered_cb, option_label))
        output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))


class Form(forms.ModelForm):

    learning_goals = MultipleAutoCreateField("title")
    keywords = MultipleAutoCreateField("name", required=False)
    subjects = ModelMultipleChoiceField(GeneralSubject.objects.all(), widget=SubjectsWidget())
    language = forms.ModelChoiceField(queryset=Language.objects.all(), required=False)

    class Meta:
        model = AuthoredMaterial
        fields = ["summary", "learning_goals", "keywords", "subjects", "grade_level", "language"]
        widgets = dict(
            summary=forms.Textarea(attrs=dict(placeholder=u"Please give a short summary of your resource. This will appear as the preview in search results."))
        )

class Describe(TemplateView):

    template_name = "authoring/describe.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.material = get_object_or_404(
            AuthoredMaterial,
            id=int(kwargs["material_id"]),
            author=request.user
        )
        self.form = Form(instance=self.material)
        return super(Describe, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        self.form = Form(request.POST, instance=self.material)
        if self.form.is_valid():
            self.form.save()
        else:
            messages.error(request, u"Please correct the indicated errors.")
            return self.get(request, **kwargs)
        if request.POST.get("next") == "true":
            return self.get(request, **kwargs)
        elif request.POST.get("next") == "false":
            return redirect("authoring:write", material_id=self.material.id)
        return self.get(request, **kwargs)


    def get_context_data(self, **kwargs):
        data = super(Describe, self).get_context_data(**kwargs)
        data["form"] = self.form
        data["material"] = self.material
        return data


