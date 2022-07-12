from datetime import date

import django_filters
from django.shortcuts import reverse, redirect
from django.views.generic import TemplateView, ListView, UpdateView

from carrentapp.models import Order
from carrentapp.enums import OrderStatus
from employee.mixins import StaffStatusRequiredMixin
from employee.validators import new_mileage_validator, status_check


class EmployeeHomeView(StaffStatusRequiredMixin, TemplateView):
    template_name = 'employee/employee_home_page.html'


class PastDueListView(StaffStatusRequiredMixin, ListView):
    model = Order
    template_name = 'employee/employee_past_due_list.html'

    def get_queryset(self):
        orders = Order.objects.filter(return_date__lt=date.today(), status=OrderStatus.AKTYWNY).order_by('issue_resolved')
        return orders


class PastDueDetailView(StaffStatusRequiredMixin, UpdateView):
    model = Order
    fields = ['issue_resolved', 'status', 'kilometers_traveled']
    template_name = 'employee/employee_order_detail.html'

    def get_success_url(self):
        return reverse('past_due')

    def form_valid(self, form):
        objct = form.save(commit=False)
        order = Order.objects.get(id=self.kwargs['pk'])
        car = order.car
        old_mileage = car.car_mileage
        new_mileage = int(self.request.POST.get('kilometers_traveled'))
        errors = new_mileage_validator(new_mileage, old_mileage)
        if errors:
            return redirect('past_due_detail_msg', pk=self.kwargs['pk'], msg=errors)
        car.car_mileage = new_mileage
        car.save()
        objct.kilometers_traveled = new_mileage - old_mileage
        objct.save()
        return redirect("past_due")

    def get_initial(self):
        order = Order.objects.get(id=self.kwargs['pk'])
        initial = super().get_initial()
        initial = initial.copy()
        initial['status'] = order.status
        initial['issue_resolved'] = order.issue_resolved
        initial['kilometers_traveled'] = order.car.car_mileage
        return initial


class OrderFilter(django_filters.FilterSet):

    class Meta:
        model = Order
        fields = ['client']


class CarReturnListView(StaffStatusRequiredMixin, ListView):
    model = Order
    template_name = 'employee/employee_car_return.html'

    def get_queryset(self):
        orders = Order.objects.filter(return_date=date.today(), status=OrderStatus.AKTYWNY)
        return orders

    def get_context_data(self, **kwargs):
        fltr = OrderFilter(self.request.GET, queryset=self.get_queryset())
        fltr_dict = {'filter': fltr}
        kwargs.setdefault('view', self)
        kwargs.update(fltr_dict)
        return kwargs


# class CarListView(FilterView):
#     model = Car
#     template_name = 'carrentapp/car_list.html'
#     filterset_class = CarFilter


class CarReturnDetailView(StaffStatusRequiredMixin, UpdateView):
    model = Order
    fields = ['status', 'kilometers_traveled']
    template_name = 'employee/employee_car_return_detail.html'

    def get_success_url(self):
        return reverse('car_return')

    def form_valid(self, form):
        objct = form.save(commit=False)
        order = Order.objects.get(id=self.kwargs['pk'])
        car = order.car
        old_mileage = car.car_mileage
        new_mileage = int(self.request.POST.get('kilometers_traveled'))

        errors = new_mileage_validator(new_mileage, old_mileage)
        if errors:
            return redirect('car_return_detail_msg', pk=self.kwargs['pk'], msg=errors)

        status = self.request.POST.get('status')
        errors = status_check(status)
        if errors:
            return redirect('car_return_detail_msg', pk=self.kwargs['pk'], msg=errors)

        car.car_mileage = new_mileage
        car.save()
        objct.kilometers_traveled = new_mileage - old_mileage
        objct.save()
        return redirect("car_return")
