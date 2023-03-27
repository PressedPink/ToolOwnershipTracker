from django.contrib import admin
from django.urls import path


import base
from ToolOwnershipTracker.views import Profile, Login, SignUp, EditUser
urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', Profile.as_view()),
    path('signup/', SignUp.as_view()),
    path('edituser/', EditUser.as_view()),
    path('', Login.as_view(), name='LoginHTML'),
]
