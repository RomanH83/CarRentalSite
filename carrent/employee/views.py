from datetime import date

import django_filters
from django.core.exceptions import ImproperlyConfigured
from django.forms import modelform_factory
from django.shortcuts import reverse, redirect
from django.views.generic import TemplateView, ListView, UpdateView

from carrentapp.models import Order
from carrentapp.enums import OrderStatus
from employee.mixins import StaffStatusRequiredMixin
from employee.validators import new_mileage_validator, status_check
from employee.forms import CarReturnForm, IssueResolvedForm

class EmployeeHomeView(StaffStatusRequiredMixin, TemplateView):
    template_name = 'employee/employee_home_page.html'


class PastDueListView(StaffStatusRequiredMixin, ListView):
    model = Order
    template_name = 'employee/employee_past_due_list.html'
    paginate_by = 10

    def get_queryset(self):
        orders = Order.objects.filter(return_date__lt=date.today(), status=OrderStatus.AKTYWNY).order_by('issue_resolved')
        return orders


class PastDueDetailView(StaffStatusRequiredMixin, UpdateView):
    model = Order
    template_name = 'employee/employee_order_detail.html'

    # this view requires 2 forms and cannot be used with fields
    form_class = IssueResolvedForm
    form_class_2 = CarReturnForm

    def get_form_class(self):
        order = Order.objects.get(id=self.kwargs['pk'])
        """Return the form class to use in this view."""
        if self.fields is not None and self.form_class:
            raise ImproperlyConfigured(
                "Specifying both 'fields' and 'form_class' is not permitted."
            )
        if self.form_class and order.issue_resolved is not True:
            return self.form_class
        elif self.form_class:
            return self.form_class_2

    def get_success_url(self):
        return reverse('past_due')

    def form_valid(self, form):
        objct = form.save(commit=False)
        order = Order.objects.get(id=self.kwargs['pk'])

        if order.issue_resolved is True:
            car = order.car
            old_mileage = car.car_mileage
            new_mileage = int(self.request.POST.get('kilometers_traveled'))
            errors = new_mileage_validator(new_mileage, old_mileage)
            if errors:
                return redirect('past_due_detail_msg', pk=self.kwargs['pk'], msg=errors)
            errors = status_check(self.request.POST.get('status'))
            if errors:
                return redirect('past_due_detail_msg', pk=self.kwargs['pk'], msg=errors)
            car.car_mileage = new_mileage
            car.save()
            objct.kilometers_traveled = new_mileage - old_mileage

        objct.save()
        return redirect("past_due")

    # def get_initial(self):
    #     order = Order.objects.get(id=self.kwargs['pk'])
    #     initial = super().get_initial()
    #     initial = initial.copy()
    #     initial['status'] = order.status
    #     initial['issue_resolved'] = order.issue_resolved
    #     initial['kilometers_traveled'] = order.car.car_mileage
    #     return initial


class OrderFilter(django_filters.FilterSet):

    class Meta:
        model = Order
        fields = ['client']


class CarReturnListView(StaffStatusRequiredMixin, ListView):
    model = Order
    template_name = 'employee/employee_car_return.html'
    paginate_by = 10

    def get_queryset(self):
        orders = Order.objects.filter(return_date=date.today(), status=OrderStatus.AKTYWNY)
        return orders

    def get_context_data(self, **kwargs):
        fltr = OrderFilter(self.request.GET, queryset=self.get_queryset())
        fltr_dict = {'filter': fltr}

        page_size = self.get_paginate_by(fltr.qs)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(
                fltr.qs, page_size
            )
            context = {
                "paginator": paginator,
                "page_obj": page,
                "is_paginated": is_paginated,
                "object_list": queryset,
            }
        else:
            context = {
                "paginator": None,
                "page_obj": None,
                "is_paginated": False,
                "object_list": fltr.qs,
            }

        _request_copy = self.request.GET.copy()
        parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
        context['parameters'] = parameters

        kwargs.setdefault('view', self)
        kwargs.update(fltr_dict)
        kwargs.update(context)
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
