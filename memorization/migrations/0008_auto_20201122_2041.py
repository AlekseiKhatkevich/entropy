# Generated by Django 3.1.3 on 2020-11-22 17:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('memorization', '0007_auto_20201122_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notebook',
            name='entry_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='date and time when entry was created'),
        ),
    ]
