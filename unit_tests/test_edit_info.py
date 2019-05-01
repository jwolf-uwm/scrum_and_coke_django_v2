from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class TestEditInfo(TestCase):
    # TODO: split up these unit tests

    def setUp(self):
        self.person1 = models.User()
        self.person1.email = "person1@uwm.edu"
        self.person1.password = "DEFAULT_PASSWORD"
        self.person1.save()

        self.person2 = models.User()
        self.person2.email = "person2@uwm.edu"
        self.person2.password = "DEFAULT_PASSWORD"
        self.person2.save()

    def test_change_password(self):
        self.assertEquals(Commands.change_password("person1@uwm.edu", "password"), "Password changed.")
        person1 = models.User.objects.get(email="person1@uwm.edu")
        self.assertEquals(person1.password, "password")
        self.assertNotEquals(person1.password, "DEFAULT_PASSWORD")

    def test_change_email(self):
        self.assertEquals(Commands.change_email("person1@uwm.edu", "snoop@uwm.edu"), "Email address changed.")
        person1 = models.User.objects.get(email="snoop@uwm.edu")
        self.assertEquals(person1.email, "snoop@uwm.edu")
        self.assertNotEquals(person1.email, "person1@uwm.edu")
        self.assertEquals(Commands.change_email("snoop@uwm.edu", "snoop@gmail.com"),
                          "Email address must be uwm address.")
        self.assertEquals(Commands.change_email("snoop@uwm.edu", "no_at_symbol_or_dot_something"),
                          "Email address must be uwm address.")
        self.assertEquals(Commands.change_email("person1@uwm.edu", "person2@uwm.edu"), "Email address taken.")

    def test_change_phone(self):
        self.assertEquals(Commands.change_phone("person1@uwm.edu", "414.414.4141"), "Phone number changed.")
        self.person1 = models.User.objects.get(email="person1@uwm.edu")
        self.assertEquals(self.person1.phone, "414.414.4141")
        self.assertNotEquals(self.person1.phone, "000.000.0000")
        self.assertEquals(Commands.change_phone("person1@uwm.edu", "1234567890"), "Invalid phone format.")
        self.assertEquals(Commands.change_phone("person1@uwm.edu", "414-414-4141"), "Invalid phone format.")
        self.assertEquals(Commands.change_phone("person1@uwm.edu", "(414)414-4141"), "Invalid phone format.")
        self.assertEquals(Commands.change_phone("person1@uwm.edu", "abc.abc.abcd"), "Invalid phone format.")
        self.assertEquals(Commands.change_phone("person1@uwm.edu", "1234.1234.1234"), "Invalid phone format.")

    def test_change_name(self):
        self.assertEquals(Commands.change_name("person1@uwm.edu", "Snoop Doggy Dog"), "Name changed.")
        self.person1 = models.User.objects.get(email="person1@uwm.edu")
        self.assertEquals(self.person1.name, "Snoop Doggy Dog")
        self.assertNotEquals(self.person1.name, "DEFAULT")
