from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class TestViewTAAssign(TestCase):

    def setUp(self):
        return

    def test_no_ta_assignments(self):

        lists = Commands.view_ta_assign()
        self.assertTrue(len(lists) == 0)

    def test_inst(self):

        inst1 = models.User()
        inst1.email = "inst1@uwm.edu"
        inst1.password = "password"
        inst1.type = "instructor"
        inst1.save()

        lists = Commands.view_ta_assign()
        self.assertEquals(lists, "")

    def test_ta(self):

        ta1 = models.User()
        ta1.email = "ta1@uwm.edu"
        ta1.password = "password"
        ta1.type = "ta"
        ta1.save()

        lists = Commands.view_ta_assign()
        self.assertEquals(lists, "TA: DEFAULT | ta1@uwm.edu | 000.000.0000\n\n")

    def test_admin(self):

        ad1 = models.User()
        ad1.email = "admin@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.save()

        lists = Commands.view_ta_assign()
        self.assertEquals(lists, "")

    def test_super(self):

        sup1 = models.User()
        sup1.email = "super@uwm.edu"
        sup1.password = "password"
        sup1.type = "supervisor"
        sup1.save()

        lists = Commands.view_ta_assign()
        self.assertEquals(lists, "")

    def test_one_course_and_ta(self):

        ta1 = models.User()
        ta1.email = "ta1@uwm.edu"
        ta1.password = "password"
        ta1.type = "ta"
        ta1.save()

        course1 = models.Course()
        course1.course_department = "COMPSCI"
        course1.course_id = "100"
        course1.course_dept_id = "COMPSCI100"
        course1.save()

        ta1_course1 = models.TACourse()
        ta1_course1.course = course1
        ta1_course1.TA = ta1
        ta1_course1.save()

        lists = Commands.view_ta_assign()
        self.assertEquals(lists, "TA: DEFAULT | ta1@uwm.edu | 000.000.0000\n\tCourse: COMPSCI100\n\n")

    def test_inst_and_one_ta(self):

        ta1 = models.User()
        ta1.email = "ta1@uwm.edu"
        ta1.password = "password"
        ta1.type = "ta"
        ta1.save()

        inst1 = models.User()
        inst1.email = "inst1@uwm.edu"
        inst1.password = "password"
        inst1.type = "instructor"
        inst1.save()

        lists = Commands.view_ta_assign()
        self.assertEquals(lists, "TA: DEFAULT | ta1@uwm.edu | 000.000.0000\n\n")

    def test_ta_no_courses(self):

        ta1 = models.User()
        ta1.email = "ta1@uwm.edu"
        ta1.password = "password"
        ta1.type = "ta"
        ta1.save()

        lists = Commands.view_ta_assign()
        self.assertEquals(lists, "TA: DEFAULT | ta1@uwm.edu | 000.000.0000\n\n")

    def test_all_the_things(self):

        ta1 = models.User()
        ta1.email = "ta1@uwm.edu"
        ta1.password = "password"
        ta1.type = "ta"
        ta1.save()

        course1 = models.Course()
        course1.course_department = "COMPSCI"
        course1.course_id = "100"
        course1.course_dept_id = "COMPSCI100"
        course1.save()

        ta1_course1 = models.TACourse()
        ta1_course1.course = course1
        ta1_course1.TA = ta1
        ta1_course1.save()

        ta2 = models.User()
        ta2.email = "ta2@uwm.edu"
        ta2.password = "password"
        ta2.type = "ta"
        ta2.save()

        course2 = models.Course()
        course2.course_department = "COMPSCI"
        course2.course_id = "101"
        course2.course_dept_id = "COMPSCI101"
        course2.save()

        ta2_course2 = models.TACourse()
        ta2_course2.course = course2
        ta2_course2.TA = ta2
        ta2_course2.save()

        ta3 = models.User()
        ta3.email = "ta3@uwm.edu"
        ta3.password = "password"
        ta3.type = "ta"
        ta3.save()

        lists = Commands.view_ta_assign()
        self.assertEquals(lists, "TA: DEFAULT | ta1@uwm.edu | 000.000.0000\n\tCourse: COMPSCI100\n\n"
                                 "TA: DEFAULT | ta2@uwm.edu | 000.000.0000\n\tCourse: COMPSCI101\n\n"
                                 "TA: DEFAULT | ta3@uwm.edu | 000.000.0000\n\n")
