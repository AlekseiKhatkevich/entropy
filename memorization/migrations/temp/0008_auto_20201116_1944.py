# Generated by Django 3.1.3 on 2020-11-16 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memorization', '0007_auto_20201102_1226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='language',
            name='id',
        ),
        migrations.AlterField(
            model_name='language',
            name='code',
            field=models.CharField(editable=False, max_length=2, primary_key=True, serialize=False, verbose_name='country code acc. ISO 639'),
        ),
    ]