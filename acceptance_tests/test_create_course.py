from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages


class CreateCourseTests(TestCase):
    def setUp(self):
        return

    def test_no_login_get(self):
        client = Client()
        response = client.get('/create_course/')
        # this gets any messages
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        # this should be the first and only message, tagged error
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "Please login first.")
        # since we returned a redirect, we can check the location
        self.assertEqual(response.get('location'), '/login/')

    def test_admin_get(self):

        client = Client()
        # make a session, email and type are all you need
        session = client.session
        session['email'] = 'admin@uwm.edu'
        session['type'] = 'administrator'
        # save the session
        session.save()
        response = client.get('/create_course/')
        # status code 200, we loaded the correct page
        self.assertEqual(response.status_code, 200)
        # since we returned a render, it has all the content of the page
        # we'll just look for the header
        self.assertContains(response, "Create Course")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        # no error messages
        self.assertEqual(len(all_messages), 0)

    def test_super_get(self):

        client = Client()
        session = client.session
        session['email'] = 'super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.get('/create_course/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_instructor_get(self):

        client = Client()
        session = client.session
        session['email'] = 'inst@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.get('/create_course/')
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
        response = client.get('/create_course/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "You do not have access to this page.")
        self.assertEqual(response.get('location'), '/index/')

    def test_create_course_admin(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.post('/create_course/', data={'course_department': "COMPSCI", 'course_id': "361",
                                                        'num_lectures': "3", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "Course created successfully")

    def test_create_course_supervisor(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/create_course/', data={'course_department': "COMPSCI", 'course_id': "361",
                                                        'num_lectures': "3", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "Course created successfully")

    def test_create_course_already_exists(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_department': "COMPSCI", 'course_id': "361",
                                                        'num_lectures': "3", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "Course created successfully")

        response = client.post('/create_course/', data={'course_department': "COMPSCI", 'course_id': "361",
                                                        'num_lectures': "3", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "Course already exists")

    def test_create_course_bad_department(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_department': "CHILDAFFAIRS", 'course_id': "361",
                                                        'num_lectures': "3", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "That department is not offered")

    def test_create_course_course_id_letters(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_department': "COMPSCI", 'course_id': "ABC",
                                                        'num_lectures': "3", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "Course ID must be a number")

    def test_create_course_course_id_too_big(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_department': "COMPSCI", 'course_id': "1234",
                                                        'num_lectures': "3", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "Course ID must be 3 digits long and between 101 and 999")

    def test_create_course_course_id_too_small(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_department': "COMPSCI", 'course_id': "12",
                                                        'num_lectures': "3", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "Course ID must be 3 digits long and between 101 and 999")

    def test_create_course_num_lectures_letters(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_department': "COMPSCI", 'course_id': "361",
                                                        'num_lectures': "A", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "Number of lecture sections must be a number")

    def test_create_course_num_lectures_too_big(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_department': "COMPSCI", 'course_id': "361",
                                                        'num_lectures': "12", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "Number of lecture sections cannot be less than 1 or greater than 5")

    def test_create_course_num_lectures_zero(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_department': "COMPSCI", 'course_id': "361",
                                                        'num_lectures': "0", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "Number of lecture sections cannot be less than 1 or greater than 5")

    def test_create_course_num_lectures_neg(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_department': "COMPSCI", 'course_id': "361",
                                                        'num_lectures': "-1", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "Number of lecture sections must be a number")

    def test_create_course_num_labs_letters(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_department': "COMPSCI", 'course_id': "361",
                                                        'num_lectures': "3", 'num_labs': "A"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "Number of lab sections must be a number")

    def test_create_course_num_labs_too_big(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_department': "COMPSCI", 'course_id': "361",
                                                        'num_lectures': "3", 'num_labs': "31"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "Number of lab sections cannot be less than 0 or greater than 5")

    def test_create_course_num_labs_neg(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_department': "COMPSCI", 'course_id': "361",
                                                        'num_lectures': "3", 'num_labs': "-3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "Number of lab sections must be a number")
