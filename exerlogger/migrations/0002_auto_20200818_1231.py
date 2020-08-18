# Generated by Django 3.0.3 on 2020-08-18 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exerlogger', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='program', to='exerlogger.Program', verbose_name='program'),
        ),
    ]