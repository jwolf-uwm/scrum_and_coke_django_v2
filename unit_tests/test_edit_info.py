from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class TestEditInfo(TestCase):

    def setUp(self):
        person1 = models.User()
        person1.email = "person1@uwm.edu"
        person1.password = "DEFAULT_PASSWORD"
        person1.save()

    def test_change_password(self):
        self.assertEquals(Commands.change_password("person1@uwm.edu", "password"), "Password changed.")
        self.assertEquals(self.person1.password, "password")
        self.assertNotEquals(self.person1.password, "DEFAULT_PASSWORD")
        model_person1 = models.User.objects.get(email=self.person1.email)
        self.assertEquals(model_person1.password, "password")

    def test_change_email(self):
        self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.person2 = Person("goober@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.person1.change_email("snoop@uwm.edu")
        self.assertEquals(self.person1.email, "snoop@uwm.edu")
        self.assertNotEquals(self.person1.email, "person1@uwm.edu")
        model_person1 = models.ModelPerson.objects.get(email=self.person1.email)
        self.assertEquals(model_person1.email, "snoop@uwm.edu")
        self.assertFalse(self.person1.change_email("snoop@gmail.com"))
        self.assertFalse(self.person1.change_email("no_at_symbol_or_dot_something"))
        self.assertFalse(self.person1.change_email("goober@uwm.edu"))

    def test_change_phone(self):
        self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.person1.change_phone("414.414.4141")
        model_person1 = models.ModelPerson.objects.get(email=self.person1.email)
        self.assertEquals(model_person1.phone, "414.414.4141")
        self.assertEquals(self.person1.phone_number, "414.414.4141")
        self.assertNotEquals(self.person1.phone_number, "000.000.0000")
        self.assertFalse(self.person1.change_phone("1234567890"))
        self.assertFalse(self.person1.change_phone("414-414-4141"))
        self.assertFalse(self.person1.change_phone("(414)414-4141"))
        self.assertFalse(self.person1.change_phone("abc.abc.abcd"))
        self.assertFalse(self.person1.change_phone("1234.1234.1234"))

    def test_change_name(self):
        self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.person1.change_name("Snoop Doggy Dog")
        model_person1 = models.ModelPerson.objects.get(email=self.person1.email)
        self.assertEquals(model_person1.name, "Snoop Doggy Dog")
        self.assertEquals(self.person1.name, "Snoop Doggy Dog")
        self.assertNotEquals(self.person1.name, "DEFAULT")