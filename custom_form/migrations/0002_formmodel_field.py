# Generated by Django 2.1.2 on 2018-11-07 16:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('custom_form', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='formmodel',
            name='field',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
