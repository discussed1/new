from django.urls import path
from allauth.account import views as allauth_views
from .auth_views import LoginView, SignupView, PasswordResetView

urlpatterns = [
    # Override the login, signup, and password reset views with our custom views
    path("login/", LoginView.as_view(), name="account_login"),
    path("signup/", SignupView.as_view(), name="account_signup"),
    path("password/reset/", PasswordResetView.as_view(), name="account_reset_password"),
    
    # Include the rest of the allauth views as-is
    path("logout/", allauth_views.LogoutView.as_view(), name="account_logout"),
    path("password/change/", allauth_views.PasswordChangeView.as_view(), name="account_change_password"),
    path("password/set/", allauth_views.PasswordSetView.as_view(), name="account_set_password"),
    path("confirm-email/", allauth_views.EmailVerificationSentView.as_view(), name="account_email_verification_sent"),
    path("confirm-email/<str:key>/", allauth_views.ConfirmEmailView.as_view(), name="account_confirm_email"),
    path("password/reset/done/", allauth_views.PasswordResetDoneView.as_view(), name="account_reset_password_done"),
    path("password/reset/key/<str:uidb36>/<str:key>/", allauth_views.PasswordResetFromKeyView.as_view(), name="account_reset_password_from_key"),
    path("password/reset/key/done/", allauth_views.PasswordResetFromKeyDoneView.as_view(), name="account_reset_password_from_key_done"),
]