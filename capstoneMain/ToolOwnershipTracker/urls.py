from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views


import base
from ToolOwnershipTracker.views import Profile, Login, PasswordReset, PasswordResetSent, PasswordResetForm, PasswordResetDone

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', Profile.as_view()),    
    path('password_reset/', PasswordReset.as_view()),
    path('password_reset_sent/', PasswordResetSent.as_view()),
    path('password_reset_form/<token>/', PasswordResetForm.as_view()),
    path('password_reset_done/', PasswordResetDone.as_view()),

    path('', Login.as_view(), name='LoginHTML'),
]
