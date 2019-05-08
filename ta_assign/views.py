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
        request.session.set_expiry(300)
        if request.session.get("email"):
            return redirect("index1")

        return render(request, "main/login.html")

    def post(self, request):
        request.session.set_expiry(300)
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
        request.session.set_expiry(300)
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
        request.session.set_expiry(300)
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
        request.session.set_expiry(300)
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
        request.session.set_expiry(300)
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")

        account_type = request.session.get("type")

        if not account_type == "administrator" and not account_type == "supervisor":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")

        return render(request, 'main/create_course.html')

    def post(self, request):
        request.session.set_expiry(300)
        course_department = request.POST["course_department"]
        course_id = request.POST["course_id"]
        num_lectures = request.POST["num_lectures"]
        num_labs = request.POST["num_labs"]

        response = Commands.create_course(course_department, course_id, num_lectures, num_labs)

        if response == "Course has been created successfully.":
            messages.success(request, response)
        else:
            messages.error(request, response)

        return render(request, 'main/create_course.html', {"message": [course_department, course_id, num_lectures, num_labs]})


# Access Info
class AccessInfo(View):

    @staticmethod
    def get(request):
        request.session.set_expiry(300)
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")

        account_type = request.session.get("type")

        if not account_type == "administrator" and not account_type == "supervisor":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")

        admin = models.User.objects.get(type="administrator")
        supervisor = models.User.objects.get(type="supervisor")
        instructors = models.User.objects.filter(type="instructor")
        tas = models.User.objects.filter(type="ta")
        courses = models.Course.objects.all()

        return render(request, 'main/access_info.html', {"admin": admin, "super": supervisor,
                                                         "instructors": instructors, "tas": tas, "courses": courses})


class CourseView(View):
    def get(self, request, **kwargs):
        request.session.set_expiry(300)
        course_dept_id = self.kwargs["course_dept_id"]

        course = models.Course.objects.get(course_dept_id=course_dept_id)
        labs = models.Lab.objects.filter(course=course)
        lectures = models.Lecture.objects.filter(course=course)

        instructor_courses = models.InstructorCourse.objects.filter(course=course)
        instructors = []
        for instructor_course in instructor_courses:
            instructors.append(instructor_course.instructor)

        ta_courses = models.TACourse.objects.filter(course=course)
        tas = []
        for ta_course in ta_courses:
            tas.append(ta_course.TA)

        return render(request, 'main/course.html', {"course_dept_id": course_dept_id, "labs": labs,
                                                    "lectures": lectures, "instructors": instructors, "tas": tas})


class InstructorView(View):
    def get(self, request, **kwargs):
        request.session.set_expiry(300)
        instructor_email = self.kwargs["instructor_email"]

        instructor = models.User.objects.get(email=instructor_email)

        instructor_courses = models.InstructorCourse.objects.filter(instructor=instructor)
        courses = []
        for instructor_course in instructor_courses:
            courses.append(instructor_course.course)

        instructor_lectures = models.Lecture.objects.filter(instructor=instructor.email)
        lectures = []
        for instructor_lecture in instructor_lectures:
            lectures.append(instructor_lecture)

        return render(request, 'main/instructor.html', {"instructor_name": instructor.name, "instructor": instructor,
                                                        "courses": courses, "lectures": lectures})


class TAView(View):
    def get(self, request, **kwargs):
        request.session.set_expiry(300)
        ta_email = self.kwargs["ta_email"]

        ta = models.User.objects.get(email=ta_email)

        ta_courses = models.TACourse.objects.filter(TA=ta)
        courses = []
        for ta_course in ta_courses:
            courses.append(ta_course.course)

        ta_lectures = models.Lecture.objects.filter(TA=ta.email)
        lectures = []
        for ta_lecture in ta_lectures:
            lectures.append(ta_lecture)

        ta_labs = models.Lab.objects.filter(TA=ta.email)
        labs = []
        for ta_lab in ta_labs:
            labs.append(ta_lab)

        return render(request, 'main/TA.html', {"ta_name": ta.name, "ta": ta, "courses": courses, "labs": labs,
                                                "lectures": lectures})


# Edit Account
class EditAccount(View):
    def get(self, request):
        request.session.set_expiry(300)
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")

        account_type = request.session.get("type")

        if not account_type == "administrator" and not account_type == "supervisor":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")

        return render(request, 'main/edit_account.html')

    def post(self, request):
        request.session.set_expiry(300)
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
        request.session.set_expiry(300)
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")

        some_guy = models.User.objects.get(email=request.session.get("email"))

        return render(request, 'main/edit_info.html', {"some_email": some_guy.email, "some_password": some_guy.password,
                                                       "some_name": some_guy.name, "some_phone": some_guy.phone,
                                                       "some_address": some_guy.address})

    @staticmethod
    def post(request):
        request.session.set_expiry(300)
        email = request.POST["email"]
        password = request.POST["password"]
        name = request.POST["name"]
        phone = request.POST["phone"]
        address = request.POST["address"]
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

        if address != "":
            pick_anything = True
            response = Commands.change_address(request.session["email"], address)

            if response == "Address changed.":
                messages.success(request, response)
            else:
                messages.error(request, response)

        if not pick_anything:
            messages.error(request, "You should pick something to change.")

        return redirect("EditInfo1")


# Edit Lecture/Lab
class EditLecLab(View):
    def get(self, request):
        request.session.set_expiry(300)
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")

        account_type = request.session.get("type")

        if not account_type == "administrator" and not account_type == "supervisor":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")

        return render(request, 'main/edit_lec_lab.html')

    def post(self, request):
        request.session.set_expiry(300)
        department = request.POST["course_department"]
        course_id = request.POST["course_id"]
        section_type = request.POST["section"]
        section_id = request.POST["section_id"]
        location = request.POST["location"]
        time = request.POST["time"]

        response = Commands.edit_lec_lab(department, course_id, section_type, section_id, location, time)

        if response == "Section has been edited successfully.":
            messages.success(request, response)
        else:
            messages.error(request, response)

        return render(request, 'main/edit_lec_lab.html')

# Assign Instructor


class AssignInstructorToCourse(View):
    def get(self, request):
        request.session.set_expiry(300)
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")
        account_type = request.session.get("type")
        if not account_type == "supervisor":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")
        return render(request, 'main/assign_instructor.html')

    def post(self, request):
        request.session.set_expiry(300)
        email1 = request.POST["email"]
        course_department = request.POST["course_department"]
        course_id = request.POST["course_id"]
        response = Commands.assign_instructor_to_course(email1, course_id, course_department)

        if response == "Instructor Assigned!":
            messages.success(request, response)
        else:
            messages.error(request, response)
        return render(request, 'main/assign_instructor.html')


# Assign TA
class AssignTAToCourse(View):
    def get(self, request):
        request.session.set_expiry(300)
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")
        account_type = request.session.get("type")
        if not account_type == "supervisor" :
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")
        return render(request, 'main/assign_ta.html')

    def post(self, request):
        request.session.set_expiry(300)
        email = request.POST["email"]
        course_id = request.POST["course_id"]
        course_department = request.POST["course_department"]
        response = Commands.assign_ta_to_course(email, course_id, course_department)
        if response == "TA Assigned!":
            messages.success(request, response)
        else:
            messages.error(request, response)
        return render(request, 'main/assign_ta.html')


class AssignInstructorToLecture(View):
    def get(self, request):
        request.session.set_expiry(300)
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")
        account_type = request.session.get("type")
        if not account_type == "supervisor":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")
        return render(request, 'main/assign_instructor_lec.html')

    def post(self, request):
        request.session.set_expiry(300)
        email = request.POST["email"]
        course_id = request.POST["course_id"]
        course_section = request.POST["course_section"]
        course_department = request.POST["course_department"]
        response = Commands.assign_instructor_to_lec(email, course_id, course_section, course_department)
        if response == "Instructor assigned to lecture":
            messages.success(request, response)
        else:
            messages.error(request, response)
        return render(request, 'main/assign_instructor_lec.html')


class AssignTAToLabLec(View):
    def get(self, request):
        request.session.set_expiry(300)
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")
        account_type = request.session.get("type")
        if not account_type == "instructor" and not account_type == "supervisor":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")
        return render(request, 'main/assign_ta_lablec.html')

    def post(self, request):
        request.session.set_expiry(300)
        ins = request.session.get("email")
        email = request.POST["email"]
        course_id = request.POST["course_id"]
        course_section = request.POST["course_section"]
        course_department = request.POST["course_department"]
        response = Commands.assign_ta_to_lablec(ins, email, course_id, course_section, course_department)
        if response == "TA Assigned!":
            messages.success(request, response)
        else:
            messages.error(request, response)
        return render(request, 'main/assign_ta_lablec.html')


# View course assignments
class ViewCourseAssignments(View):

    def get(self, request):
        request.session.set_expiry(300)
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
class ViewTAAssign(View):

    @staticmethod
    def get(request):
        request.session.set_expiry(300)
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")

        account_type = request.session.get("type")

        if not account_type == "instructor" and not account_type == "ta":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")

        tas = models.User.objects.filter(type="ta")
        courses = []
        lecs = []
        labs = []
        for ta in tas:

            for ta_courses in models.TACourse.objects.all():
                if ta_courses.TA.email == ta.email:
                    courses.append(ta_courses)

            for ta_lec in models.Lecture.objects.all():
                if ta_lec.TA == ta.email:
                    lecs.append(ta_lec)

            for ta_lab in models.Lab.objects.all():
                if ta_lab.TA == ta.email:
                    labs.append(ta_lab)

        return render(request, 'main/view_ta_assign.html', {"tas": tas, "courses": courses,
                                                                 "lecs": lecs, "labs": labs})


class DeleteAccount(View):
    def get(self, request):
        request.session.set_expiry(300)
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")

        account_type = request.session.get("type")

        if not account_type == "administrator" and not account_type == "supervisor":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")
        return render(request, 'main/delete_account.html')

    def post(self, request):
        request.session.set_expiry(300)
        username = request.POST["email"]
        response = Commands.delete_account(username)

        if response == "Command successful.":
            messages.success(request, response)
        else:
            messages.error(request, response)

        return redirect("Delete1")


# Read Public Contact Info
class ContactInfo(View):

    @staticmethod
    def get(request):
        request.session.set_expiry(300)
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")

        account_type = request.session.get("type")

        if not account_type == "instructor" and not account_type == "ta":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")

        admin = models.User.objects.get(type="administrator")
        supervisor = models.User.objects.get(type="supervisor")
        instructors = models.User.objects.filter(type="instructor")
        tas = models.User.objects.filter(type="ta")

        return render(request, 'main/contact_info.html', {"admin": admin, "super": supervisor,
                                                          "instructors": instructors, "tas": tas})
