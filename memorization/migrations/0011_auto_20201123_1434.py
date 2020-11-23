# Generated by Django 3.1.3 on 2020-11-23 11:34

from django.db import migrations, models
import django.utils.timezone
import entropy.validators


class Migration(migrations.Migration):

    dependencies = [
        ('memorization', '0010_auto_20201123_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notebook',
            name='entry_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, validators=[entropy.validators.ProtectFutureValidator('memo_notebook_3 --- entry date in the future', 'memo_notebook_3')], verbose_name='date and time when entry was created'),
        ),
        migrations.AlterField(
            model_name='notebook',
            name='memorization_date',
            field=models.DateTimeField(blank=True, null=True, validators=[entropy.validators.ProtectFutureValidator('memo_notebook_4 --- memorization date in the future', 'memo_notebook_4')], verbose_name='date when word was memorized'),
        ),
    ]
