from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class TestAccessinfo(TestCase):

    def setUp(self):
        ad1 = models.User()
        ad1.email = "ad1@uwm.edu"
        ad1.type = "administrator"
        ad1.save()

        sup1 = models.User()
        sup1.email = "sup1@uwm.edu"
        sup1.type = "supervisor"
        sup1.save()

    def test_access_info_admin_title(self):
        access_info = Commands.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[0], "Administrator:")

    def test_access_info_admin_(self):
        access_info = Commands.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[1], "DEFAULT | ad1@uwm.edu | 000.000.0000")

    def test_access_info_blank_one(self):
        access_info = Commands.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[2], "")

    def test_access_info_sup_title(self):
        access_info = Commands.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[3], "Supervisor:")

    def test_access_info_sup(self):
        access_info = Commands.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[4], "DEFAULT | sup1@uwm.edu | 000.000.0000")

    def test_access_info_blank_two(self):
        access_info = Commands.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[5], "")

    def test_access_info_inst_title(self):
        access_info = Commands.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[6], "Instructors:")

    def test_access_info_blank_three(self):
        access_info = Commands.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[7], "")

    def test_access_info_ta_title(self):
        access_info = Commands.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[8], "TAs:")

    def test_access_info_blank_four(self):
        access_info = Commands.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[9], "")

    def test_access_info_course_title(self):
        access_info = Commands.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[10], "Courses:")

    def test_access_info_inst_no_course(self):
        # Add instructor, no course assignments
        inst1 = models.User()
        inst1.email = "inst1@uwm.edu"
        inst1.type = "instructor"
        inst1.save()
        access_info = Commands.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[7], "DEFAULT | inst1@uwm.edu | 000.000.0000")

    def test_access_info_ta_no_course(self):
        # Add TA, no course assignments
        ta1 = models.User()
        ta1.email = "ta1@uwm.edu"
        ta1.type = "ta"
        ta1.save()
        access_info = Commands.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[9], "DEFAULT | ta1@uwm.edu | 000.000.0000")

    def test_access_info_inst_one_course(self):
        # Instructor with a course
        inst1 = models.User()
        inst1.email = "inst1@uwm.edu"
        inst1.type = "instructor"
        inst1.save()
        course1 = models.Course()
        course1.course_id = "CS101"
        course1.instructor = "inst1@uwm.edu"
        course1.save()
        access_info = Commands.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[7], "DEFAULT | inst1@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[8], "\tCourse: CS101")

    def test_access_info_ta_one_course(self):
        # TA with a course
        ta1 = models.User()
        ta1.email = "ta1@uwm.edu"
        ta1.type = "ta"
        ta1.save()
        course1 = models.Course()
        course1.course_id = "CS101"
        course1.instructor = "inst1@uwm.edu"
        course1.save()
        ta1_course1 = models.TACourse()
        ta1_course1.TA = ta1
        ta1_course1.course = course1
        ta1_course1.save()
        access_info = Commands.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[10], "\tCourse: CS101")

    def test_access_info_course(self):
        # just a course
        course1 = models.Course()
        course1.course_id = "CS101"
        course1.instructor = "inst1@uwm.edu"
        course1.save()
        access_info = Commands.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[11], "CS101")

    def test_access_info_all_the_things(self):
        # ALL THE THINGS
        inst1 = models.User()
        inst1.email = "inst1@uwm.edu"
        inst1.type = "instructor"
        inst1.save()
        inst2 = models.User()
        inst2.email = "inst2@uwm.edu"
        inst2.type = "instructor"
        inst2.save()
        ta1 = models.User()
        ta1.email = "ta1@uwm.edu"
        ta1.type = "ta"
        ta1.save()
        ta2 = models.User()
        ta2.email = "ta2@uwm.edu"
        ta2.type = "ta"
        ta2.save()
        course1 = models.Course()
        course1.course_id = "CS101"
        course1.instructor = "inst1@uwm.edu"
        course1.save()
        course2 = models.Course()
        course2.course_id = "CS102"
        course2.instructor = "inst2@uwm.edu"
        course2.save()
        ta1_course1 = models.TACourse()
        ta1_course1.TA = ta1
        ta1_course1.course = course1
        ta1_course1.save()
        ta2_course2 = models.TACourse()
        ta2_course2.TA = ta2
        ta2_course2.course = course2
        ta2_course2.save()
        access_info = Commands.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[0], "Administrator:")
        self.assertEqual(parse_info[1], "DEFAULT | ad1@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[2], "")
        self.assertEqual(parse_info[3], "Supervisor:")
        self.assertEqual(parse_info[4], "DEFAULT | sup1@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[5], "")
        self.assertEqual(parse_info[6], "Instructors:")
        self.assertEqual(parse_info[7], "DEFAULT | inst1@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[8], "\tCourse: CS101")
        self.assertEqual(parse_info[9], "")
        self.assertEqual(parse_info[10], "DEFAULT | inst2@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[11], "\tCourse: CS102")
        self.assertEqual(parse_info[12], "")
        self.assertEqual(parse_info[13], "")
        self.assertEqual(parse_info[14], "TAs:")
        self.assertEqual(parse_info[15], "DEFAULT | ta1@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[16], "\tCourse: CS101")
        self.assertEqual(parse_info[17], "")
        self.assertEqual(parse_info[18], "DEFAULT | ta2@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[19], "\tCourse: CS102")
        self.assertEqual(parse_info[20], "")
        self.assertEqual(parse_info[21], "")
        self.assertEqual(parse_info[22], "Courses:")
        self.assertEqual(parse_info[23], "CS101")
        self.assertEqual(parse_info[24], "CS102")
