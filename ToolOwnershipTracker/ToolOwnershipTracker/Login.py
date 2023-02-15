import hashlib
from tkinter import INSERT

import signupForm as signupForm
import loginForm as loginForm
import mysql.connector
from numpy.core.defchararray import upper

form = signup.FormFieldStorage()


def login: ()


email = loginForm.getvalue('email')
pw = loginForm.getvalue('password')
auth = pw.encode()
auth_hash = hashlib.md5(auth).hexdigest()
if checkEmail(email) and auth_hash == checkPassword(auth_hash):
    clearSessions(email)
    user.active = true
    account_redirect(email)
else:
    print(“Login
    failed! \n”)

    def signup():
        active = false
        while (!active):
        first_name = signupForm.getvalue('first_name')
        last_name = signupForm.getvalue('last_name')
        email = signupForm.getvalue('email')
        pw = signupForm.getvalue('password')
        conf_pwd = signupForm.getvalue('conf_pwd')
        account_type = 0
        if (signupForm.getvalue('radio1') == true)):
            account_type = 1
        else if (signupForm.getvalue('radio2' == true)):
            account_type = 2
        else if (signupForm.getvalue('radio3' == true)):
            account_type = 3
        if (conf_pwd == pwd & !checkEmail(email)):
            enc = conf_pwd.encode()
        hash1 = hashlib.md5(enc).hexdigest()
        if account_type > 0:
            active = true
        addAccount(first_name, last_name, account_type, email, hash1, active)
        print("You have registered successfully!")
        account_redirect(email)
        else if checkEmail():
            print(
                "There is already a account using this email. Please verify your email or use the forgot password link \n")
        break

    else if (pw != conf_pwd):
        print("Passwords do not match!")
        break
        else:
            print("Account type not selected\n")


        def account_redirect(email):
            return redirect('account-landing', pk=email.user.pk, name=email.user.email)


        def checkEmail(email):

            mydb = mysql.connector.connect(
                host="localhost",
                user="yourusername",
                password="yourpassword",
                database="mydatabase"
            )

            mycursor = mydb.cursor()

            mycursor.execute("SELECT email FROM users")

            emails = mycursor.fetchall()

            for x in emails:
                if (upper(x) == upper(email)):
                    return true


        def checkPassword(pw):

            mydb = mysql.connector.connect(
                host="localhost",
                user="yourusername",
                password="yourpassword",
                database="mydatabase"
            )

            mycursor = mydb.cursor()

            mycursor.execute("SELECT email, password FROM users")

            accounts = mycursor.fetchall()
            passwords = mycursor

            for x in accounts:
                if (upper(x(0)) == upper(email)):
                    return x(1)

            return 0


        def addAccount(fn, ln, account_type, email, pw, active):

            createUser(fn, ln, account_type, email, pw, active)

            mydb = mysql.connector.connect(
                host="localhost",
                user="yourusername",
                password="yourpassword",
                database="mydatabase"
            )

            mycursor = mydb.cursor()

            mycursor.execute(
                INSERT INTO users(fn, ln, account_type, email, pw, active)
                VALUES
                (fn, ln, account_type, email, pw, active)
                mydb.commit()


        def clearSessions(email):
            #TODO


        def createUser(fn, ln, account_type, email, pw, active):
            #TODO