from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages
from ta_assign import models


class DeleteAccountTests(TestCase):

    def setUp(self):
        admin = models.User()
        admin.email = "ta_assign_admin@uwm.edu"
        admin.type = "administrator"
        admin.save()

        supervisor = models.User()
        supervisor.email = "ta_assign_super@uwm.edu"
        supervisor.type = "supervisor"
        supervisor.save()

        instructor = models.User()
        instructor.email = "instructor@uwm.edu"
        instructor.password = "instructor"
        instructor.name = "DEFAULT"
        instructor.phone = "000.000.0000"
        instructor.type = "instructor"
        instructor.isLoggedOn = False
        instructor.save()

        ta = models.User()
        ta.email = "ta@uwm.edu"
        ta.password = "ta"
        ta.name = "DEFAULT"
        ta.phone = "000.000.0000"
        ta.type = "ta"
        ta.isLoggedOn = False
        ta.save()

    def test_no_login_get(self):
        client = Client()
        response = client.get('/delete_account/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "Please login first.")
        self.assertEqual(response.get('location'), '/login/')
