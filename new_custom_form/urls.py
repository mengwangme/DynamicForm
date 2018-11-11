from django.urls import include, path
from django.contrib.auth import views as auth_views

from .views import (
        AddFieldView,
        delete_field, CustomFormView
)

app_name = 'new_custom_form'

urlpatterns = [
    path('', AddFieldView.as_view(), name='add_field'),
    path('deletefield/<int:id>', delete_field, name='delete_field'),
    # path('form/<str:form_name>', form, name='form'),
    # path('form/', form, name='form'),
    path('form/<str:form_name>', CustomFormView.as_view(), name='form'),
]


