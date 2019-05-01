from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages
from ta_assign import models


class ViewInfoTests(TestCase):

    def setUp(self):
        return

    def test_no_login_get(self):

        client = Client()
        response = client.get('/edit_info/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "Please login first.")
        self.assertEqual(response.get('location'), '/login/')

    def test_admin_get(self):

        ad1 = models.User()
        ad1.email = "ta_assign_admin@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/edit_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Current Email:")
        self.assertContains(response, "ta_assign_admin@uwm.edu")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_super_get(self):

        sup1 = models.User()
        sup1.email = "ta_assign_super@uwm.edu"
        sup1.password = "password"
        sup1.type = "supervisor"
        sup1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()

        response = client.get('/edit_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Current Email:")
        self.assertContains(response, "ta_assign_super@uwm.edu")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_instructor_get(self):

        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.password = "password"
        inst1.save()

        client = Client()
        session = client.session
        session['email'] = 'instructor@uwm.edu'
        session['type'] = 'instructor'
        session.save()

        response = client.get('/edit_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Current Email:")
        self.assertContains(response, "instructor@uwm.edu")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_ta_get(self):

        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.password = "password"
        ta1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta@uwm.edu'
        session['type'] = 'ta'
        session.save()

        response = client.get('/edit_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Current Email:")
        self.assertContains(response, "ta@uwm.edu")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)
