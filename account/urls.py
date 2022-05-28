import django
from django.urls import path,include
from account import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, CustomerPasswordRestForm, CustomerSetPasswordForm

urlpatterns = [
        path('registration/', views.CustomerRegistration.as_view(), name='customerregistration'),
        path('login/', views.CustomerLoginView.as_view(), name='login'),
        path('logout/', views.LogoutView.as_view(), name='logout'),

        path('password-reset/', auth_views.PasswordResetView.as_view(
          template_name='core/password_reset.html',
          form_class=CustomerPasswordRestForm
        ), name='password_reset'),

        path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
          template_name='core/password_reset_done.html',
        ), name='password_reset_done'),

        path('accounts/password-reset/confirm/<uidb64>/<token>/',
           auth_views.PasswordResetConfirmView.as_view(
               template_name='core/password_reset_confirm.html',
               form_class=CustomerSetPasswordForm), name='password_reset_confirm'),

        path('password-reset-complete/', auth_views.
           PasswordResetCompleteView.as_view(
           template_name='core/password_reset_complete.html',
        ), name='password_reset_complete'),

        path('changePassword/', views.ChangePassword.as_view(), name='changepassword'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
