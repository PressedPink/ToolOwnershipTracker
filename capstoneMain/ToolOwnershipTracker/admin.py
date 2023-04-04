from django.contrib import admin
from .models import User, Jobsite, Tool, Toolbox
# Register your models here.

admin.site.register(User)
admin.site.register(Jobsite)
admin.site.register(Tool)
admin.site.register(Toolbox)
