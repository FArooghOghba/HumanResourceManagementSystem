from django.urls import path

from src.hr_management_system.departments.apis import (
    DepartmentDetailAPIView, DepartmentListAPIView,
    PositionDetailAPIView, PositionListAPIView
)


app_label = 'departments'


urlpatterns = [
    path(route='', view=DepartmentListAPIView.as_view(), name='list'),
    path(route='detail/', view=DepartmentDetailAPIView.as_view(), name='detail'),
    path(route='positions/', view=PositionListAPIView.as_view(), name='positions-list'),
    path(route='positions/detail/', view=PositionDetailAPIView.as_view(), name='positions-detail'),
]
