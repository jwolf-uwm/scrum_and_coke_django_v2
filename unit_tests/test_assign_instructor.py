from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class AssignInstructorTests(TestCase):
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
    def setUp(self):
        return

    def test_assign_proper(self):
        ins1 = models.User()
        ins1.email = "ins1@uwm.edu"
        ins1.type = "instructor"
        ins1.save()
        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()
        proper = Commands.assign_instructor_to_course(ins1.email, course.course_id, course.course_department)
        self.assertEqual(proper, "Instructor Assigned!")

    def test_assign_improper_instructor(self):
        ins1 = models.User()
        ins1.email = "ins1@uwm.edu"
        ins1.type = "instructor"
        ins1.save()
        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()
        proper = Commands.assign_instructor_to_course("ins2@uwm.edu", course.course_id, course.course_department)
        self.assertEqual(proper, "no such instructor")

    def test_assign_improper_course(self):
        ins1 = models.User()
        ins1.email = "ins1@uwm.edu"
        ins1.type = "instructor"
        ins1.save()
        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()
        proper = Commands.assign_instructor_to_course(ins1.email, "302", course.course_department)
        self.assertEqual(proper, "no such course")

    def test_assign_instructor_TA(self):
        ta1 = models.User()
        ta1.email = "ta1@uwm.edu"
        ta1.type = "ta"
        ta1.save()
        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()
        proper = Commands.assign_instructor_to_course(ta1.email, course.course_id, course.course_department)
        self.assertEqual(proper, "no such instructor")

    def test_assign_instructor_admin(self):
        ad1 = models.User()
        ad1.email = "ad1@uwm.edu"
        ad1.type = "administrator"
        ad1.save()
        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()
        proper = Commands.assign_instructor_to_course(ad1.email, course.course_id, course.course_department)
        self.assertEqual(proper, "no such instructor")

    def test_assign_instructor_sup(self):
        sup1 = models.User()
        sup1.email = "sup1@uwm.edu"
        sup1.type = "supervisor"
        sup1.save()
        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()
        proper = Commands.assign_instructor_to_course(sup1.email, course.course_id, course.course_department)
        self.assertEqual(proper, "no such instructor")
