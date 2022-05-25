from django.urls import path
from django.views.generic import TemplateView

from employee.views import EmployeeHomeView, PastDueListView, PastDueDetailView

urlpatterns = [
    path('', EmployeeHomeView.as_view(), name='employee_main'),
    path('past-due/', PastDueListView.as_view(), name='past_due'),
    path('past-due-detail/<int:pk>', PastDueDetailView.as_view(), name='past_due_detail'),
]