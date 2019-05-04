from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class TestAccessinfo(TestCase):

    def setUp(self):
        return

    def test_admin_only(self):
        ad1 = models.User()
        ad1.email = "admin@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.save()

        lists = Commands.access_info()
        users = lists[0]
        self.assertEquals(users[0], ad1)
