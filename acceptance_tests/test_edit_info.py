from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages
from ta_assign import models


class EditInfoTests(TestCase):

    def setUp(self):
        return

    # get tests

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
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    # email tests

    def test_admin_change_email(self):

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

        response = client.post('/edit_info/', data={'email': "admin@uwm.edu", 'password': "", 'name': "",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Email address changed.")

    def test_super_change_email(self):

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

        response = client.post('/edit_info/', data={'email': "super@uwm.edu", 'password': "", 'name': "",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Email address changed.")

    def test_instructor_change_email(self):

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

        response = client.post('/edit_info/', data={'email': "inst@uwm.edu", 'password': "", 'name': "",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Email address changed.")

    def test_ta_change_email(self):

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

        response = client.post('/edit_info/', data={'email': "tee_ayy@uwm.edu", 'password': "", 'name': "",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Email address changed.")

    def test_bad_email(self):

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

        response = client.post('/edit_info/', data={'email': "admin@uwm.com", 'password': "", 'name': "",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Email address must be uwm address.")

    def test_weird_email(self):

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

        response = client.post('/edit_info/', data={'email': "admin@uwm.edu@uwm.edu", 'password': "", 'name': "",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Email address must be uwm address.")

    def test_taken_email(self):

        ad1 = models.User()
        ad1.email = "ta_assign_admin@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.save()

        sup1 = models.User()
        sup1.email = "ta_assign_super@uwm.edu"
        sup1.password = "password"
        sup1.type = "supervisor"
        sup1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_info/', data={'email': "ta_assign_super@uwm.edu", 'password': "", 'name': "",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Email address taken.")

    def test_multi_user_online_change_email(self):
        ad1 = models.User()
        ad1.email = "ta_assign_admin@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.save()

        sup1 = models.User()
        sup1.email = "ta_assign_super@uwm.edu"
        sup1.password = "password"
        sup1.type = "supervisor"
        sup1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        client2 = Client()
        session2 = client2.session
        session2['email'] = 'ta_assign_super@uwm.edu'
        session2['type'] = 'supervisor'
        session2.save()

        response = client.post('/edit_info/', data={'email': "admin@uwm.edu", 'password': "", 'name': "",
                                                    'phone': "", 'address': ""}, follow="true")
        response2 = client2.post('/edit_info/', data={'email': "super@uwm.edu", 'password': "", 'name': "",
                                                      'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Email address changed.")
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, "Edit Info")
        self.assertContains(response2, "Email address changed.")

    def test_change_email_max(self):

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

        response = client.post('/edit_info/', data={'email': "thereallylongemailaddresslikefiftychars123@uwm.edu",
                                                    'password': "", 'name': "", 'phone': "", 'address': ""},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Email address changed.")

    def test_change_email_min(self):

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

        response = client.post('/edit_info/', data={'email': "a@uwm.edu",
                                                    'password': "", 'name': "", 'phone': "", 'address': ""},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Email address changed.")

    def test_change_email_too_big(self):

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

        response = client.post('/edit_info/', data={'email': "thereallylongemailaddresslikefiftychars1234@uwm.edu",
                                                    'password': "", 'name': "", 'phone': "", 'address': ""},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Email address must be 50 characters or less.")

    def test_change_email_int(self):

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

        response = client.post('/edit_info/', data={'email': "1",
                                                    'password': "", 'name': "", 'phone': "", 'address': ""},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Email address must be uwm address.")

    # password tests

    def test_admin_change_password(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "new_password", 'name': "",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Password changed.")

    def test_super_change_password(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "new_password", 'name': "",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Password changed.")

    def test_instructor_change_password(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "new_password", 'name': "",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Password changed.")

    def test_ta_change_password(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "new_password", 'name': "",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Password changed.")

    def test_change_password_multi_user_online(self):

        ad1 = models.User()
        ad1.email = "ta_assign_admin@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.save()

        sup1 = models.User()
        sup1.email = "ta_assign_super@uwm.edu"
        sup1.password = "password"
        sup1.type = "supervisor"
        sup1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        client2 = Client()
        session2 = client2.session
        session2['email'] = 'ta_assign_super@uwm.edu'
        session2['type'] = 'supervisor'
        session2.save()

        response = client.post('/edit_info/', data={'email': "", 'password': "new_password", 'name': "",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Password changed.")

        response2 = client2.post('/edit_info/', data={'email': "", 'password': "new_password", 'name': "",
                                                      'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, "Edit Info")
        self.assertContains(response2, "Password changed.")

    def test_change_password_max(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "bigol20charpassword1", 'name': "",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Password changed.")

    def test_change_password_min(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "1", 'name': "",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Password changed.")

    def test_change_password_too_big(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "bigol20charpassword11", 'name': "",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Password must be 20 characters or less.")

    # name tests

    def test_admin_change_name(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "Admin",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Name changed.")

    def test_super_change_name(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "Super",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Name changed.")

    def test_instructor_change_name(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "Instructor",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Name changed.")

    def test_ta_change_name(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "TA",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Name changed.")

    def test_big_name(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "Jim Joe Bob Henry Bob Bob",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Name changed.")

    def test_max_name(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "",
                                                    'name': "John Jacob Jingle Heimer Schmitenhoffenvuelerstein",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Name changed.")

    def test_min_name(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "",
                                                    'name': "A",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Name changed.")

    def test_name_too_big(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "",
                                                    'name': "John Jacob Jingle Heimer Schmitenhoffenvuelerstein1",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Name must be 50 characters or less.")

    # phone tests

    def test_admin_change_phone(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': "414.867.5309", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Phone number changed.")

    def test_super_change_phone(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': "414.867.5309", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Phone number changed.")

    def test_instructor_change_phone(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': "414.867.5309", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Phone number changed.")

    def test_ta_change_phone(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': "414.867.5309", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Phone number changed.")

    def test_bad_phone(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': "414-867-5309", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Invalid phone format.")

    def test_bad_phone_two(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': "4148675309", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Invalid phone format.")

    def test_big_phone(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': "9999.9999.99999", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Invalid phone format.")

    def test_max_phone(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': "999.999.9999", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Phone number changed.")

    def test_string_phone(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': "I'M A PHONE NUMBER", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Invalid phone format.")

    def test_admin_change_address(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': "", 'address': "1234 5th Street Milwaukee, WI 53111"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Address changed.")

    def test_super_change_address(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': "", 'address': "1234 5th Street Milwaukee, WI 53111"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Address changed.")

    def test_instructor_change_address(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': "", 'address': "1234 5th Street Milwaukee, WI 53111"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Address changed.")

    def test_ta_change_address(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': "", 'address': "1234 5th Street Milwaukee, WI 53111"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Address changed.")

    def test_multi_user_online_change_address(self):
        ad1 = models.User()
        ad1.email = "ta_assign_admin@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.save()

        sup1 = models.User()
        sup1.email = "ta_assign_super@uwm.edu"
        sup1.password = "password"
        sup1.type = "supervisor"
        sup1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        client2 = Client()
        session2 = client2.session
        session2['email'] = 'ta_assign_super@uwm.edu'
        session2['type'] = 'supervisor'
        session2.save()

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': "", 'address': "1234 5th Street Milwaukee, WI 53111"},
                               follow="true")
        response2 = client2.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                      'phone': "", 'address': "1234 5th Street Milwaukee, WI 53111"},
                                 follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Address changed.")
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, "Edit Info")
        self.assertContains(response2, "Address changed.")

    def test_change_address_max(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "", 'phone': "",
                                                    'address': "123456789123 Longstreetnamed St, Except In The "
                                                               "Basement, Really Big Town Name Like So Huge, NY 21221"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Address changed.")

    def test_change_address_min(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "", 'phone': "",
                                                    'address': "1"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Address changed.")

    def test_change_address_too_big(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "", 'phone': "",
                                                    'address': "1123456789123 Longstreetnamed St, Except In The "
                                                               "Basement, Really Big Town Name Like So Huge, NY 21221"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Address must be 100 characters or less.")

    def test_admin_change_all(self):

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

        response = client.post('/edit_info/', data={'email': "admin@uwm.edu", 'password': "secure_password",
                                                    'name': "Admin Guy", 'phone': "414.111.1111",
                                                    'address': "1234 5th Street Milwaukee, WI 53111"}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Email address changed.")
        self.assertContains(response, "Password changed.")
        self.assertContains(response, "Name changed.")
        self.assertContains(response, "Phone number changed.")
        self.assertContains(response, "Address changed.")

    def test_nothing(self):

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

        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': "", 'address': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "You should pick something to change.")
