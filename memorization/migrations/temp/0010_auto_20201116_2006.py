# Generated by Django 3.1.3 on 2020-11-16 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('memorization', '0009_auto_20201116_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='language',
            field=models.ForeignKey(default='ru', on_delete=django.db.models.deletion.PROTECT, to='memorization.language', verbose_name='language of the word'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='word',
            unique_together={('name', 'language')},
        ),
    ]