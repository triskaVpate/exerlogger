# Generated by Django 2.2.5 on 2019-11-12 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exerlogger', '0005_auto_20191111_2136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workout',
            name='exercises',
        ),
        migrations.AddField(
            model_name='exercise',
            name='workout',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='exerlogger.Workout', verbose_name='workout'),
            preserve_default=False,
        ),
    ]
