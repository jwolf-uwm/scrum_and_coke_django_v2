from ta_assign import models


class Commands:

    # commands organized by page menu order

    # Login commands
    # this appears to be unused in the view
    @staticmethod
    def login(email, password):

        people = models.User.objects.all()

        temp = None

        for i in people:
            if i.isLoggedOn is True:
                return "User already logged in"
            if i.email == email:
                temp = i

        if temp is None:
            return "Invalid login info"
        elif temp.email != email or temp.password != password:
            return "Invalid login info"
        models.User.objects.filter(email=email).update(isLoggedOn=True)
        return

    # Logout commands
    # this also appears unused in the view
    @staticmethod
    def logout(email):

        person = models.User.objects.get(email=email)
        if person.isLoggedOn is False:
            return False
        models.User.objects.filter(email=email).update(isLoggedOn=False)
        return True

    # Create Account Commands
    @staticmethod
    def create_account(email, password, account_type):
        # Jeff's method
        # Usage: (string: email, string: password, string: account_type)

        try:
            find_email = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            find_email = "none"

        if find_email != "none":
            return "Email address taken."

        parse_at = email.split("@")

        try:
            if len(parse_at) != 2 or parse_at[1] != "uwm.edu":
                return "Email address must be uwm address."
        # I'm not sure why I wrote this exception, I don't test for it and can't
        # figure out how it'd even show up, but if it does someday, we'll find out
        except IndexError:
            return "Bad email address."

        if password == "":
            return "Bad password."

        if account_type != "instructor" and account_type != "ta":
            return "Invalid account type."

        some_guy = models.User()
        some_guy.email = email
        some_guy.password = password
        some_guy.type = account_type
        some_guy.save()

        return "Account created!"

    # Create Course Commands
    @staticmethod
    def create_course(course_id, num_labs):
        if len(course_id) != 9:
            return "course_id is the wrong size to be of the right form (CS###-###)"
        if course_id[0:2] != "CS":
            return "course_id is not a CS course (CS###-###)"
        if not course_id[2:5].isdigit():
            return "The course number contains an invalid digit (CS###-###)"
        if course_id[5] != "-":
            return "The course and section number should be separated by a hyphen (CS###-###)"
        if not course_id[6:].isdigit():
            return "The section number contains an invalid digit (CS###-###)"
        try:
            if int(num_labs) < 0 or int(num_labs) > 5:
                return "The number of lab sections should be positive and not exceed 5"
        except ValueError:
            return "num_labs must be an valid number"
        try:
            find_course = models.Course.objects.get(course_id=course_id)
        except models.Course.DoesNotExist:
            find_course = "none"
        if find_course != "none":
            return "Course already exists"

        some_course = models.Course()
        some_course.course_id = course_id
        some_course.num_labs = num_labs
        some_course.save()
        return "Course created successfully"

    # Access Info Commands
    @staticmethod
    def access_info():
        # Jeff's method
        # Usage: access_info()
        # returns a string of all users/courses in the system
        # with appropriate linebreaks for display
        # TODO: REWRITE TO MODEL LIST

        string_list = "Administrator:\n"

        admins = models.User.objects.filter(type="administrator")
        for admin in admins:
            string_list = string_list + admin.name + " | " + admin.email + " | " + \
                          str(admin.phone) + "\n"
            string_list = string_list + "\n"

        string_list = string_list + "Supervisor:\n"

        supers = models.User.objects.filter(type="supervisor")
        for supervi in supers:
            string_list = string_list + supervi.name + " | " + supervi.email + " | " + \
                          str(supervi.phone) + "\n"
            string_list = string_list + "\n"

        string_list = string_list + "Instructors:\n"

        instructs = models.User.objects.filter(type="instructor")
        for instruct in instructs:
            string_list = string_list + instruct.name + " | " + instruct.email + " | " + \
                          str(instruct.phone) + "\n"

            for courses in models.Course.objects.all():
                if courses.instructor == instruct.email:
                    string_list = string_list + "\tCourse: " + courses.course_id + "\n"
            string_list = string_list + "\n"

        string_list = string_list + "\n"

        string_list = string_list + "TAs:\n"

        tee_ayys = models.User.objects.filter(type="ta")
        for tee_ayy in tee_ayys:
            string_list = string_list + tee_ayy.name + " | " + tee_ayy.email + " | " + str(tee_ayy.phone) + \
                          "\n"

            for ta_courses in models.TACourse.objects.all():
                if ta_courses.TA.email == tee_ayy.email:
                    string_list = string_list + "\tCourse: " + ta_courses.course.course_id + "\n"
            string_list = string_list + "\n"

        string_list = string_list + "\n"

        string_list = string_list + "Courses:\n"
        courses = models.Course.objects.all()
        for course in courses:
            string_list = string_list + course.course_id + "\n"
        return string_list

    # Edit Account Commands
    @staticmethod
    def edit_account(email, field, content):
        try:
            models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            return "Entered user does not exist"

        if field == "email":
            parse_at = content.split("@")
            try:
                if len(parse_at) != 2 or parse_at[1] != "uwm.edu":
                    return "Entered email does not end in uwm.edu"
            except ValueError:
                return "Entered email is not of the correct form"
            models.User.objects.filter(email=email).update(email=content)
            return "User has been updated successfully"

        elif field == "password":
            models.User.objects.filter(email=email).update(password=content)
            return "User has been updated successfully"

        elif field == "phone":
            parse_phone = content.split(".")
            if len(parse_phone) != 3:
                return "Phone number is not of the correct form (###.###.####)"
            if not parse_phone[0].isdigit() or not parse_phone[1].isdigit() or not parse_phone[2].isdigit():
                return "Phone number is not of the correct form (###.###.####)"
            if len(parse_phone[0]) != 3 or len(parse_phone[1]) != 3 or len(parse_phone[2]) != 4:
                return "Phone number is not of the correct form (###.###.####)"
            models.User.objects.filter(email=email).update(phone=content)
            return "User has been updated successfully"

        elif field == "name":
            models.User.objects.filter(email=email).update(name=content)
            return "User has been updated successfully"
        else:
            return "The entered data field does not exist"

    # Edit Info Commands
    @staticmethod
    def change_password(email, new):
        if new == "":
            return "Bad password."

        models.User.objects.filter(email=email).update(password=new)
        return "Password changed."

    @staticmethod
    def change_email(email, address):
        parse_at = address.split("@")

        try:
            if len(parse_at) != 2 or parse_at[1] != "uwm.edu":
                return "Email address must be uwm address."
        except ValueError:
            return "Bad email address."

        try:
            find_email = models.User.objects.get(email=address)
        except models.User.DoesNotExist:
            find_email = "none"

        if find_email != "none":
            return "Email address taken."

        models.User.objects.filter(email=email).update(email=address)
        return "Email address changed."

    @staticmethod
    def change_name(email, name):
        models.User.objects.filter(email=email).update(name=name)
        return "Name changed."

    @staticmethod
    def change_phone(email, phone):
        parse_phone = phone.split(".")
        invalid = "Invalid phone format."
        if len(parse_phone) != 3:
            return invalid
        if not parse_phone[0].isdigit() or not parse_phone[1].isdigit() or not parse_phone[2].isdigit():
            return invalid
        if len(parse_phone[0]) != 3 or len(parse_phone[1]) != 3 or len(parse_phone[2]) != 4:
            return invalid

        models.User.objects.filter(email=email).update(phone=phone)
        return "Phone number changed."

    # View Info Commands
    @staticmethod
    def view_info(email):

        this_guy = models.User.objects.get(email=email)
        info_list = [this_guy.email, this_guy.password, this_guy.name, this_guy.phone]

        return info_list

    # Assign Instructor Commands
    @staticmethod
    def assign_instructor(email, course):
        try:
            check_ins = models.User.objects.get(email=email, type="instructor")
        except models.User.DoesNotExist:
            check_ins = None
        if check_ins is None:
            return "no such instructor"
        try:
            check_course = models.Course.objects.get(course_id=course)
        except models.Course.DoesNotExist:
            check_course = None
        if check_course is None:
            return "no such course"

        models.Course.objects.filter(course_id=course).update(instructor=email)

        return "Instructor Assigned!"

    # Assign TA Commands
    @staticmethod
    def assign_ta(email, course):
        try:
            check_ta = models.User.objects.get(email=email, type="ta")
        except models.User.DoesNotExist:
            check_ta = None
        if check_ta is None:
            return "no such ta"
        try:
            check_course = models.Course.objects.get(course_id=course)
        except models.Course.DoesNotExist:
            check_course = None
        if check_course is None:
            return "no such course"

        ta_course = models.TACourse()
        ta_course.TA = check_ta
        ta_course.course = check_course
        ta_course.save()
        return "TA Assigned!"

    # View TA Assign Commands
    @staticmethod
    def view_ta_assign():
        string_list = ""
        tee_ayys = models.User.objects.filter(type="ta")
        for tee_ayy in tee_ayys:
            string_list = string_list + "TA: " + tee_ayy.name + " | " + tee_ayy.email + " | " + tee_ayy.phone + "\n"

            for ta_courses in models.TACourse.objects.all():
                if ta_courses.TA.email == tee_ayy.email:
                    string_list = string_list + "\tCourse: " + ta_courses.course.course_id + "\n"
            string_list = string_list + "\n"

        return string_list
