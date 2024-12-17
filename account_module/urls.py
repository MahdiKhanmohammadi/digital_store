from django.urls import path
from . import views


urlpatterns = [
    path('register',views.RegisterView.as_view(),name='register'),
    path('login',views.LoginView.as_view(),name='login'),
    path('logout',views.log_out,name='logout'),
    path('forgot-password',views.ForgotPasswordView.as_view(),name='forgot_password'),
    path('change-password/<verify_code>',views.ChangePasswordView.as_view(),name='change_password'),
    path("active-account/<verify_code>",views.ActiveAccountView.as_view(),name='active-account'),
]