# Generated by Django 3.1.3 on 2020-11-22 13:30

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('memorization', '0006_auto_20201118_1950'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='notebook',
            constraint=models.CheckConstraint(check=models.Q(entry_date__lte=django.db.models.expressions.F('memorization_date')), name='entry_date_vs_memorization_date_check'),
        ),
    ]
