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

    def test_multi_users(self):

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

        response = client.get('/edit_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Current Email:")
        self.assertContains(response, "ta_assign_admin@uwm.edu")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_multi_users_online(self):

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

        response = client.get('/edit_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Current Email:")
        self.assertContains(response, "ta_assign_admin@uwm.edu")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

        response2 = client2.get('/edit_info/')
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, "Edit Info")
        self.assertContains(response2, "Current Email:")
        self.assertContains(response2, "ta_assign_super@uwm.edu")
        all_messages2 = [msg for msg in get_messages(response2.wsgi_request)]
        self.assertEqual(len(all_messages2), 0)

    def test_user_big_email(self):

        ad1 = models.User()
        ad1.email = "thereallylongemailaddresslikefiftychars123@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.save()

        client = Client()
        session = client.session
        session['email'] = 'thereallylongemailaddresslikefiftychars123@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/edit_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Current Email:")
        self.assertContains(response, "thereallylongemailaddresslikefiftychars123@uwm.edu")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_user_small_email(self):

        ad1 = models.User()
        ad1.email = "a@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.save()

        client = Client()
        session = client.session
        session['email'] = 'a@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/edit_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Current Email:")
        self.assertContains(response, "a@uwm.edu")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_user_big_password(self):

        ad1 = models.User()
        ad1.email = "ta_assign_admin@uwm.edu"
        ad1.password = "bigol20charpassword1"
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
        self.assertContains(response, "Current Password:")
        self.assertContains(response, "bigol20charpassword1")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_user_small_password(self):

        ad1 = models.User()
        ad1.email = "ta_assign_admin@uwm.edu"
        ad1.password = "1"
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
        self.assertContains(response, "Current Password:")
        self.assertContains(response, "1")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_user_big_name(self):

        ad1 = models.User()
        ad1.email = "ta_assign_admin@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.name = "John Jacob Jingle Heimer Schmitenhoffenvuelerstein"
        ad1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/edit_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Current Name:")
        self.assertContains(response, "John Jacob Jingle Heimer Schmitenhoffenvuelerstein")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_user_small_name(self):

        ad1 = models.User()
        ad1.email = "ta_assign_admin@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.name = "A"
        ad1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/edit_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Current Name:")
        self.assertContains(response, "A")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_user_max_phone(self):

        ad1 = models.User()
        ad1.email = "ta_assign_admin@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.phone = "999.999.9999"
        ad1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/edit_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Current Phone:")
        self.assertContains(response, "999.999.9999")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_user_big_address(self):

        ad1 = models.User()
        ad1.email = "ta_assign_admin@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.address = "123456789123 Longstreetnamed St, Except In The Basement, " \
                      "Really Big Town Name Like So Huge, NY 21221"
        ad1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/edit_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Current Address:")
        self.assertContains(response, "123456789123 Longstreetnamed St, Except In The Basement, "
                                      "Really Big Town Name Like So Huge, NY 21221")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_user_small_address(self):

        ad1 = models.User()
        ad1.email = "ta_assign_admin@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.address = "1"
        ad1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/edit_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Current Address:")
        self.assertContains(response, "1")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)