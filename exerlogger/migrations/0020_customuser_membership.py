# Generated by Django 2.2.5 on 2020-04-11 06:57

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exerlogger', '0019_auto_20200322_0651'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='membership',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True, verbose_name='membership'),
        ),
    ]