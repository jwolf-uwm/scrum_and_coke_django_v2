from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages
from ta_assign import models


class LoginTests(TestCase):

    def setUp(self):
        return

    def test_logout(self):

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.get('/logout/')
        self.assertEqual(response.get('location'), '/login/')

    def test_notin_logout(self):

        client = Client()
        response = client.get('/logout/')
        self.assertEqual(response.get('location'), '/index/')
