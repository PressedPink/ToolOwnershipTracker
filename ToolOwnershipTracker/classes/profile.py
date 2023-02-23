from base.models import User

# Used for booleans.
class Profile:
    def __init__(self, username):
        self.username = username

    # Checks if there is a user with the same username. Returns T/F
    def duplicateUserCheck(self):
        return User.objects.filter(username=self.username).exists()

    # If no duplicated user, creates a new user object and returns true, otherwise returns false.
    def createUser(self, password, accountType, email, phone, address):
        if not self.duplicateUserCheck():
            User.objects.create(username=self.username, password=password, accountType=accountType, email=email,
                                phone=phone, address=address)
            return True
        else:
            return False