from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, logout
from django.utils.crypto import get_random_string
from .forms import RegisterForm, LoginForm, ForgotPasswordForm, ChangePasswordForm
from .models import User
from utils.emailService import send_email
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from datetime import datetime
# Create your views here.


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'account_module/register.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():

            get_email = form.cleaned_data.get('email')

            email_exist = User.objects.filter(email__iexact=get_email).exists()

            if email_exist:
                form.add_error('email', "ایمیل وارد شده تکراری است.")
            else:
                new_user = User(email=get_email, username=get_email, verify_code=get_random_string(
                    72), phone=None, address=None, is_active=False)

                get_password = form.cleaned_data.get('password')

                new_user.set_password(get_password)

                new_user.save()

                send_email('email/active_account.html', new_user.email,
                           {'verfiy_code': new_user.verify_code}, 'active account')

                return redirect(reverse('login'))

        context = {'form': form}
        return render(request, 'account_module/register.html', context)


class ActiveAccountView(View):
    def get(self, request, verify_code):

        find_user = get_object_or_404(User, verify_code=verify_code)
        find_user.is_active = True
        find_user.save()

        return redirect(reverse('login'))


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {'form': form}
        return render(request, 'account_module/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            get_email = form.cleaned_data.get('email')

            get_user = User.objects.filter(
                email=get_email, is_active=True).first()

            if get_user:

                get_password = form.cleaned_data.get('password')

                if User.check_password(get_user, get_password):
                    login(request, get_user)

                    get_user.last_login = datetime.now()

                    get_user.save()

                    return HttpResponse('200')
                else:
                    form.add_error('email', "نام کاربری یا رمزعبور اشتباه است")
            else:
                form.add_error('email', "نام کاربری یا رمزعبور اشتباه است")

        context = {'form': form}
        return render(request, 'account_module/login.html', context)


def log_out(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
        return redirect(reverse('home'))

    else:
        return HttpResponseNotFound()


class ForgotPasswordView(View):
    def get(self, request):
        form = ForgotPasswordForm()
        context = {"form": form}
        return render(request, 'account_module/forgot_password.html', context)

    def post(self, request):
        form = ForgotPasswordForm(request.POST)

        if form.is_valid():

            get_email = form.cleaned_data.get('email')

            user_exist = User.objects.filter(email=get_email).first()

            if user_exist:

                user_exist.verify_code = get_random_string(72)

                user_exist.save()

                send_email('email/reset_password.html', get_email,
                           {'verfiy_code': user_exist.verify_code}, "تغییر رمز عبور")

                return redirect(reverse('login'))
            else:
                form.add_error('email', 'ایمیل وجود ندارد')

        context = {'form': form}

        return render(request, 'account_module/forgot_password.html', context)


class ChangePasswordView(View):

    def get(self, request, **kwargs):

        get_code = kwargs['verify_code']

        get_object_or_404(User, verify_code=get_code)

        form = ChangePasswordForm()

        context = {'form': form}
        return render(request, 'account_module/change_password.html', context)

    def post(self, request, **kwargs):

        form = ChangePasswordForm(request.POST)

        if form.is_valid():

            get_code = kwargs['verify_code']

            find_user = get_object_or_404(User, verify_code=get_code)

            get_new_password = form.cleaned_data.get('password')

            find_user.set_password(get_new_password)

            find_user.verify_code = get_random_string(72)

            find_user.is_active = True

            find_user.save()

            return redirect(reverse('login'))

        context = {'form': form}
        return render(request, 'account_module/change_password.html', context)

