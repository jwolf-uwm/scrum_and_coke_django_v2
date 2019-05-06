from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages
from ta_assign import models


class TestViewTAAssign(TestCase):

    def setUp(self):
        ad1 = models.User()
        ad1.email = "ta_assign_admin@uwm.edu"
        ad1.type = "administrator"
        ad1.save()

        sup1 = models.User()
        sup1.email = "ta_assign_super@uwm.edu"
        sup1.type = "supervisor"
        sup1.save()

    def test_no_login_get(self):

        client = Client()
        response = client.get('/view_ta_assign/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "Please login first.")
        self.assertEqual(response.get('location'), '/login/')

    def test_admin_get(self):

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/view_ta_assign/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "You do not have access to this page.")
        self.assertEqual(response.get('location'), '/index/')

    def test_super_get(self):

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()

        response = client.get('/view_ta_assign/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "You do not have access to this page.")
        self.assertEqual(response.get('location'), '/index/')

    def test_view_ta_assign_instructor(self):

        client = Client()
        session = client.session
        session['email'] = 'inst@uwm.edu'
        session['type'] = 'instructor'
        session.save()

        response = client.get('/view_ta_assign/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        info_string = str(all_messages)
        self.assertEqual(info_string, "[]")

    def test_view_ta_assign_ta(self):

        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta@uwm.edu'
        session['type'] = 'ta'
        session.save()

        response = client.get('/view_ta_assign/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        info_string = str(all_messages[0])
        self.assertEqual(info_string, "TA: DEFAULT | ta@uwm.edu | 000.000.0000\n\n")

    def test_view_ta_assign_instructor_no_ta(self):

        client = Client()
        session = client.session
        session['email'] = 'instructor@uwm.edu'
        session['type'] = 'instructor'
        session.save()

        response = client.get('/view_ta_assign/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        info_string = str(all_messages)
        self.assertEqual(info_string, "[]")

    def test_view_ta_assign_ta_no_class(self):

        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta@uwm.edu'
        session['type'] = 'ta'
        session.save()

        response = client.get('/view_ta_assign/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        info_string = str(all_messages[0])
        self.assertEqual(info_string, "TA: DEFAULT | ta@uwm.edu | 000.000.0000\n\n")

    def test_view_ta_assign_inst_one_course(self):

        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        course1 = models.TACourse()
        course1.course.course_dept_id_id = "CS101-401"
        course1.course.instructor = "instructor@uwm.edu"
        course1.TA = ta1
        course1.save()

        client = Client()
        session = client.session
        session['email'] = 'instructor@uwm.edu'
        session['type'] = 'instructor'
        session.save()

        response = client.get('/view_ta_assign/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        info_string = str(all_messages[0])
        self.assertEqual(info_string, "TA: DEFAULT | ta@uwm.edu | 000.000.0000\n\tCourse: CS101-401\n\n")

    def test_view_ta_assign_ta_one_course(self):

        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        course1 = models.TACourse()
        course1.course.course_dept_id = "CS101-401"
        course1.course.instructor = "instructor@uwm.edu"
        course1.TA = ta1
        course1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta@uwm.edu'
        session['type'] = 'ta'
        session.save()

        response = client.get('/view_ta_assign/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        info_string = str(all_messages[0])
        self.assertEqual(info_string, "TA: DEFAULT | ta@uwm.edu | 000.000.0000\n\tCourse: CS101-401\n\n")

    def test_view_ta_assign_all_the_things(self):

        ta = models.User()
        ta.email = "ta@uwm.edu"
        ta.type = "ta"
        ta.save()

        ta1 = models.User()
        ta1.email = "ta1@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        ta2 = models.User()
        ta2.email = "ta2@uwm.edu"
        ta2.type = "ta"
        ta2.save()

        inst1 = models.User()
        inst1.email = "inst1@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        inst2 = models.User()
        inst2.email = "inst2@uwm.edu"
        inst2.type = "instructor"
        inst2.save()

        course1 = models.TACourse()
        course1.course.course_dept_id = "CS101-401"
        course1.course.instructor = "inst1@uwm.edu"
        course1.TA = ta1
        course1.save()

        course2 = models.TACourse()
        course2.course.course_dept_id = "CS102-402"
        course2.course.instructor = "inst2@uwm.edu"
        course2.TA = ta2
        course2.save()

        client = Client()
        session = client.session
        session['email'] = 'ta@uwm.edu'
        session['type'] = 'ta'
        session.save()

        response = client.get('/view_ta_assign/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        info_string = str(all_messages[0])
        self.assertEqual(info_string, "TA: DEFAULT | ta@uwm.edu | 000.000.0000\n\n"
                                      "TA: DEFAULT | ta1@uwm.edu | 000.000.0000\n"
                                      "\tCourse: CS101-401\n\n"
                                      "TA: DEFAULT | ta2@uwm.edu | 000.000.0000\n"
                                      "\tCourse: CS102-401\n\n")
