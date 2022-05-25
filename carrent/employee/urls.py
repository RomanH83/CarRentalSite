from django.urls import path
from django.views.generic import TemplateView

from employee.views import EmployeeHomeView, PastDueListView, PastDueDetailView, CarReturnListView, CarReturnDetailView

urlpatterns = [
    path('', EmployeeHomeView.as_view(), name='employee_main'),
    path('past-due/', PastDueListView.as_view(), name='past_due'),
    path('past-due-detail/<int:pk>', PastDueDetailView.as_view(), name='past_due_detail'),
    path('car-return', CarReturnListView.as_view(), name='car_return'),
    path('car-return-detail/<int:pk>', CarReturnDetailView.as_view(), name='car_return_detail')
]