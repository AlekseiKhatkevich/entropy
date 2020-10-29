from rest_framework.views import exception_handler
from rest_framework.response import Response as DRF_response
from rest_framework import status
from entropy.errors.schema import ErrorMessage
from entropy.errors import messages

def custom_exception_handler(exc, context):
    """
    {'timezone': [{'message': ErrorDetail(string='user_2 --- Timezone name is incorrect', code='user_2'), 'code': 'user_2'}]}
    :param exc:
    :param context:
    :return:
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
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
                    'status': status.HTTP_400_BAD_REQUEST,
                    'detail': message.detail,
                    'instance': 'placeholder',
                }
            else:
                message = err['message']

            data[field] = message

    return DRF_response(data=data, status=status.HTTP_400_BAD_REQUEST)

    return response