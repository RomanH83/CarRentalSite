from datetime import date
from django.views.generic import TemplateView, ListView, UpdateView
from django.shortcuts import reverse

from carrentapp.models import Order
from employee.mixins import StaffStatusRequiredMixin


class EmployeeHomeView(StaffStatusRequiredMixin, TemplateView):
    template_name = 'employee/employee_home_page.html'


class PastDueListView(StaffStatusRequiredMixin, ListView):
    model = Order
    template_name = 'employee/employee_past_due_list.html'

    def get_queryset(self):
        orders = Order.objects.filter(return_date__lt=date.today(), status='Aktywny').order_by('issue_resolved')
        return orders


class PastDueDetailView(StaffStatusRequiredMixin, UpdateView):
    model = Order
    fields = ['issue_resolved', 'status', 'kilometers_traveled']
    template_name = 'employee/employee_order_detail.html'

    def get_success_url(self):
        return reverse('past_due')


class CarReturnListView(StaffStatusRequiredMixin, ListView):
    model = Order
    template_name = 'employee/employee_car_return.html'

    def get_queryset(self):
        orders = Order.objects.filter(return_date=date.today(), status="Aktywny")
        return orders


class CarReturnDetailView(StaffStatusRequiredMixin, UpdateView):
    model = Order
    fields = ['status']
    template_name = 'employee/employee_car_return_detail.html'

    def get_success_url(self):
        return reverse('car_return')
