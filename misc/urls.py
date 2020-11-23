from django.urls import path

from misc.views import ErrorsListView

urlpatterns = [
    path('errors/', ErrorsListView.as_view(), name='errors'),
]