from base.models import User

# Used for booleans.
class Profile:
    def __init__(self, username):
        self.username = username
        
    def editUser(self, password, email, phone, address):
        toEdit = User.objects.get(username=self.username)
        toEdit = User.objects.update(password=password, email=email, phone=phone, address=address)
