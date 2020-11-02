import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg2 import openapi
from drf_yasg2.views import get_schema_view
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api-auth/', include('rest_framework.urls')),
]

schema_view = get_schema_view(
      openapi.Info(
         title='EnTrOpY',
         default_version='v1',
         description='...void...',
         contact=openapi.Contact(email='hardcase@inbox.ru'),
         license=openapi.License(name='BDSM License'),
      ),
      public=True,
      permission_classes=(permissions.AllowAny,),
   )

#  Schema API documentations endpoints.
urlpatterns += [
      re_path(
          r'^swagger(?P<format>\.json|\.yaml)$'
          , schema_view.without_ui(cache_timeout=0),
          name='schema-json',
      ),
      re_path(
          r'^swagger/$',
          schema_view.with_ui('swagger', cache_timeout=0),
          name='schema-swagger-ui',
      ),
      re_path(
          r'^redoc/$',
          schema_view.with_ui('redoc', cache_timeout=0),
          name='schema-redoc',
      ),
   ]
#  Endpoints are present only during running in development.
if settings.DEBUG:
    urlpatterns.append(
        path('__debug__/', include(debug_toolbar.urls)),
    )

 

