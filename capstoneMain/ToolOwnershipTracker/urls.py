from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import include

import base
from ToolOwnershipTracker.views import Profile, Login, PasswordReset, PasswordResetSent, PasswordResetForm, PasswordResetDone, SignUp, Jobsites, editUsers, createJobsite, editJobsite

urlpatterns = [
    path('', include('pwa.urls')),
    path('admin/', admin.site.urls),
    path('profile/', Profile.as_view()),
    path('password_reset/', PasswordReset.as_view(), name='password-reset'),
    path('password_reset_sent/', PasswordResetSent.as_view(),
         name='password_reset_sent'),
    path('password_reset_form/<str:token>/',
         PasswordResetForm.as_view(), name='password_reset_form'),
    path('password_reset_done/', PasswordResetDone.as_view(),
         name='password_reset_done'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('jobsites/', Jobsites.as_view(), name='jobsites'),
    path('createJobsite/', createJobsite.as_view(), name='createJobsite'),
    path('editJobsite/', editJobsite.as_view(), name='editJobsite'),
    path('edituser/', editUsers.as_view(), name="edituser"),
    path('', Login.as_view(), name='LoginHTML'),
]
