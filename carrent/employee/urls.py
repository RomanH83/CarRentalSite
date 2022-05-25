from django.urls import path
from django.views.generic import TemplateView

from employee.views import EmployeeHomeView

urlpatterns = [
    path('', EmployeeHomeView.as_view(template_name='employee/employee_home_page.html'), name='employee_main'),
]