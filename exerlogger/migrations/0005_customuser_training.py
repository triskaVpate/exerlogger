# Generated by Django 2.2.5 on 2020-01-04 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exerlogger', '0004_auto_20200103_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='training',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='exerlogger.Training', verbose_name='training'),
        ),
    ]
