from django.shortcuts import render, redirect
from django.views.generic.edit import FormView, CreateView
from django.db import connection
from django import forms
from django.contrib import messages

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
        """
        向模板传入创建的字段和表单
        """
        objs = FieldModel.objects.all()
        kwargs['fields'] = objs
        forms = FormModel.objects.all()
        kwargs['forms'] = forms

        return super(AddFieldView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        field = form.save(commit=False)
        form_name = form.cleaned_data['form_name']
        form = FormModel.objects.filter(form_name=form_name).first()

        # 如果表单不存在,则创建该表单
        if not form:
            form = FormModel.objects.create(form_name=form_name)

        # 当flag=True,代表此表已经添加过数据,禁止编辑
        if form.flag==1:
            messages.error(self.request, '该表单已创建模型,无法编辑')
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
    template_name = 'new_custom_form/form.html'

    def set_form(self, form_name):
        """
        创建form
        :param form_name:
        :return:
        """
        # 指定表单
        custom_form = self.get_form(form_class=FormForm)
        form = FormModel.objects.filter(form_name=form_name).first()
        # 指定字段, 这一步考虑了字段的顺序
        fields = FieldModel.objects.filter(form=form).order_by('id')
        for field in fields:
            # 根据field_type来设立不同类型的字段
            if field.field_type == 'int':
                custom_form.fields[field.field] = forms.IntegerField(label=field.field_name)
            # 在这里可以添加代码,以考虑更多的字段类型
            else:
                custom_form.fields[field.field] = forms.CharField(label=field.field_name)

        return custom_form

    def get(self, request, *args, **kwargs):
        custom_form = self.set_form(kwargs['form_name'])
        data = {'form_name': kwargs['form_name'],
                'custom_form': custom_form}

        return render(request, 'new_custom_form/form.html', data)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.set_form(kwargs['form_name'])
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
        custom_form = FormModel.objects.filter(form_name=form_name).first()

        # 如果表不存在,先创建表
        if custom_form.flag==0:
            fields_list = []
            fields = FieldModel.objects.filter(form=custom_form)
            # 创建 sql 语句
            for field in fields:
                str = '{0} varchar(50) not null'.format(field.field)
                fields_list.append(str)
            field_str = ','.join(fields_list)
            create_sql = 'create table {0}(' \
                         'id int(3) auto_increment not null primary key,' \
                         '{1}' \
                         ');'.format(form_name, field_str)
            # print(create_sql)
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
        messages.error(self.request, '输入表单无效')
        return redirect('new_custom_form:add_field')




