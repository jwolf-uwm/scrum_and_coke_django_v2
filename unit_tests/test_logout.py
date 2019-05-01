from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class TestLogout(TestCase):

    def setUp(self):
        self.person1 = models.User()
        self.person1.email = "person1@uwm.edu"
        self.person1.password = "DEFAULT_PASSWORD"
        self.person1.save()

        self.person2 = models.User()
        self.person2.email = "person2@uwm.edu"
        self.person2.password = "DEFAULT_PASSWORD"
        self.person2.save()

    def test_logout_correct(self):
        self.assertEquals(Commands.login("person1@uwm.edu", "DEFAULT_PASSWORD"), "Login successful")
        model_person1 = models.User.objects.get(email=self.person1.email)
        self.assertTrue(model_person1.isLoggedOn)
        self.assertTrue(Commands.logout("person1@uwm.edu"))
        model_person1 = models.User.objects.get(email=self.person1.email)
        self.assertFalse(model_person1.isLoggedOn)

    def test_logout_with_other(self):
        self.assertEquals(Commands.login("person1@uwm.edu", "DEFAULT_PASSWORD"), "Login successful")

        model_person1 = models.User.objects.get(email=self.person1.email)
        self.assertTrue(model_person1.isLoggedOn)

        self.assertEquals(Commands.login("person2@uwm.edu", "DEFAULT_PASSWORD"), "Login successful")

        model_person2 = models.User.objects.get(email=self.person2.email)
        self.assertTrue(model_person2.isLoggedOn)

        self.assertTrue(Commands.logout("person1@uwm.edu"))

        model_person1 = models.User.objects.get(email=self.person1.email)
        self.assertFalse(model_person1.isLoggedOn)

        self.assertTrue(Commands.logout("person2@uwm.edu"))

        model_person2 = models.User.objects.get(email=self.person2.email)
        self.assertFalse(model_person2.isLoggedOn)

    def test_logout_incorrect(self):
        self.assertEquals(Commands.login("person1@uwm.edu", "DEFAULT_BAD_PASSWORD"), "Invalid login info")
        self.assertFalse(Commands.logout("person1@uwm.edu"))

        model_person1 = models.User.objects.get(email=self.person1.email)
        self.assertFalse(model_person1.isLoggedOn)

    def test_logout_incorrect_with_other(self):
        self.assertEquals(Commands.login("person1@uwm.edu", "DEFAULT_BAD_PASSWORD"), "Invalid login info")
        self.assertEquals(Commands.login("person1@uwm.edu", "DEFAULT_BAD_PASSWORD"), "Invalid login info")
        self.assertFalse(Commands.logout("person1@uwm.edu"))
        self.assertFalse(Commands.logout("person2@uwm.edu"))

        model_person1 = models.User.objects.get(email=self.person1.email)
        self.assertFalse(model_person1.isLoggedOn)

        model_person2 = models.User.objects.get(email=self.person2.email)
        self.assertFalse(model_person2.isLoggedOn)

    def test_logout_incorrect_with_mismatch(self):
        self.assertEquals(Commands.login("person1@uwm.edu", "DEFAULT_BAD_PASSWORD"), "Invalid login info")
        self.assertEquals(Commands.login("person2@uwm.edu", "DEFAULT_PASSWORD"), "Login successful")

        model_person1 = models.User.objects.get(email=self.person1.email)
        self.assertFalse(model_person1.isLoggedOn)

        model_person2 = models.User.objects.get(email=self.person2.email)
        self.assertTrue(model_person2.isLoggedOn)

        self.assertFalse(Commands.logout("person1@uwm.edu"))
        self.assertTrue(Commands.logout("person2@uwm.edu"))

    def test_logout_incorrect_no_user(self):
        self.assertFalse(Commands.logout("person1@uwm.edu"))
        self.assertFalse(Commands.logout("person2@uwm.edu"))
