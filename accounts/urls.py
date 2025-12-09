from django.urls import path
from .views import *

urlpatterns = [
    path('register/phone/', RegisterView.as_view(), name='register-phone'),
    path('register/email/', EmailRegisterView.as_view(), name='register-email'),
    path('login/phone/', LoginView.as_view(), name='login-phone'),    
    path('login/email/', EmailLoginView.as_view(), name='login-email'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('send-reset-code/', SendResetCodeView.as_view(), name='send-reset-code'),
    # path('verify-reset-code/', VerifyResetCodeView.as_view(), name='verify-reset-code'),
    # path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]

