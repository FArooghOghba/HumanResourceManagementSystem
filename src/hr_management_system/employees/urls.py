from django.urls import path

from src.hr_management_system.employees.apis import EmployeeDetailAPIView, EmployeeListAPIView


app_label = 'employees'


urlpatterns = [
    path(route='', view=EmployeeListAPIView.as_view(), name='list'),
    path(route='detail/', view=EmployeeDetailAPIView.as_view(), name='create'),
]