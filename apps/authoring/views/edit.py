from annoying.decorators import JsonResponse
from authoring.models import AuthoredMaterial
from django import forms
from django.contrib import messages
from django.shortcuts import  get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import  TemplateView
from utils.decorators import login_required


class AuthoredMaterialForm(forms.ModelForm):

    # TODO: clean up HTML from `text` field.

    class Meta:
        model = AuthoredMaterial
        fields = ["title", "text"]
        widgets = dict(
            title=forms.HiddenInput(),
            text=forms.HiddenInput(),
        )


class Edit(TemplateView):

    template_name = "authoring/edit.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.material = get_object_or_404(
            AuthoredMaterial,
            id=int(kwargs["material_id"]),
            author=request.user
        )
        self.form = AuthoredMaterialForm(instance=self.material)
        return super(Edit, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        self.form = AuthoredMaterialForm(request.POST, instance=self.material)
        if self.form.is_valid():
            self.form.save()
            if request.is_ajax():
                return JsonResponse(dict(
                    status="success",
                    message=u"Saved.",
                ))
            messages.success(request, u"Saved.")
            return self.get(request, **kwargs)
        else:
            if request.is_ajax():
                # TODO: return error messages
                return JsonResponse(dict(
                    status="error",
                    message=u"Please correct the indicated errors.",
                ))
            messages.error(request, u"Please correct the indicated errors.")
            return self.get(request, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(Edit, self).get_context_data(**kwargs)
        data["form"] = self.form
        data["material"] = self.material
        return data



