# Generated by Django 2.2.5 on 2020-01-07 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exerlogger', '0007_customuser_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='exerlogger.Lesson', verbose_name='lesson'),
        ),
    ]