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
        num = int(num_labs)
        for i in range(num):
            lab = models.Lab()
            lab.section_id = 801 + i
            lab.course_id = course_id
            lab.save()

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
class EditInfo(View):

    @staticmethod
    def get(request):
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")

        some_guy = models.User.objects.get(email=request.session.get("email"))

        return render(request, 'main/edit_info.html', {"some_email": some_guy.email, "some_password": some_guy.password,
                                                       "some_name": some_guy.name, "some_phone": some_guy.phone})

    @staticmethod
    def post(request):
        email = request.POST["email"]
        password = request.POST["password"]
        name = request.POST["name"]
        phone = request.POST["phone"]
        pick_anything = False

        if email != "":
            pick_anything = True
            response = Commands.change_email(request.session["email"], email)
            if response == "Email address changed.":
                messages.success(request, response)
                request.session["email"] = email
            else:
                messages.error(request, response)

        if password != "":
            pick_anything = True
            response = Commands.change_password(request.session["email"], password)

            if response == "Password changed.":
                messages.success(request, response)
            else:
                messages.error(request, response)

        if name != "":
            pick_anything = True
            response = Commands.change_name(request.session["email"], name)

            if response == "Name changed.":
                messages.success(request, response)
            else:
                messages.error(request, response)

        if phone != "":
            pick_anything = True
            response = Commands.change_phone(request.session["email"], phone)

            if response == "Phone number changed.":
                messages.success(request, response)
            else:
                messages.error(request, response)

        if not pick_anything:
            messages.error(request, "You should pick something to change.")

        return redirect("EditInfo1")

# Assign Instructor


class AssignInstructorToCourse(View):
    def get(self, request):
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")
        account_type = request.session.get("type")
        if not account_type == "supervisor":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")
        return render(request, 'main/assign_instructor.html')

    def post(self, request):
        email1 = request.POST["email"]
        course_id = request.POST["course_id"]
        course_section = request.POST["course_section"]
        command_course = "CS" + course_id + "-" + course_section
        response = Commands.assign_instructor(email1, command_course)

        if response == "Instructor Assigned!":
            messages.success(request, response)
        else:
            messages.error(request, response)
        return render(request, 'main/assign_instructor.html')

    # Assign TA


class AssignTAToCourse(View):
    def get(self, request):
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")
        account_type = request.session.get("type")
        if not account_type == "supervisor":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")
        return render(request, 'main/assign_ta.html')

    def post(self, request):
        email = request.POST["email"]
        course_id = request.POST["course_id"]
        course_section = request.POST["course_section"]
        command_input = "CS" + course_id + "-" + course_section
        response = Commands.assign_ta(email, command_input)
        if response == "TA Assigned!":
            messages.success(request, response)
        else:
            messages.error(request, response)
        return render(request, 'main/assign_ta.html')

# View course assignments


class ViewCourseAssignments(View):

    def get(self, request):

        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")

        account_type = request.session.get("type")

        if not account_type == "instructor":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")

        response = Commands.view_course_assignments(request.session.get("email"))
        messages.success(request, response)
        return render(request, 'main/view_course_assignments.html')
# View TA Assign
