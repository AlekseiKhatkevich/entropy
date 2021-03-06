import pytest
from django.db.utils import InternalError

from memorization.language_codes import codes_dict
from memorization.models import Language


@pytest.mark.django_db
class Test_memorization_0005:
    """
    Test on '0005_populate_lang_table.py' migration in 'memorization' app.
    Migration populates DB with language codes and names.
    """
    def test_forward_action(self):
        """
        Check that after migration DB table should be populated with language codes and names.
        """
        dict_from_db = {obj.code: obj.name for obj in Language.objects.all()}

        assert dict_from_db == codes_dict

    def test_read_only(self):
        """
        Check that Language table is read-only.
        """
        lng = Language.objects.first()
        lng.name = 'test'

        with pytest.raises(InternalError):
            lng.save(fc=False)

