from django import forms

from .models import FormModel, CustomModel


class CreateFieldsForm(forms.ModelForm):

    class Meta:
        model = FormModel
        fields = ['field', 'field_name', 'field_type']


class CustomForm(forms.ModelForm):
    """
    要展示的表单
    从数据库里读字段数据并生产表单
    """

    class Meta:
        model = CustomModel
        exclude = ['', ]


def get_fields():
    fields = FormModel.objects.all()
    return fields.get_dict()
