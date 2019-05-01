from django.shortcuts import render, redirect
from django.views import View
from classes.commands import Commands
from django.contrib import messages
from ta_assign import models


# Create your views here.


# Index/Homepage
class Index(View):

    @staticmethod
    def get(request):
        return render(request, 'main/index.html')


# Login
class Login(View):
    def get(self, request):
        if request.session.get("email"):
            return redirect("index1")

        return render(request, "main/login.html")

    def post(self, request):
        username = request.POST["email"]
        password = request.POST["password"]
        user = models.User.objects.all().filter(email=username)

        if user.count() == 0 or user[0].password != password:
            return render(request, "main/login.html", {"error_messages": "username/password incorrect"})

        models.User.objects.filter(email=username).update(isLoggedOn=True)
        request.session["email"] = username
        request.session["type"] = user[0].type
        return redirect("index1")


# Logout
class Logout(View):
    def get(self, request):
        if not request.session.get("email"):
            return redirect("index1")
        username = request.session.get("email")
        models.User.objects.filter(email=username).update(isLoggedOn=False)
        request.session.pop("email", None)
        return redirect("Login1")


# create Account
class CreateAccount(View):

    @staticmethod
    def get(request):

        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")

        account_type = request.session.get("type")

        if not account_type == "administrator" and not account_type == "supervisor":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")

        return render(request, 'main/create_account.html')

    @staticmethod
    def post(request):

        account_email = request.POST["email"]
        account_password = request.POST["password"]
        account_type = request.POST["type"]
        response = Commands.create_account(account_email, account_password, account_type)

        if response == "Account Created!":
            messages.success(request, response)
        else:
            messages.error(request, response)

        return render(request, 'main/create_account.html')


# Create Course
class CreateCourse(View):
    def get(self, request):
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")

        account_type = request.session.get("type")

        if not account_type == "administrator" and not account_type == "supervisor":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")

        return render(request, 'main/create_course.html')

    def post(self, request):
        course_id = request.POST["course_id"]
        course_section = request.POST["course_section"]
        num_labs = request.POST["num_labs"]

        response = Commands.create_course("CS"+course_id+"-"+course_section, num_labs)

        if response == "Course has been created successfully.":
            messages.success(request, response)
        else:
            messages.error(request, response)

        return render(request, 'main/create_course.html', {"message": [course_id, course_section, num_labs]})


# Access Info
class AccessInfo(View):

    @staticmethod
    def get(request):

        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")

        account_type = request.session.get("type")

        if not account_type == "administrator" and not account_type == "supervisor":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")

        response = Commands.access_info()
        messages.success(request, response)
        return render(request, 'main/access_info.html')


# Edit Account
class EditAccount(View):
    def get(self, request):
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")

        account_type = request.session.get("type")

        if not account_type == "administrator" and not account_type == "supervisor":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")

        return render(request, 'main/edit_account.html')

    def post(self, request):
        email = request.POST["email"]
        field = request.POST["field"]
        data = request.POST["data"]

        response = Commands.edit_account(email, field, data)

        if response == "Command successful.":
            messages.success(request, response)
        else:
            messages.error(request, response)

        return render(request, 'main/edit_account.html')


# Edit Info

# Assign Instructor

# Assign TA

# View TA Assign
