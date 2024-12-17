from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):

    email = forms.CharField(label='ایمیل', widget=forms.EmailInput(
        attrs={'class': 'form-control form-control-lg'}
    ),
        validators=[
        validators.EmailValidator(),
        validators.MaxLengthValidator(120)

    ]
    )

    password = forms.CharField(label='رمزعبور', widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-lg'}),
        validators=[
            validators.MinLengthValidator(4),
            validators.MaxLengthValidator(32)
    ]
    )

    confirm_password = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-lg'},),
        validators=[
            validators.MinLengthValidator(4),
            validators.MaxLengthValidator(32)
    ])


# cutome validate

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if (password == confirm_password):
            return confirm_password
        else:
            raise ValidationError("پسورد ها باهم مغایرت دارند.")


class LoginForm(forms.Form):

    email = forms.CharField(label='ایمیل', widget=forms.EmailInput(
        attrs={'class': "form-control form-control-lg", 'id': "typeEmailX"}
    ),
        validators=[
        validators.EmailValidator(),
        validators.MaxLengthValidator(120)

    ]
    )

    password = forms.CharField(label='رمزعبور', widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-lg', 'id': "typePasswordX"}),
        validators=[
            validators.MinLengthValidator(4),
            validators.MaxLengthValidator(32)
    ]
    )


class ForgotPasswordForm(forms.Form):

    email = forms.CharField(label='ایمیل', widget=forms.EmailInput(
        attrs={'class': "form-control my-3", 'id': "typeEmail"}
    ),
        validators=[
        validators.EmailValidator(),
        validators.MaxLengthValidator(120)

    ]
    )


class ChangePasswordForm(forms.Form):

    password = forms.CharField(label='رمزعبور', widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-lg'}),
        validators=[
            validators.MinLengthValidator(4),
            validators.MaxLengthValidator(32)
    ]
    )

    confirm_password = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-lg'},),
        validators=[
            validators.MinLengthValidator(4),
            validators.MaxLengthValidator(32)
    ])


# cutome validate

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if (password == confirm_password):
            return confirm_password
        else:
            raise ValidationError("پسورد ها باهم مغایرت دارند.")
