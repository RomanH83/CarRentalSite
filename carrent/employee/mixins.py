from django.contrib.auth.mixins import UserPassesTestMixin


class StaffStatusRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        obj = self.request.user
        return obj.is_staff is True
