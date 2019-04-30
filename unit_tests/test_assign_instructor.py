from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class AssignInstructorTests(TestCase):

    def setUp(self):
        ad1 = models.User()
        ad1.email = "ad1@uwm.edu"
        ad1.type = "administrator"
        ad1.save()

        sup1 = models.User()
        sup1.email = "sup1@uwm.edu"
        sup1.type = "supervisor"
        sup1.save()


        """
            Assigning an instructor requires user logged in as Supervisor or Administrator.
            When the create account command is entered, it takes two arguments:
                - Instructor ID
                - Course ID
            If the course does not currently have an instructor, assigns instructor to that course and
            is successful:
            - "Instructor *Instructor Name* assigned to class *Class Name*."
            If the course is already assigned to an instructor then failure:
            - "*Class Name* already has an instructor."
            If the Instructor ID or Course ID is omitted, failure:
            - "Invalid arguments in command."
            If attempting to assign a role that is not instructor, failure:
            - "Only instructors can be assigned to classes."
            If the user is not logged in as a Supervisor or Administrator, failure:
            - "You are not authorized to assign instructors."
            If an invalid email address is used for the instructor, failure:
            - "Invalid email address."
            If the course entered does not exist, failure:
            - "Course does not exist."
            If the instructor entered does not exist, failure:
            - "Instructor does not exist."
        """



    def test_assign_instructor_supervisor(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account inst@uwm.edu password instructor")
        self.ui.parse_command("create_course CS201-401 3")
        self.assertEqual(self.ui.parse_command("assign_instructor inst@uwm.edu CS201-401"),
                             "command successful")

    def test_assign_instructor_administrator(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("assign_instructor instructor@uwm.edu CS201-401"),
                             "Access Denied")

    def test_assign_instructor_instructor(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account inst@uwm.edu password instructor")
        self.ui.parse_command("create_course CS201-401 3")
        self.ui.parse_command("logout")
        self.ui.parse_command("login inst@uwm.edu password")
        self.assertEqual(self.ui.parse_command("assign_instructor inst@uwm.edu CS201-401"),
                             "Access Denied")

    def test_assign_instructor_TA(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu TAPassword ta")
        self.ui.parse_command("create_course CS201-401 3")
        self.ui.parse_command("logout")
        self.ui.parse_command("login ta@uwm.edu TAPassword")
        self.assertEqual(self.ui.parse_command("assign_instructor inst@uwm.edu CS201-401"),
                             "Access Denied")

    def test_assign_instructor_invalid_arguments(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.assertEqual(self.ui.parse_command("assign_instructor instructor@uwm.edu"),
                             "Incorrect Command")

    def test_assign_instructor_assign_TA(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.assertEqual(self.ui.parse_command("assign_instructor ta@uwm.edu CS201-401"), "no such instructor")

    def test_invalid_email(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.assertEqual(self.ui.parse_command("assign_instructor ins1, SomeCSClass3"), "no such instructor")

    def test_nonexistent_course(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ins1@uwm.edu password instructor")
        self.assertEqual(self.ui.parse_command("assign_instructor ins1@uwm.edu CS400-601"), "no such course")
