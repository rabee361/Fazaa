from django.urls import path , include
from .views import common , client , shareek
from rest_framework_simplejwt import views as jwt_views


ShareekPatterns = [
    path('sign-up/' , shareek.ShareekSignUpView.as_view()),
    path('register-shareek/' , shareek.ShareekRegisterView.as_view()),
    path('login/' , common.LoginView.as_view()),
    path('logout/' , common.LogoutView.as_view()), 
    path('token/refresh/' , jwt_views.TokenRefreshView.as_view()),
    path('forget-password-otp/' , common.ForgetPasswordOTPView.as_view()),
    path('signup-otp/' , common.SignUpOTPView.as_view()),
    # path('reset-password-otp/' , common.ResetPasswordOTPView.as_view() , name="reset-password-otp"),
    path('verify-otp/' , common.OTPVerificationView.as_view()),
    path('reset-password/' , common.ResetPasswordView.as_view()),
]


ClientPatterns = [
    path('sign-up/' , client.ClientSignUpView.as_view()),
    path('login/' , common.LoginView.as_view()),
    path('logout/' , common.LogoutView.as_view()),
    path('token/refresh/' , jwt_views.TokenRefreshView.as_view()),
    path('forget-password-otp/' , common.ForgetPasswordOTPView.as_view()),
    path('signup-otp/' , common.SignUpOTPView.as_view()),
    # path('reset-password-otp/' , views.ResetPasswordOTPView.as_view() , name="reset-password-otp"),
    path('verify-otp/' , common.OTPVerificationView.as_view()),
    path('reset-password/' , common.ResetPasswordView.as_view()),
]


urlpatterns = [
    path('shareek/' , include(ShareekPatterns)),
    path('client/' , include(ClientPatterns)),
]
