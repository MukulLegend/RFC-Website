from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from MBA import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz/", views.healthz, name="healthz"),

    # public site
    path("", views.Home, name="home"),
    path("home/", views.Home),
    path("about/", views.About, name="about"),
    path("squad/", views.squad, name="squad"),
    path("matches/", views.matches, name="matches"),
    path("news/", views.news, name="news"),
    path("contact/", views.contact_view, name="contact"),

    # accounts
    path("login/", views.Login1, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("change-password/", views.change_password, name="change_password"),

    # secure, email-based password reset (replaces the old username-only reset)
    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name="password_reset.html",
        email_template_name="password_reset_email.txt",
        subject_template_name="password_reset_subject.txt",
        success_url=reverse_lazy("password_reset_done")), name="password_reset"),
    path("password-reset/sent/", auth_views.PasswordResetDoneView.as_view(
        template_name="password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset_confirm.html",
        success_url=reverse_lazy("password_reset_complete")), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="password_reset_complete.html"), name="password_reset_complete"),

    # AI chat (members only)
    path("chat/", views.chat, name="chat"),
    path("chat-api/", views.chat_api, name="chat_api"),
]
