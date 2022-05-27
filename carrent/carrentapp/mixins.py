from django.contrib.auth.mixins import UserPassesTestMixin


class RestrictOwnerAccessMixin(UserPassesTestMixin):

    def test_func(self):
        obj = self.get_object()
        return obj.client == self.request.user
