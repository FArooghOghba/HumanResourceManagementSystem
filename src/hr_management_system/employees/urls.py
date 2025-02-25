from django.urls import path

from src.hr_management_system.employees.views import EmployeeAPIView


app_label = 'employees'


urlpatterns = [
    path(route='detail/', view=EmployeeAPIView.as_view(), name='create'),
]