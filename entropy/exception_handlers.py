from functools import singledispatch

from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.response import Response as DRF_response
from rest_framework.views import exception_handler

from entropy.errors import messages


@singledispatch
def custom_exception_handler(exc, context, *args, **kwargs):
    """
    Base function for handling exceptions in DRF.
    """
    response = exception_handler(exc, context)

    return response


@custom_exception_handler.register(serializers.ValidationError)
@custom_exception_handler.register(ValidationError)
def _(exc, context, *args, **kwargs):
    """
    Handles ValidationErrors of different kind. Substitutes standard error behaviour by adding
    following fields to each error description.
                    'type'
                    'title'
                    'status'
                    'detail'
                    'instance'
    """
    # example of exc.get_full_details()
    # {'timezone': [
    # {'message': ErrorDetail(string='user_2 --- Timezone name is incorrect', code='user_2'), 'code': 'user_2'}
    # ]}
    fields_to_err_dict = exc.get_full_details()

    data = {}
    for field, err_list in fields_to_err_dict.items():
        for err in err_list:
            code = err['code']
            message = getattr(messages, code, None)

            if message is not None:
                message = {
                    'type': message.error_code,
                    'title': message.title,
                    'status': exc.status_code,
                    'detail': message.detail,
                    'instance': context['request'].path,
                }
            else:
                message = err['message']

            data[field] = [message]

    return DRF_response(data=data, status=exc.status_code)

