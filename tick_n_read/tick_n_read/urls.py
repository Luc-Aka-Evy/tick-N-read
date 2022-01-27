"""tick_n_read URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.conf import settings
import authentication.views
import review.views
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        LoginView.as_view(
            template_name="authentication/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "change-password/",
        PasswordChangeView.as_view(template_name="authentication/change_password.html"),
        name="change-password",
    ),
    path(
        "change-password-done/",
        PasswordChangeDoneView.as_view(
            template_name="authentication/change_password_done.html"
        ),
        name="change-password-done",
    ),
    path("signup/", authentication.views.signup_page, name="signup"),
    path("home/", review.views.home, name="home"),
    path("my-posts/", review.views.home_posts, name="my-posts"),
    path("ticket/create/", review.views.post_ticket, name="create-ticket"),
    path("ticket/<int:ticket_id>", review.views.view_ticket, name="view-ticket"),
    path("ticket/<int:ticket_id>/edit", review.views.edit_ticket, name="edit-ticket"),
    path("review/create/", review.views.post_review, name="create-review"),
    path("review/<int:review_id>", review.views.view_review, name="view-review"),
    path("review/<int:review_id>/edit", review.views.edit_review, name="edit-review"),
    path(
        "review/<int:ticket_id>/add_review/",
        review.views.add_review_for_ticket,
        name="add-review",
    ),
    path("follow-users/", review.views.follow_users, name="follow_users"),
    path("unfollow/<int:user_id>", review.views.unfollow_users, name="unfollow"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
