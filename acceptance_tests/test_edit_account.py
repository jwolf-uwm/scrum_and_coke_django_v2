from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages
from ta_assign import models


class EditAccountTests(TestCase):

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
        response = client.get('/edit_account/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "Please login first.")
        self.assertEqual(response.get('location'), '/login/')

    def test_admin_get(self):
        client = Client()
        session = client.session
        session['email'] = 'admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.get('/edit_account/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_super_get(self):
        client = Client()
        session = client.session
        session['email'] = 'super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.get('/edit_account/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_instructor_get(self):
        client = Client()
        session = client.session
        session['email'] = 'inst@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.get('/edit_account/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "You do not have access to this page.")
        self.assertEqual(response.get('location'), '/index/')

    def test_ta_get(self):
        client = Client()
        session = client.session
        session['email'] = 'ta@uwm.edu'
        session['type'] = 'ta'
        session.save()
        response = client.get('/edit_account/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "You do not have access to this page.")
        self.assertEqual(response.get('location'), '/index/')

    def test_admin_edit_admin_email(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "email",
                                                       'data': "new_email@uwm.edu"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_admin_edit_admin_password(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "password",
                                                       'data': "new_password"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_admin_edit_admin_name(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "name",
                                                       'data': "Dr. John Tang Boyland"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_admin_edit_admin_phone(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "phone",
                                                       'data': "414.123.4567"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_admin_edit_admin_address(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "address",
                                                       'data': "NEW FRICKEN ADDRESS MAN"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_admin_edit_super_email(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_super@uwm.edu", 'field': "email",
                                                       'data': "new_email@uwm.edu"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_admin_edit_super_password(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_super@uwm.edu", 'field': "password",
                                                       'data': "new_password"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_admin_edit_super_name(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_super@uwm.edu", 'field': "name",
                                                       'data': "Dr. John Tang Boyland"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_admin_edit_super_phone(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_super@uwm.edu", 'field': "phone",
                                                       'data': "414.123.4567"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_admin_edit_super_address(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_super@uwm.edu", 'field': "address",
                                                       'data': "NEW FRICKEN ADDRESS MAN"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_admin_edit_instructor_email(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "instructor@uwm.edu", 'field': "email",
                                                       'data': "new_email@uwm.edu"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_admin_edit_instructor_password(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "instructor@uwm.edu", 'field': "password",
                                                       'data': "new_password"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_admin_edit_instructor_name(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "instructor@uwm.edu", 'field': "name",
                                                       'data': "Dr. John Tang Boyland"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_admin_edit_instructor_phone(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "instructor@uwm.edu", 'field': "phone",
                                                       'data': "414.123.4567"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_admin_edit_instructor_address(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "instructor@uwm.edu", 'field': "address",
                                                       'data': "NEW FRICKEN ADDRESS MAN"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_admin_edit_ta_email(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta@uwm.edu", 'field': "email",
                                                       'data': "new_email@uwm.edu"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_admin_edit_ta_password(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta@uwm.edu", 'field': "password",
                                                       'data': "new_password"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_admin_edit_ta_name(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta@uwm.edu", 'field': "name",
                                                       'data': "Dr. John Tang Boyland"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_admin_edit_ta_phone(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta@uwm.edu", 'field': "phone",
                                                       'data': "414.123.4567"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_admin_edit_ta_address(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta@uwm.edu", 'field': "address",
                                                       'data': "NEW FRICKEN ADDRESS MAN"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_super_edit_admin_email(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "email",
                                                       'data': "new_email@uwm.edu"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_super_edit_admin_password(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "password",
                                                       'data': "new_password"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_super_edit_admin_name(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "name",
                                                       'data': "Dr. John Tang Boyland"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_super_edit_admin_phone(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "phone",
                                                       'data': "414.123.4567"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_super_edit_admin_address(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "address",
                                                       'data': "NEW FRICKEN ADDRESS MAN"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_super_edit_super_email(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_super@uwm.edu", 'field': "email",
                                                       'data': "new_email@uwm.edu"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_super_edit_super_password(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_super@uwm.edu", 'field': "password",
                                                       'data': "new_password"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_super_edit_super_name(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_super@uwm.edu", 'field': "name",
                                                       'data': "Dr. John Tang Boyland"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_super_edit_super_phone(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_super@uwm.edu", 'field': "phone",
                                                       'data': "414.123.4567"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_super_edit_super_address(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_super@uwm.edu", 'field': "address",
                                                       'data': "NEW FRICKEN ADDRESS MAN"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_super_edit_instructor_email(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "instructor@uwm.edu", 'field': "email",
                                                       'data': "new_email@uwm.edu"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_super_edit_instructor_password(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "instructor@uwm.edu", 'field': "password",
                                                       'data': "new_password"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_super_edit_instructor_name(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "instructor@uwm.edu", 'field': "name",
                                                       'data': "Dr. John Tang Boyland"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_super_edit_instructor_phone(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "instructor@uwm.edu", 'field': "phone",
                                                       'data': "414.123.4567"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_super_edit_instructor_address(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "instructor@uwm.edu", 'field': "address",
                                                       'data': "NEW FRICKEN ADDRESS MAN"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_super_edit_ta_email(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta@uwm.edu", 'field': "email",
                                                       'data': "new_email@uwm.edu"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_super_edit_ta_password(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta@uwm.edu", 'field': "password",
                                                       'data': "new_password"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_super_edit_ta_name(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta@uwm.edu", 'field': "name",
                                                       'data': "Dr. John Tang Boyland"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_super_edit_ta_phone(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta@uwm.edu", 'field': "phone",
                                                       'data': "414.123.4567"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_super_edit_ta_address(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta@uwm.edu", 'field': "address",
                                                       'data': "NEW FRICKEN ADDRESS MAN"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "User has been updated successfully")

    def test_edit_bad_email(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "email",
                                                       'data': "BAD_EMAIL@uwm.com"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Entered email does not end in uwm.edu")

    def test_edit_bad_email_too_many_args(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "email",
                                                       'data': "BAD_EMAIL@uwm.edu otherstuff"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Entered email does not end in uwm.edu")

    def test_edit_bad_phone_too_long(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "phone",
                                                       'data': "123.123.12345"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Phone number is not of the correct form (###.###.####)")

    def test_edit_bad_phone_too_short(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "phone",
                                                       'data': "123.123.123"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Phone number is not of the correct form (###.###.####)")

    def test_edit_bad_phone_wrong_format(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "phone",
                                                       'data': "123-123-1234"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Phone number is not of the correct form (###.###.####)")

    def test_edit_bad_phone_non_digits(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "phone",
                                                       'data': "123.123.ABCD"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Phone number is not of the correct form (###.###.####)")

    def test_edit_bad_phone_too_many_args(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "phone",
                                                       'data': "123.123.1234 otherstuff"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Phone number is not of the correct form (###.###.####)")

    def test_edit_account_bad_field(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "nombre",
                                                       'data': "Dr. John Tang Boyland"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "The entered data field does not exist")
