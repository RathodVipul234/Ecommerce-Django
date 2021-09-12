from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm,SetPasswordForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _
from .models import Customer
# from django.forms import forms
from django import forms
from .models import STATE_CHOICE


class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'username'
        })
        self.fields['email'].required = True,
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'email',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'confirm password (Again)'
        })

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exist please try again with different Email")
        return self.cleaned_data


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __str__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'username'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'password'
        })


class CustomerPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(required=True, label='old_password',
                                   widget=forms.PasswordInput(attrs={
                                       'placeholder': 'current password',
                                       'class': 'form-control',
                                   })
                                   )

    new_password1 = forms.CharField(required=True, label='new_password1',
                                    widget=forms.PasswordInput(attrs={
                                        'placeholder': 'new password',
                                        'class': 'form-control',
                                    })
                                    )

    new_password2 = forms.CharField(required=True, label='new_password2',
                                    widget=forms.PasswordInput(attrs={
                                        'placeholder': 'confirm new password',
                                        'class': 'form-control',
                                    })
                                    )


class CustomerPasswordRestForm(PasswordResetForm):
    email = forms.CharField(required=True, label='Email',
                             widget=forms.EmailInput(attrs={
                                 'placeholder': 'Email',
                                 'class': 'form-control',
                             })
                             )
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email).exists():
            raise ValidationError("There is no user registered with the specified email address!")
        return email


class CustomerSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(required=True, label='new_password1',
                                    widget=forms.PasswordInput(attrs={
                                        'placeholder': 'new password',
                                        'class': 'form-control',
                                    })
                                )

    new_password2 = forms.CharField(required=True, label='new_password1',
                                    widget=forms.PasswordInput(attrs={
                                        'placeholder': 'new password',
                                        'class': 'form-control',
                                    })
                                )



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'zipcode']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'placeholder': 'name',
            'class': 'form-control',
        })
        self.fields['locality'].widget.attrs.update({
            'placeholder': 'address',
            'class': 'form-control',
        })
        self.fields['city'].widget.attrs.update({
            'placeholder': 'city',
            'class': 'form-control',
        })
        self.fields['state'].widget.select = STATE_CHOICE
        self.fields['state'].widget.attrs.update({
            'placeholder': 'state state',
            'class': 'form-control',
        })
        self.fields['zipcode'].widget.attrs.update({
            'placeholder': 'zipcode',
            'class': 'form-control',
        })
