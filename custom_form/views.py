from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import FormView, CreateView
from django.db import connection
from django.forms.formsets import formset_factory, BaseFormSet

from .models import FormModel, CustomModel
from .forms import CreateFieldsForm, CustomForm


class AddFieldView(CreateView):
    """
    添加表单字段
    POST 方式传入字典数据
    将字段数据存入数据库
    """
    form_class = CreateFieldsForm
    template_name = 'custom_form/create_form.html'

    def get_context_data(self, **kwargs):
        objs = FormModel.objects.all()
        kwargs['fields'] = objs

        return super(AddFieldView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        field = request.POST['field']
        field_name = request.POST['field_name']
        field_type = request.POST['field_type']
        temp_field = FormModel(field=field, field_name=field_name, field_type=field_type)
        temp_field.save()
        cursor = connection.cursor()
        cursor.execute('alter table custom_form_custommodel add COLUMN {} VARCHAR(20) DEFAULT NULL;'.format(field))

        return redirect('new_custom_form:add_field')


def delete_field(request, field):
    """
    删除字段
    """
    FormModel.objects.filter(field=field).delete()
    cursor = connection.cursor()
    cursor.execute('alter table custom_form_custommodel drop COLUMN {};'.format(field))

    return redirect('new_custom_form:add_field')


class CustomFormView(CreateView):
    """
    展示表单
    将上下文传入模板
    并可以向表单提交数据,存入数据库
    """
    model = CustomModel
    form_class = CustomForm
    template_name = 'custom_form/form.html'

    def get_context_data(self, **kwargs):
        """
        将表单字段上下文传入模板
        """
        fields = FormModel.objects.all()
        kwargs['fields'] = fields
        objs = CustomModel.objects.all()
        kwargs['objs'] = objs

        return super(CustomFormView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        遍历每个字段数据并存入数据库
        """
        key_list = []
        value_list = []
        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                key_list.append(key)
                value_list.append(value)
        cursor = connection.cursor()
        key_str = ','.join(key_list)
        value_str = '\''+'\',\''.join(value_list)+'\''
        sql = 'INSERT INTO custom_form_custommodel ({0}) VALUES ({1});'.format(key_str, value_str)
        cursor.execute(sql)

        return redirect('new_custom_form:form')
