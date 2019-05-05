from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class AssignTACourse(TestCase):
    def setUp(self):
        return

    def test_assign_ta_proper(self):
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
        proper = Commands.assign_ta_to_course(ta1.email, course.course_id, course.course_department)
        self.assertEqual(proper, "TA Assigned!")

    def test_assign_ta_course_improper_ta(self):
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
        proper = Commands.assign_ta_to_course("ta2@uwm.edu", course.course_id, course.course_department)
        self.assertEqual(proper, "no such ta")

    def test_assign_ta_improper_course(self):
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
        proper = Commands.assign_ta_to_course(ta1.email, "302", course.course_department)
        self.assertEqual(proper, "no such course")

    def test_assign_ta_admin(self):
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
        proper = Commands.assign_ta_to_course(ad1.email, course.course_id, course.course_department)
        self.assertEqual(proper, "no such ta")

    def test_assign_ta_sup(self):
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
        proper = Commands.assign_ta_to_course(sup1.email, course.course_id, course.course_department)
        self.assertEqual(proper, "no such ta")

    def test_assign_ta_ins(self):
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
        proper = Commands.assign_ta_to_course(ins1.email, course.course_id, course.course_department)
        self.assertEqual(proper, "no such ta")

    def test_assign_ta_too_many(self):
        ta1 = models.User()
        ta1.email = "ta1@uwm.edu"
        ta1.type = "ta"
        ta1.save()
        ta2 = models.User()
        ta2.email = "ta2@uwm.edu"
        ta2.type = "ta"
        ta2.save()
        ta3 = models.User()
        ta3.email = "ta3@uwm.edu"
        ta3.type = "ta"
        ta3.save()
        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()
        proper = Commands.assign_ta_to_course(ta1.email, course.course_id, course.course_department)
        self.assertEqual(proper, "TA Assigned!")
        proper = Commands.assign_ta_to_course(ta2.email, course.course_id, course.course_department)
        self.assertEqual(proper, "TA Assigned!")
        proper = Commands.assign_ta_to_course(ta3.email, course.course_id, course.course_department)
        self.assertEqual(proper, "Too Many TA's Assigned")

    def test_assign_ta_already_assigned(self):
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
        proper = Commands.assign_ta_to_course(ta1.email, course.course_id, course.course_department)
        self.assertEqual(proper, "TA Assigned!")
        proper = Commands.assign_ta_to_course(ta1.email, course.course_id, course.course_department)
        self.assertEqual(proper, "TA Already Assigned!")
