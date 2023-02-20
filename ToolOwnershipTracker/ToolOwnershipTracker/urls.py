from django.contrib import admin
from django.urls import path

import base
from base.views import Profile
urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', Profile.as_view()),
]
