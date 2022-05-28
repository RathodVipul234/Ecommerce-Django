from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm,SetPasswordForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout


class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
        self.fields['email'].required = True,
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exist please try again with different email")
        return self.cleaned_data


class LoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })


class CustomerPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(required=True, label='old_password',
                                   widget=forms.PasswordInput(attrs={
                                       'placeholder': 'Current password',
                                       'class': 'form-control',
                                   })
                                   )

    new_password1 = forms.CharField(required=True, label='new_password1',
                                    widget=forms.PasswordInput(attrs={
                                        'placeholder': 'New password',
                                        'class': 'form-control',
                                    })
                                    )

    new_password2 = forms.CharField(required=True, label='new_password2',
                                    widget=forms.PasswordInput(attrs={
                                        'placeholder': 'Confirm new password',
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
