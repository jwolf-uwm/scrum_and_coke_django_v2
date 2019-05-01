from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class TestViewInfo(TestCase):

    def setUp(self):
        self.person1 = models.User()
        self.person1.email = "person1@uwm.edu"
        self.person1.password = "DEFAULT_PASSWORD"
        self.person1.save()

        self.person2 = models.User()
        self.person2.email = "person2@uwm.edu"
        self.person2.password = "DEFAULT_PASSWORD"
        self.person2.save()

    def test_view_info(self):
        self.assertEquals(Commands.view_info("person1@uwm.edu"),
                          ["person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT", "000.000.0000"])
        self.assertEquals(Commands.view_info("person2@uwm.edu"),
                          ["person2@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT", "000.000.0000"])
