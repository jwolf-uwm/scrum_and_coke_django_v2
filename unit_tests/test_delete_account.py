from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class TestDeleteAccount(TestCase):
    def setUp(self):
        return

    def test_delete_account_exists_TA(self):
        # create a test user in the system
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.type = "TA"
        tester.save()

        self.assertEqual(Commands.delete_account("rando@uwm.edu"), "rando@uwm.edu has been deleted successfully")
        self.assertEqual(len(models.User.objects.filter(email="rando@uwm.edu")), 0)

    def test_delete_account_not_exists_TA(self):
        # create a test user in the system
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.type = "TA"
        tester.save()

        self.assertEqual(Commands.delete_account("randomboy@uwm.edu"), "Such User does not exist")

    def test_delete_account_after_delete_TA(self):
        # create a test user in the system
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.type = "TA"
        tester.save()

        self.assertEqual(Commands.delete_account("rando@uwm.edu"), "rando@uwm.edu has been deleted successfully")
        self.assertEqual(Commands.delete_account("rando@uwm.edu"), "Such User does not exist")
        self.assertEqual(len(models.User.objects.filter(email="rando@uwm.edu")), 0)

    def test_delete_account_exists_instructor(self):
        # create a test user in the system
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.type = "instructor"
        tester.save()

        self.assertEqual(Commands.delete_account("rando@uwm.edu"), "rando@uwm.edu has been deleted successfully")
        self.assertEqual(len(models.User.objects.filter(email="rando@uwm.edu")), 0)

    def test_delete_account_not_exists_instructor(self):
        # create a test user in the system
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.type = "instructor"
        tester.save()

        self.assertEqual(Commands.delete_account("randomboy@uwm.edu"), "Such User does not exist")

    def test_delete_account_after_delete_instructor(self):
        # create a test user in the system
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.type = "instructor"
        tester.save()

        self.assertEqual(Commands.delete_account("rando@uwm.edu"), "rando@uwm.edu has been deleted successfully")
        self.assertEqual(Commands.delete_account("rando@uwm.edu"), "Such User does not exist")
        self.assertEqual(len(models.User.objects.filter(email="rando@uwm.edu")), 0)

    def test_delete_account_after_TA_assign(self):

        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.type = "TA"

        tester.save()
        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        lab = models.Lab()
        lab.TA = tester.email
        lab.course = course
        lab.lab_section = 499
        lab.save()

        self.assertEqual(Commands.delete_account("rando@uwm.edu"), "rando@uwm.edu has been deleted successfully")
        self.assertEqual(len(models.User.objects.filter(email="rando@uwm.edu")), 0)
        self.assertEqual(models.Lab.objects.get(lab_section=499).TA, "no TA")

    def test_delete_account_after_instructor_assign(self):

        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.type = "instructor"
        tester.save()

        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        lecture = models.Lecture()
        lecture.instructor = tester.email
        lecture.course = course
        lecture.lecture_section = 499
        lecture.save()

        self.assertEqual(Commands.delete_account("rando@uwm.edu"), "rando@uwm.edu has been deleted successfully")
        self.assertEqual(len(models.User.objects.filter(email="rando@uwm.edu")), 0)
        self.assertEqual(models.Lecture.objects.get(lecture_section=499).instructor, "no instructor")
