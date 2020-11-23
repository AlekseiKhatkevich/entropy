# Generated by Django 3.1.3 on 2020-11-23 11:14

from django.db import migrations, models
import django.db.models.functions.datetime


class Migration(migrations.Migration):

    dependencies = [
        ('memorization', '0009_same_language_check_constraint'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='notebook',
            constraint=models.CheckConstraint(check=models.Q(('entry_date__lt', django.db.models.functions.datetime.Now()), ('memorization_date__lt', django.db.models.functions.datetime.Now())), name='protect_future_check'),
        ),
    ]