from django.urls import include, path
from django.contrib.auth import views as auth_views

from .views import (
        AddFieldView, CustomFormView,
        delete_field,
)

app_name = 'custom_form'

urlpatterns = [
    path('', AddFieldView.as_view(), name='add_field'),
    path('deletefield/<str:field>', delete_field, name='delete_field'),
    path('customform', CustomFormView.as_view(), name='form'),
]


