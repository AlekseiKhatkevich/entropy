from django.db.models import CharField
from django.db.models.functions import Length

CharField.register_lookup(Length)