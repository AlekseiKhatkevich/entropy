from django.contrib.postgres.operations import CreateExtension
# All extensions are here.

from django.db import migrations


class IntarrayExtension(CreateExtension):
    """
    Creates 'intarray' extension for Postgres.
    """

    def __init__(self):
        self.name = 'intarray'


class Migration(migrations.Migration):

    dependencies = [
        ('memorization', '0002_populate_lang_table'),
    ]

    operations = [
        IntarrayExtension(),
    ]
