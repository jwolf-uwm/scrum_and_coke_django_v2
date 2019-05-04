from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class TestAccessinfo(TestCase):

    def setUp(self):
        return

    def test_no_info(self):
        lists = Commands.access_info()
        users = lists[0]
        courses = lists[1]
        self.assertTrue(len(users) == 0)
        self.assertTrue(len(courses) == 0)

    def test_admin_only(self):
        ad1 = models.User()
        ad1.email = "admin@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.save()

        lists = Commands.access_info()
        users = lists[0]
        self.assertEquals(users[0], ad1)

    def test_super_only(self):
        sup1 = models.User()
        sup1.email = "super@uwm.edu"
        sup1.password = "password"
        sup1.type = "supervisor"
        sup1.save()

        lists = Commands.access_info()
        users = lists[0]
        self.assertEquals(users[0], sup1)

    def test_inst_only(self):
        inst1 = models.User()
        inst1.email = "inst1@uwm.edu"
        inst1.password = "password"
        inst1.type = "instructor"
        inst1.save()

        lists = Commands.access_info()
        users = lists[0]
        self.assertEquals(users[0], inst1)

    def test_ta_only(self):
        ta1 = models.User()
        ta1.email = "ta1@uwm.edu"
        ta1.password = "password"
        ta1.type = "ta"
        ta1.save()

        lists = Commands.access_info()
        users = lists[0]
        self.assertEquals(users[0], ta1)

    def test_admin_super_default(self):
        ad1 = models.User()
        ad1.email = "admin@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.save()

        sup1 = models.User()
        sup1.email = "super@uwm.edu"
        sup1.password = "password"
        sup1.type = "supervisor"
        sup1.save()

        lists = Commands.access_info()
        users = lists[0]
        self.assertTrue(ad1 in users)
        self.assertTrue(sup1 in users)

    def test_each_user(self):
        ad1 = models.User()
        ad1.email = "admin@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.save()

        sup1 = models.User()
        sup1.email = "super@uwm.edu"
        sup1.password = "password"
        sup1.type = "supervisor"
        sup1.save()

        inst1 = models.User()
        inst1.email = "inst1@uwm.edu"
        inst1.password = "password"
        inst1.type = "instructor"
        inst1.save()

        ta1 = models.User()
        ta1.email = "ta1@uwm.edu"
        ta1.password = "password"
        ta1.type = "ta"
        ta1.save()

        lists = Commands.access_info()
        users = lists[0]
        self.assertTrue(ad1 in users)
        self.assertTrue(sup1 in users)
        self.assertTrue(inst1 in users)
        self.assertTrue(ta1 in users)

    def test_one_course(self):
        course1 = models.Course()
        course1.course_department = "COMPSCI"
        course1.course_id = "100"
        course1.save()

        lists = Commands.access_info()
        courses = lists[1]
        self.assertTrue(course1 in courses)

    def test_two_courses(self):
        course1 = models.Course()
        course1.course_department = "COMPSCI"
        course1.course_id = "100"
        course1.save()

        course2 = models.Course()
        course2.course_department = "COMPSCI"
        course2.course_id = "150"
        course2.save()

        lists = Commands.access_info()
        courses = lists[1]
        self.assertTrue(course1 in courses)
        self.assertTrue(course2 in courses)

    def test_course_default_setup(self):
        ad1 = models.User()
        ad1.email = "admin@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.save()

        sup1 = models.User()
        sup1.email = "super@uwm.edu"
        sup1.password = "password"
        sup1.type = "supervisor"
        sup1.save()

        course1 = models.Course()
        course1.course_department = "COMPSCI"
        course1.course_id = "100"
        course1.save()

        lists = Commands.access_info()
        users = lists[0]
        self.assertTrue(ad1 in users)
        self.assertTrue(sup1 in users)
        courses = lists[1]
        self.assertTrue(course1 in courses)

    def test_all_the_things(self):
        ad1 = models.User()
        ad1.email = "admin@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.save()

        sup1 = models.User()
        sup1.email = "super@uwm.edu"
        sup1.password = "password"
        sup1.type = "supervisor"
        sup1.save()

        inst1 = models.User()
        inst1.email = "inst1@uwm.edu"
        inst1.password = "password"
        inst1.type = "instructor"
        inst1.save()

        ta1 = models.User()
        ta1.email = "ta1@uwm.edu"
        ta1.password = "password"
        ta1.type = "ta"
        ta1.save()

        course1 = models.Course()
        course1.course_department = "COMPSCI"
        course1.course_id = "100"
        course1.save()

        course2 = models.Course()
        course2.course_department = "COMPSCI"
        course2.course_id = "150"
        course2.save()

        lists = Commands.access_info()
        users = lists[0]
        self.assertTrue(ad1 in users)
        self.assertTrue(sup1 in users)
        self.assertTrue(inst1 in users)
        self.assertTrue(ta1 in users)
        courses = lists[1]
        self.assertTrue(course1 in courses)
        self.assertTrue(course2 in courses)
