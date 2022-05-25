from datetime import date
from django.views.generic import TemplateView, ListView, UpdateView
from django.shortcuts import reverse

from carrentapp.models import Order


class EmployeeHomeView(TemplateView):
    template_name = 'employee/employee_home_page.html'


class PastDueListView(ListView):
    model = Order
    template_name = 'employee/employee_past_due_list.html'

    def get_queryset(self):
        orders = Order.objects.filter(return_date__lt=date.today(), status='Aktywny').order_by('issue_resolved')
        return orders


class PastDueDetailView(UpdateView):
    model = Order
    fields = ['issue_resolved', ]
    template_name = 'employee/employee_order_detail.html'

    def get_success_url(self):
        return reverse('past_due')
