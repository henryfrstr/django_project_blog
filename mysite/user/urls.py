from django.urls import path, include
from .views import profile, register, activate, profile_edit, PasswordChange, delete_user
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm, PwdChangeForm


urlpatterns = [
    # path('password_change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change_form.html',
    #                                                                form_class=PwdChangeForm), name='password_change'),
    path('password_change/', PasswordChange.as_view(), name='password_change'),
    path('password_change/', auth_views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'), name='password_change_done'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html',
                                                authentication_form=UserLoginForm), name='login'),
    path('delete/', delete_user, name='delete_user'),
    path('profile/', profile, name='profile'),
    path('profile-edit/', profile_edit, name='profile_edit'),
    path('register/', register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="users/password_reset.html"), name="reset_password"),
    path('reset_password_send/', auth_views.PasswordResetDoneView.as_view(
        template_name="users/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="users/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="users/password_reset_complete.html"), name="password_reset_complete"),
]
