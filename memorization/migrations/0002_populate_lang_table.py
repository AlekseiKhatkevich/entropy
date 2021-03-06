# Generated by Django 3.1.2 on 2020-10-31 16:42

from django.db import migrations

from memorization.language_codes import codes_dict
from memorization.models import Language


#  Populates 'Language' models DB table with language codes and names.


def forwards_func(apps, schema_editor):
    """
    Populate 'Language' model with language codes and names
    """
    Language_model = apps.get_model('memorization', 'Language')
    language_instances = [
        Language_model(code=code, name=name) for code, name in codes_dict.items()
    ]
    Language_model.objects.bulk_create(language_instances)


def reverse_func(apps, schema_editor):
    """
    Truncate 'Language' model's DB table.
    """
    Language_model = apps.get_model('memorization', 'Language')
    Language_model.objects.all().delete()


table_name = Language._meta.db_table

forward_sql = f"""
            create or replace function do_not_change()
              returns trigger
            as
            $$
            begin
              raise exception 'Cannot modify table "{table_name}"
                Contact the system administrator if you want to make this change.';
            end;
            $$
            language plpgsql;
            
            
            drop trigger IF EXISTS  no_change_trigger on "{table_name}";
            
            create trigger  no_change_trigger
              before insert or update or delete on "{table_name}"
              execute procedure do_not_change();
            """

reverse_sql = """
                drop  function do_not_change() cascade
                """


class Migration(migrations.Migration):
    dependencies = [
        ('memorization', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
        migrations.RunSQL(forward_sql, reverse_sql),
    ]
