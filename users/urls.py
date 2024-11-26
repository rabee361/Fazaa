from django.urls import path , include
from . import views
from rest_framework_simplejwt import views as jwt_views


ShareekPatterns = [
    path('sign-up/' , views.ShareekSignUpView.as_view() , name="login"),
    path('register-shareek/' , views.ShareekRegisterView.as_view() , name="register-shareek"),
    path('login/' , views.LoginView.as_view() , name="login"),
    path('logout/' , views.LogoutView.as_view() , name="logout"), 
    path('token/refresh/' , jwt_views.TokenRefreshView.as_view() , name='token-refresh'),
    path('forget-password-otp/' , views.ForgetPasswordOTPView.as_view() , name="forget-password-otp"),
    # path('reset-password-otp/' , views.ResetPasswordOTPView.as_view() , name="reset-password-otp"),
    path('verify-otp/' , views.OTPVerificationView.as_view() , name="verify-otp"),
    path('reset-password/' , views.ResetPasswordView.as_view() , name="reset-password"),
]


ClientPatterns = [
    path('sign-up/' , views.ClientSignUpView.as_view() , name="client-sign-up"),
    path('login/' , views.LoginView.as_view() , name="login"),
    path('logout/' , views.LogoutView.as_view() , name="logout"),
    path('token/refresh/' , jwt_views.TokenRefreshView.as_view() , name='token-refresh'),
    path('forget-password-otp/' , views.ForgetPasswordOTPView.as_view() , name="forget-password-otp"),
    # path('reset-password-otp/' , views.ResetPasswordOTPView.as_view() , name="reset-password-otp"),
    path('verify-otp/' , views.OTPVerificationView.as_view() , name="verify-otp"),
    path('reset-password/' , views.ResetPasswordView.as_view() , name="reset-password"),
]


urlpatterns = [
    path('shareek/' , include(ShareekPatterns)),
    path('client/' , include(ClientPatterns)),
]
