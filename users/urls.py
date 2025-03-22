from django.urls import path , include
from .views import common , client , shareek
from rest_framework_simplejwt import views as jwt_views


ShareekPatterns = [
    path('sign-up/' , shareek.ShareekSignUpView.as_view()),
    path('register-shareek/' , shareek.ShareekRegisterView.as_view()),
    path('login/' , common.ShareekLoginView.as_view()),
    path('logout/' , common.LogoutView.as_view()), 
    path('token/refresh/' , common.RefreshTokenView.as_view()),
    path('refresh-firebase-token/' , common.RefreshFirebaseToken.as_view()),
    path('forget-password-otp/' , common.ForgetPasswordOTPView.as_view()),
    path('reset-password-otp/' , common.ResetPasswordOTPView.as_view()),
    path('signup-otp/' , common.SignUpOTPView.as_view()),
    path('verify-otp/' , common.OTPVerificationView.as_view()),
    path('reset-password/<str:user_id>/' , common.ResetPasswordView.as_view()),
    path('change-password/' , common.ChangePasswordView.as_view()),
    path('update/<int:pk>/' , shareek.UpdateShareekView.as_view()),
    path('info/<int:id>/' , shareek.ShareekInfoView.as_view()),
    path('delete/' , shareek.DeleteShareekView.as_view()),
    path('location/<int:user_id>/' , common.UpdateLocationView.as_view()),
    path('notifications/' , common.NotificationsView.as_view()),
    path('activate-notifications/<int:user_id>/' , common.ActivateNotificationsView.as_view()),
]


ClientPatterns = [
    path('sign-up/' , client.ClientSignUpView.as_view()),
    path('login/' , common.ClientLoginView.as_view()),
    path('logout/' , common.LogoutView.as_view()),
    path('token/refresh/' , jwt_views.TokenRefreshView.as_view()),
    path('refresh-firebase-token/' , common.RefreshFirebaseToken.as_view()),
    path('forget-password-otp/' , common.ForgetPasswordOTPView.as_view()),
    path('reset-password-otp/' , common.ResetPasswordOTPView.as_view()),
    path('signup-otp/' , common.SignUpOTPView.as_view()),
    path('verify-otp/' , common.OTPVerificationView.as_view()),
    path('reset-password/<str:user_id>/' , common.ResetPasswordView.as_view()),
    path('change-password/' , common.ChangePasswordView.as_view()),
    path('update/<int:pk>/' , client.UpdateClientView.as_view()),
    path('delete/' , client.DeleteClientView.as_view()),
    path('location/<int:user_id>/' , common.UpdateLocationView.as_view()),
    path('notifications/' , common.NotificationsView.as_view()),
    path('activate-notifications/<int:user_id>/' , common.ActivateNotificationsView.as_view()),
]


urlpatterns = [
    path('shareek/' , include(ShareekPatterns)),
    path('client/' , include(ClientPatterns)),
]
