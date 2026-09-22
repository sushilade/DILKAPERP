from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.user_login, name="login"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("college/", views.college_profile, name="college_profile"),
    path("college/add/", views.add_college, name="add_college"),
    path("college/edit/<int:college_id>/", views.edit_college, name="edit_college"),
    path("college/delete/<int:college_id>/", views.delete_college, name="delete_college"),
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="password_reset.html"), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="password_reset_complete.html"), name="password_reset_complete"),
]
