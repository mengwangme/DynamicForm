from django.shortcuts import render, redirect, render_to_response
from django.views.generic import View
from django.views.generic.edit import FormView, CreateView
from django.db import connection
from django.forms.formsets import formset_factory, BaseFormSet
from django.middleware import csrf
from django import forms

from .models import FormModel, FieldModel
from .forms import FormForm, CreateFieldForm


class AddFieldView(CreateView):
    """
    添加表单字段
    POST 方式传入字典数据
    将字段数据存入数据库
    """
    model = FieldModel
    form_class = CreateFieldForm
    template_name = 'new_custom_form/create_form.html'

    def get_context_data(self, **kwargs):
        objs = FieldModel.objects.all()
        kwargs['fields'] = objs
        forms = FormModel.objects.all()
        kwargs['forms'] = forms

        return super(AddFieldView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        print('验证成功')
        field = form.save(commit=False)
        # print(form.cleaned_data)
        form_name = form.cleaned_data['form_name']
        form = FormModel.objects.filter(form_name=form_name).first()
        if not form:
            form = FormModel.objects.create(form_name=form_name)
        # 当flag=True,禁止编辑
        if form.flag==1:
            return redirect('new_custom_form:add_field')
        else:
            field.form = form
            field.save()
            return redirect('new_custom_form:add_field')


def delete_field(request, id):
    """
    删除字段
    :param request:
    :return:
    """
    FieldModel.objects.filter(id=id).delete()

    return redirect('new_custom_form:add_field')


class CustomFormView(FormView):

    # model = FormModel
    template_name = 'new_custom_form/form.html'
    # form_class = FormForm

    def set_form(self, form_name):
        """
        创建form
        :param form_name:
        :return:
        """
        # 指定表单
        custom_form = self.get_form(form_class=FormForm)
        # custom_form = forms.ModelForm()
        form = FormModel.objects.filter(form_name=form_name).first()
        # 指定字段
        fields = FieldModel.objects.filter(form=form)
        for field in fields:
            custom_form.fields[field.field] = forms.CharField()
        # self.form_class = custom_form
        return custom_form

    def get(self, request, *args, **kwargs):
        # data['form_name'] = kwargs['form_name']
        # 指定表单
        # custom_form = self.get_form(form_class=FormForm)
        # form = FormModel.objects.filter(form_name=kwargs['form_name']).first()
        # # 指定字段
        # fields = FieldModel.objects.filter(form=form)
        # for field in fields:
        #     custom_form.fields[field.field] = forms.CharField()
        # self.form_class = custom_form
        # print(self.form_class)
        custom_form = self.set_form(kwargs['form_name'])
        data = {}
        data = {'form_name': kwargs['form_name'],
                'custom_form': custom_form}

        # return render_to_response('new_custom_form/form.html', data)
        return render(request, 'new_custom_form/form.html', data)

    def post(self, request, *args, **kwargs):
        self.object = None
        # form = kwargs['custom_form']
        form = self.set_form(kwargs['form_name'])
        # form = self.get_form(form_class=form)
        # print(self.form_class)
        print(form)
        if form.is_valid():
            print('验证成功')
            return self.form_valid(form, kwargs['form_name'])
        else:
            print('验证失败')
            return self.form_invalid(form)


    def form_valid(self, form, form_name):
        form.save(commit=False)
        cursor = connection.cursor()

        # form_name = form.cleaned_data['name']
        custom_form = FormModel.objects.filter(form_name=form_name).first()

        # 如果表不存在,先创建表
        if custom_form.flag==0:
            fields_list = []
            fields = FieldModel.objects.filter(form=custom_form)
            for field in fields:
                str = '{0} varchar(50) not null'.format(field.field)
                fields_list.append(str)
            field_str = ','.join(fields_list)
            create_sql = 'create table {0}(' \
                         'id int(3) auto_increment not null primary key,' \
                         '{1}' \
                         ');'.format(form_name, field_str)
            print(create_sql)
            cursor.execute(create_sql)
            # 将模型改为不可编辑
            FormModel.objects.filter(form_name=form_name).update(flag=1)

        # 向表中传入数据
        key_list = []
        value_list = []
        for key, value in form.cleaned_data.items():
            if key != 'form_name':
                key_list.append(key)
                value_list.append(value)

        key_str = ','.join(key_list)
        value_str = '\''+'\',\''.join(value_list)+'\''
        insert_sql = 'INSERT INTO {0} ({1}) VALUES ({2});'.format(form_name, key_str, value_str)
        cursor.execute(insert_sql)

        return redirect('/form/{}'.format(form_name))

    def form_invalid(self, form):

        return redirect('new_custom_form:add_field')




