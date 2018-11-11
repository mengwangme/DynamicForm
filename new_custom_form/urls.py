from django.urls import path

from .views import (
        AddFieldView, CustomFormView,
        delete_field,
)

app_name = 'new_custom_form'

urlpatterns = [
    path('', AddFieldView.as_view(), name='add_field'),
    path('deletefield/<int:id>', delete_field, name='delete_field'),
    path('form/<str:form_name>', CustomFormView.as_view(), name='form'),
]


