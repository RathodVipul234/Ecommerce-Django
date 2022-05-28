import smtplib,os,sys
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend, UserModel
from django.contrib.auth.views import PasswordChangeView,PasswordResetView
from django.contrib.auth.models import User


from account.utils import LoginRequiredMixin
from django.views import View
from account.forms import (
    CustomerRegistrationForm,
    LoginForm,
    CustomerPasswordChangeForm,
    CustomerPasswordRestForm
)

# Create your views here.

class CustomBackend(ModelBackend):
    """
        - overiding default ModelBacked class for login user with
        username and Email Id both
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(
                Q(username__iexact=username) |
                Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None


class CustomerRegistration(View):
    """
        - on get method rendering default form of registation where user can fill up 
        their details and register to our site
        - on a  post method when user press submit button after fill up all valid
        details user data will be stored to data base
        - if form is invalid then user can see which data they enter wrong and fill up form again
    """
    def get(self, request):
        form_data = CustomerRegistrationForm()
        return render(request, 'core/customerregistration.html', {'form': form_data})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "you have successfully register!")
            return redirect('login')
        return render(request, 'core/customerregistration.html', {'form': form})


class CustomerLoginView(View):
    """
        - User login view with defult get and post function
        - on a get method login form will be rendered
        - on a post method login form will be submitted
    """
    form_class = LoginForm
    template_name = "core/login.html"
    def get(self, request, *args, **kwargs):
        context = {}
        context['form']=self.form_class
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        form =self.form_class(request.POST)
        context['form'] = form
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user'] = user.username
            messages.success(request, "logging successfully")
            return redirect('profile')
        else:
            if User.objects.filter(
                Q(username=username)|
                Q(email=username)
            ).exists():
                messages.error(request, "Please enter valid password!")
            else:
                messages.info(request, "User not found.")
            return render(request, self.template_name, context)


class ChangePassword(PasswordChangeView,LoginRequiredMixin):
    """
        - PasswordChangeView View
        - 
    """
    form_class = CustomerPasswordChangeForm
    template_name = 'core/changepassword.html'
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request,'password update successfully! please login again.')
        return redirect('login')


class ResetPassword(PasswordResetView):
    form_class = CustomerPasswordRestForm
    template_name = 'core/resetpassword.html'
    def form_valid(self, form):
        form.save()
        messages.success(self.request,'password reset link shared to your email please check')
        return redirect('home')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        return redirect('home')
