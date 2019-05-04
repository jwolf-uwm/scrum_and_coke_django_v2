from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class TestDeleteAccount(TestCase):
    def setUp(self):
        return

    def test_delete_account(self):
        # create a test user in the system
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.type = "TA"
        tester.save()
        Commands.delete_account("rando@uwm.edu")
        self.assertEqual(len(models.User.objects.filter(email="rando@uwm.edu")), 0)
