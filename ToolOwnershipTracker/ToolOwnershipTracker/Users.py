import uuid

from django.forms import models

from ToolOwnershipTracker.base.models import user


class User():
    def createUser(self, firstName, lastName, email, role, password):
        if email is None:
            raise Exception("Unique Email Required")
        test = list(map(str, user.objects.filter(email=email)))
        if test.length != 0:
            raise Exception("User already exists")