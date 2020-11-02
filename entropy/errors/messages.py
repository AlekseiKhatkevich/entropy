from django.contrib.auth.password_validation import password_validators_help_texts

from entropy.errors.schema import ErrorMessage

# POSSIBLE SECTIONS:

# auth - related to authentication(Djoser and Simple_jwt mainly)
# user - related to user creation/modification  and user data in general
# memo_family - related to Family model in 'Memorization' app.

memo_family_1 = ErrorMessage(
    section='memo_family',
    error_code_number=1,
    title='Language points on itself',
    detail='Language can not point on itself. In language family left and right languages in'
           'language pairs should be different languages',
)
#  --------------------------------------------------------------------------------------------------
user_2 = ErrorMessage(
    section='user',
    error_code_number=2,
    title='Timezone name is incorrect',
    detail='Provided user timezone name is incorrect.'
           ' Please comply to IANA tz-database timezone name',
)
user_3 = ErrorMessage(
    section='user',
    error_code_number=3,
    title='Password is not suitable',
    detail=password_validators_help_texts(),
)
user_4 = ErrorMessage(
    section='user',
    error_code_number=4,
    title='Wrong password hash',
    detail='Somehow not valid argon2 hash was attempted to get saved in DB.'
           'Perhaps you need to use manager method "create_user" instead of "objects.create(**kwargs)"'
           'or "get_user_model()(**kwargs)"',
)

