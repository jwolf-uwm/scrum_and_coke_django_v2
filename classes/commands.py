from ta_assign import models


class Commands:

    # commands organized by page they are found on

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
        # returns True if account successfully created in DB
        # returns False if account was unable to be created
        # throws exceptions if you do it wrong

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
        except IndexError:
            return "Bad email address."

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
            return "course_id is too short to be of the right form (CS###-###)"
        if course_id[0:2] != "CS":
            return "course_id is not a CS course (CS###-###)"
        if not course_id[2:5].isdigit():
            return "The course number contains an invalid digit (CS###-###)"
        if course_id[5] != "-":
            return "The course and section number should be separated by a hyphen (CS###-###)"
        if not course_id[6:].isdigit():
            return "The section number contains an invalid digit (CS###-###)"
        if num_labs < 0 or num_labs > 5:
            return "The number of lab sections should be positive and not exceed 5"
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
            return "User's email has been updated successfully"

        elif field == "password":
            models.User.objects.filter(email=email).update(password=content)
            return "User's password has been updated successfully"

        elif field == "phone":
            parse_phone = content.split(".")
            if len(parse_phone) != 3:
                return "Phone number is not of the correct form (###.###.####)"
            if not parse_phone[0].isdigit() or not parse_phone[1].isdigit() or not parse_phone[2].isdigit():
                return "Phone number is not of the correct form (###.###.####)"
            if len(parse_phone[0]) != 3 or len(parse_phone[1]) != 3 or len(parse_phone[2]) != 4:
                return "Phone number is not of the correct form (###.###.####)"
            models.User.objects.filter(email=email).update(phone=content)
            return "User's phone number has been updated successfully"

        elif field == "name":
            models.User.objects.filter(email=email).update(name=content)
            return "User's name has been updated successfully"
        else:
            return "The entered data field does not exist"
