from django.urls import path

from src.hr_management_system.payrolls.apis import PayrollDetailAPIView, PayrollListAPIView


app_label = 'payrolls'


urlpatterns = [
    path(route='detail/', view=PayrollDetailAPIView.as_view(), name='detail'),
    path(route='', view=PayrollListAPIView.as_view(), name='list'),
]