
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import codecs, json
from django.core import management
from Feas.settings import db
import datetime

import crypt



def index(request):

    return render(request, 'login/index.html')


def signin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        check_user = db.user.find_one({"email": email})
        # To check the password.

        if check_user is not None:
            valid_password = crypt.crypt(password, check_user["password"]) == check_user["password"]
            if valid_password:
                request.session['email'] = email

                return redirect("/home")
            else:
                return render(request, 'login/signin.html', {"error": "wrong password"})

        else:
            return render(request, 'login/index.html', {"error": "User does not exists"})

    return render(request, 'login/index.html')

    return render(request, 'login/index.html')


@csrf_exempt
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        # To encrypt the password.
        password = crypt.crypt(password)
        check_email = db.user.find_one({"email": email})
        check_username = db.user.find_one({"username": username})
        print(check_username)
        if check_email is None and check_username is None:
            print("new user")
            data = {
                'username': username,
                'email': email,
                'password': password,
                'datetime': datetime.datetime.utcnow(),
                'followers': [],
                'following': []
                }
            request.session['email'] = email

            result = db.user.insert_one(data)

            return HttpResponse("Success")

        if check_username is not None:
            return HttpResponse("Username_taken")
        if check_email is not None:
            return HttpResponse("email_taken")

        return HttpResponse("Error")
