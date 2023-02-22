from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

import base
from ToolOwnershipTracker.views import Profile
urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', Profile.as_view()),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), name="password_reset_complete"),
    

]
