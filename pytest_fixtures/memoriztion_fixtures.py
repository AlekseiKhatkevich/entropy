import pytest


@pytest.fixture(scope='module')
def create_language_families(db):
    """
    Creates language families.
    """
    family_1 = ('es', 'pt', 'it', 'fr', )
    family_2 = ('ru', 'uk', 'be', )
    family_3 = ('de', 'nl', )