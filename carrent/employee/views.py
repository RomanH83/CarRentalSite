from django.shortcuts import render
from django.views.generic import TemplateView


class EmployeeHomeView(TemplateView):
    template_name = 'employee/employee_home_page.html'
