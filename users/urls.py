from django.urls import path , include
from .views import common , client , shareek
from rest_framework_simplejwt import views as jwt_views


ShareekPatterns = [
    path('sign-up/' , shareek.ShareekSignUpView.as_view() , name="login"),
    path('register-shareek/' , shareek.ShareekRegisterView.as_view() , name="register-shareek"),
    path('login/' , common.LoginView.as_view() , name="login"),
    path('logout/' , common.LogoutView.as_view() , name="logout"), 
    path('token/refresh/' , jwt_views.TokenRefreshView.as_view() , name='token-refresh'),
    path('forget-password-otp/' , common.ForgetPasswordOTPView.as_view() , name="forget-password-otp"),
    path('signup-otp/' , common.SignUpOTPView.as_view() , name="signup-otp"),
    # path('reset-password-otp/' , common.ResetPasswordOTPView.as_view() , name="reset-password-otp"),
    path('verify-otp/' , common.OTPVerificationView.as_view() , name="verify-otp"),
    path('reset-password/' , common.ResetPasswordView.as_view() , name="reset-password"),
]


ClientPatterns = [
    path('sign-up/' , client.ClientSignUpView.as_view() , name="client-sign-up"),
    path('login/' , common.LoginView.as_view() , name="login"),
    path('logout/' , common.LogoutView.as_view() , name="logout"),
    path('token/refresh/' , jwt_views.TokenRefreshView.as_view() , name='token-refresh'),
    path('forget-password-otp/' , common.ForgetPasswordOTPView.as_view() , name="forget-password-otp"),
    path('signup-otp/' , common.SignUpOTPView.as_view() , name="signup-otp"),
    # path('reset-password-otp/' , views.ResetPasswordOTPView.as_view() , name="reset-password-otp"),
    path('verify-otp/' , common.OTPVerificationView.as_view() , name="verify-otp"),
    path('reset-password/' , common.ResetPasswordView.as_view() , name="reset-password"),
]


urlpatterns = [
    path('shareek/' , include(ShareekPatterns)),
    path('client/' , include(ClientPatterns)),
]
