from django.contrib.auth import views as auth_views
from django.urls import path

from .forms import LoginForm
from .views import CustomLoginView, RegisterView, ChangePasswordView, UpdateProfileUserView, ResetPasswordView, \
    ResetPasswordConfirmView, ResetPasswordSplashView, ResetPasswordFinishView

urlpatterns = [
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='accounts/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('registration/', RegisterView.as_view(), name='users-registration'),
    path('profile/', UpdateProfileUserView.as_view(), name='user-profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-splash', ResetPasswordSplashView.as_view(), name='password_reset_splash'),
    path('password-reset-confirm/<uidb64>/<token>', ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-finish', ResetPasswordFinishView.as_view(), name='password_reset_finish'),
]
