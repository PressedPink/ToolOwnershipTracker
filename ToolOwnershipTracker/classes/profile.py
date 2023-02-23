from base.models import User

# Used for booleans.
class Profile:
    def __init__(self, email):
        self.email = email

    def editUser(self, password, phone, address):
        User.objects.filter(email=self.email).update(password=password,phone=phone,address=address)
        return True
