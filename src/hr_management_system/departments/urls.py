from django.urls import path

from src.hr_management_system.departments.apis import DepartmentDetailAPIView, DepartmentListAPIView


app_label = 'departments'


urlpatterns = [
    path(route='', view=DepartmentListAPIView.as_view(), name='list'),
    path(route='detail/', view=DepartmentDetailAPIView.as_view(), name='create'),
]