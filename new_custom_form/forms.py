from django import forms

from .models import FormModel, FieldModel


class FormForm(forms.ModelForm):
    # name = forms.CharField(max_length=100, required=True, cl)
    form_name = forms.HiddenInput()

    class Meta:
        model = FormModel
        fields = []


class CreateFieldForm(forms.ModelForm):
    form_name = forms.CharField(max_length=100, required=True)
    field = forms.CharField(max_length=100, required=True)
    field_name = forms.CharField(max_length=100, required=True)
    field_type = forms.CharField(max_length=100, required=True)

    class Meta:
        model = FieldModel
        fields = ['form_name', 'field', 'field_name', 'field_type']




