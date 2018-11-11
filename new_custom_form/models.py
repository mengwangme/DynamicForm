from django.db import models


class FormModel(models.Model):
    form_name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    flag = models.BooleanField(default=False)

    class Meta:
        verbose_name = '表单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.form_name


class FieldModel(models.Model):
    form = models.ForeignKey(FormModel, on_delete=models.CASCADE)

    field = models.CharField(max_length=100, null=False, blank=False)
    field_name = models.CharField(max_length=100, null=False, blank=False)
    field_type = models.CharField(max_length=100, null=False, blank=False)
    # field_options = models.CharField(null=True, blank=True)     # 选择性字段的可选项

    class Meta:
        verbose_name = '字段'
        verbose_name_plural = verbose_name

    def __str__(self):
        str = self.field + '({})'.format(self.form)
        return str

