#  Django Rest Framework settings

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'drf_ujson.renderers.UJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
            'drf_ujson.parsers.UJSONParser',
            'rest_framework.parsers.FormParser',
            'rest_framework.parsers.MultiPartParser',
        ),
}
