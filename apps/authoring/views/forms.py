from authoring.models import AuthoredMaterialDraft
from common.models import Grade
from curriculum.models import AlignmentTag, TaggedMaterial
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from materials.models.common import CC_LICENSE_URL_RE, License, Keyword
from itertools import chain
from core.forms import MultipleAutoCreateField, AutocompleteListWidget
from django.forms import ModelMultipleChoiceField
from django.forms.widgets import CheckboxInput
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from materials.models import GeneralSubject, Language, CourseMaterialType
import string


class LearningGoalsWidget(forms.Widget):

    def render(self, name, value, attrs=None):
        attrs = attrs or {}
        attrs["autocomplete"] = "off"
        if not value: value = []
        existing = []
        for v in value:
            existing.append((v, forms.TextInput().render(name, v, attrs)))
        return render_to_string("authoring/forms/learning-goals-widget.html", dict(
            existing=existing,
            new=forms.TextInput().render(name, u"", attrs)
        ))

    def value_from_datadict(self, data, files, name):
        return filter(bool, map(string.strip, data.getlist(name)))


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


class LicenseWidget(forms.Widget):

    DERIVATIVES_CHOICES = (
        (u"y", "Yes, allow"),
        (u"sa", "Yes, allow as long as others share alike"),
        (u"n", "No, do not allow"),
    )

    COMMERCIAL_CHOICES = (
        (u"y", "Yes, allow"),
        (u"n", "No, do not allow"),
    )

    def value_from_datadict(self, data, files, name):
        return data.get("%s_url" % name)

    def render(self, name, value, attrs=None):
        license_url = value.get("url", u"")
        license_name = value.get("name", u"")
        derivatives = u""
        commercial = u""

        r = CC_LICENSE_URL_RE.search(license_url)
        if r:
            cc_type = r.groupdict()["cc_type"]
            if "nd" in cc_type:
                derivatives = "n"
            elif "sa" in cc_type:
                derivatives = "sa"
            else:
                derivatives = "y"
            commercial = "n" if "nc" in cc_type else "y"
        else:
            cc_type = ""
            license_url = u""
            license_name = u""

        return mark_safe(render_to_string(
            "authoring/forms/license-widget.html",
            dict(
                name=name,
                cc_type=cc_type,
                name_widget=forms.HiddenInput().render("%s_name" % name, license_name),
                url_widget=forms.HiddenInput().render("%s_url" % name, license_url),
                derivatives_widget=forms.RadioSelect().render(
                    "%s_derivatives" % name,
                    derivatives,
                    choices=self.DERIVATIVES_CHOICES,
                ),
                commercial_widget=forms.RadioSelect().render(
                    "%s_commercial" % name,
                    commercial,
                    choices=self.COMMERCIAL_CHOICES,
                )
            )
        ))


class LicenseField(forms.Field):

    widget = LicenseWidget
    default_error_messages = {
        'required': _(u'Please select a license.'),
        'invalid': _(u'Invalid license URL.'),
    }

    def prepare_value(self, value):
        if not value:
            return {}
        if hasattr(value, '_meta'):
            value = value.serializable_value("url")
        else:
            value = value
        name = License.objects.get_cc_license_name_from_url(value) if CC_LICENSE_URL_RE.match(value) else u""
        return dict(url=value, name=name)

    def to_python(self, value):
        if not value:
            return None
        if not CC_LICENSE_URL_RE.match(value):
            raise forms.ValidationError(self.default_error_messages["invalid"])
        return dict(url=value, name=License.objects.get_cc_license_name_from_url(value))


# Single value select that returns data as a list
class SelectMultiple(forms.Select):

    def render(self, name, value, attrs=None, choices=()):
        if not value:
            value = None
        else:
            value = value[0]
        return super(SelectMultiple, self).render(name, value, attrs, choices)

    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        return data.get(name, None)


class AlignmentTagsWidget(forms.SelectMultiple):

    def render_tag(self, tag, name):
        return u"""<li data-id="%(id)i" class="user-tag rc3">
          <a href="#">%(code)s</a> <a class="delete">x</a>
          <input type="hidden" name="%(name)s" value="%(id)i">
          </li>""" % dict(
            id=tag.id,
            code=tag.full_code,
            name=name
        )

    def render(self, name, value, attrs=None, choices=()):
        output = []
        if value:
            for tag in AlignmentTag.objects.filter(id__in=value):
                output.append(self.render_tag(tag, name))
        return mark_safe(u"\n".join(output))


class GradesWidget(forms.SelectMultiple):

    def render(self, name, value, attrs=None, choices=()):
        value = value or []
        select = forms.Select(choices=self.choices).render(name+"_select", None)
        choices_dict = dict(self.choices)
        existing = []
        for v in value:
            existing.append(mark_safe(u"""<li><span>%s</span> %s <a href="#" class="delete ui-icon ui-icon-close">Delete</a></li>""" % (
                choices_dict[v],
                forms.HiddenInput().render(name, v),
            )))
        return render_to_string("authoring/forms/grades-widget.html", dict(
            name=name,
            existing=existing,
            select=select,
        ))


class EditFormNoLicense(forms.ModelForm):

    # TODO: clean up HTML from `text` field.
    # using lxml clean. Remove all styles, Keep only allowed classes,
    # remove scripts, styles, forms, iframes, objects, embeds

    learning_goals = MultipleAutoCreateField("title", widget=LearningGoalsWidget())
    keywords = MultipleAutoCreateField("name", widget=AutocompleteListWidget(Keyword, "name"), required=False)
    general_subjects = ModelMultipleChoiceField(GeneralSubject.objects.all(), widget=SubjectsWidget())
    grades = forms.ModelMultipleChoiceField(label=u"Grade", queryset=Grade.objects.all(), widget=GradesWidget())
    languages = forms.ModelMultipleChoiceField(label=u"Language", queryset=Language.objects.all(), widget=SelectMultiple())
    material_types = forms.ModelMultipleChoiceField(label=u"Material Type", queryset=CourseMaterialType.objects.all(), widget=SelectMultiple())
    alignment_tags = forms.ModelMultipleChoiceField(
        AlignmentTag.objects.all(),
        widget=AlignmentTagsWidget(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        not_required = kwargs.pop("not_required", False)
        self.user = kwargs.pop("user")
        super(EditFormNoLicense, self).__init__(*args, **kwargs)
        self.fields["grades"].empty_label = u"Select a Grade"
        self.content_type = ContentType.objects.get_for_model(self.instance)
        self.initial["alignment_tags"] = list(tagged.tag for tagged in TaggedMaterial.objects.filter(
            content_type=self.content_type,
            object_id=self.instance.id,
            user=self.user,
        ))
        if not_required:
            for field in self.fields.values():
                field.required = False

    class Meta:
        model = AuthoredMaterialDraft
        fields = ["title", "text", "abstract", "learning_goals", "keywords", "general_subjects", "grades", "languages", "material_types"]
        widgets = dict(
            title=forms.HiddenInput(),
            text=forms.HiddenInput(),
            abstract=forms.Textarea(attrs=dict(
                placeholder=u"Please give a short summary of your resource. This will appear as the preview in search results."
            ))
        )

    def save(self, commit=True):
        instance = super(EditFormNoLicense, self).save(commit)
        existing = set(tagged.tag for tagged in TaggedMaterial.objects.filter(
            content_type=self.content_type,
            object_id=instance.id,
            user=self.user,
        ))
        tags = set(self.cleaned_data.get("alignment_tags", []))
        for tag in existing - tags:
            TaggedMaterial.objects.filter(
                content_type=self.content_type,
                object_id=instance.id,
                user=self.user,
                tag=tag
            ).delete()
        for tag in tags - existing:
            TaggedMaterial.objects.create(
                content_type=self.content_type,
                object_id=instance.id,
                user=self.user,
                tag=tag
            )
        return instance


class EditForm(EditFormNoLicense):

    license = LicenseField()

    class Meta(EditFormNoLicense.Meta):
        fields = EditFormNoLicense.Meta.fields +  ["license"]
