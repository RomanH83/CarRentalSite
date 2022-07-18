from django import forms

from carrentapp.models import Order
from carrentapp.enums import OrderStatus


class IssueResolvedForm(forms.ModelForm):
    issue_resolved = forms.NullBooleanField(required=True)

    class Meta:
        model = Order
        fields = ['issue_resolved']

class CarReturnForm(forms.ModelForm):
    status = forms.ChoiceField(choices=OrderStatus.choices, required=True)
    kilometers_traveled = forms.IntegerField(required=True)

    class Meta:
        model = Order
        fields = ['status', 'kilometers_traveled']