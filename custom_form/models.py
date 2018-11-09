from django.db import models


# 允许的字段类型
FIELD_TYPE = ['text', 'select']

DD = '1'

class FormModel(models.Model):
    field = models.CharField(max_length=100, null=False, blank=False, unique=True)
    field_name = models.CharField(max_length=100, null=False, blank=False)
    field_type = models.CharField(max_length=100, null=False, blank=False)
    # field_options = models.CharField(null=True, blank=True)     # 选择性字段的可选项

    class Meta:
        verbose_name = '表单模型'
        verbose_name_plural = verbose_name


class CustomModel(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)

    class Meta:
        verbose_name = '个人信息'
        verbose_name_plural = verbose_name


