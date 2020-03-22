# Generated by Django 2.2.5 on 2020-03-22 06:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exerlogger', '0015_auto_20200320_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+420123456789'. Up to 15 digits allowed.", regex='^\\+\\d{12}$')]),
        ),
    ]
