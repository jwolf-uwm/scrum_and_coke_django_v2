from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class TestLogin(TestCase):

    def setUp(self):
        self.person1 = models.User()
        self.person1.email = "person1@uwm.edu"
        self.person1.password = "DEFAULT_PASSWORD"
        self.person1.save()

        self.person2 = models.User()
        self.person2.email = "person2@uwm.edu"
        self.person2.password = "DEFAULT_PASSWORD"
        self.person2.save()

    def test_login_correct(self):

        self.assertEquals(Commands.login("person1@uwm.edu", "DEFAULT_PASSWORD"), "Login successful")
        model_person1 = models.User.objects.get(email=self.person1.email)
        self.assertTrue(model_person1.isLoggedOn)

    def test_login_incorrect(self):

        self.assertEquals(Commands.login("snoop@uwm.edu", "password"), "Invalid login info")
        model_person1 = models.User.objects.get(email=self.person1.email)
        self.assertFalse(model_person1.isLoggedOn)

    def test_login_multiple(self):

        self.assertEquals(Commands.login("person1@uwm.edu", "DEFAULT_PASSWORD"), "Login successful")

        model_person1 = models.User.objects.get(email=self.person1.email)
        self.assertTrue(model_person1.isLoggedOn)

        self.assertEquals(Commands.login("person2@uwm.edu", "DEFAULT_PASSWORD"), "Login successful")

        model_person2 = models.User.objects.get(email=self.person2.email)
        self.assertTrue(model_person2.isLoggedOn)

    def test_login_multiple_incorrect(self):

        self.assertEquals(Commands.login("person1@uwm.edu", "DEFAULT_BAD_PASSWORD"), "Invalid login info")

        model_person1 = models.User.objects.get(email=self.person1.email)
        self.assertFalse(model_person1.isLoggedOn)

        self.assertEquals(Commands.login("person2@uwm.edu", "DEFAULT_BAD_PASSWORD"), "Invalid login info")

        model_person2 = models.User.objects.get(email=self.person2.email)
        self.assertFalse(model_person2.isLoggedOn)

    def test_login_multiple_mismatch(self):

        self.assertEquals(Commands.login("person1@uwm.edu", "DEFAULT_BAD_PASSWORD"), "Invalid login info")

        model_person1 = models.User.objects.get(email=self.person1.email)
        self.assertFalse(model_person1.isLoggedOn)

        self.assertEquals(Commands.login("person2@uwm.edu", "DEFAULT_PASSWORD"), "Login successful")

        model_person2 = models.User.objects.get(email=self.person2.email)
        self.assertTrue(model_person2.isLoggedOn)