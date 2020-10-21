from entropy.errors.schema import ErrorMessage

# POSSIBLE SECTIONS:

# auth - related to authentication
# user - related to user creation/modification  and user data in general

user_1 = ErrorMessage(
    section='user',
    error_code_number=1,
    title='No email or password',
    detail='Email and password must be specified',
)
user_2 = ErrorMessage(
    section='user',
    error_code_number=2,
    title='Timezone name is incorrect',
    detail='Provided user timezone name is incorrect.'
           ' Please comply to IANA tz-database timezone name',
)
