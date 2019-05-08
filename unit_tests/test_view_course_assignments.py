from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class ViewCourseAssignmentsTests(TestCase):

    def setUp(self):
        return

    def test_add_one_course(self):
        inst1 = models.User()
        inst1.email = "inst@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        course = models.Course()
        course.course_department = "COMPSCI"
        course.course_id = "301"
        course.save()

        insCourse = models.InstructorCourse()
        insCourse.course = course
        insCourse.instructor = inst1
        insCourse.save()

        response=Commands.view_course_assignments(inst1.email)
        self.assertEqual(response, "COMPSCI: 301 \n")

    def test_add_two_course(self):
        inst1 = models.User()
        inst1.email = "inst@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        course = models.Course()
        course.course_department = "COMPSCI"
        course.course_id = "301"
        course.save()

        course2 = models.Course()
        course2.course_department = "COMPSCI"
        course2.course_id = "351"
        course2.save()

        insCourse = models.InstructorCourse()
        insCourse.course = course
        insCourse.instructor = inst1
        insCourse.save()

        insCourse = models.InstructorCourse()
        insCourse.course = course2
        insCourse.instructor = inst1
        insCourse.save()

        response = Commands.view_course_assignments(inst1.email)
        self.assertEqual(response, "COMPSCI: 301 \nCOMPSCI: 351 \n")