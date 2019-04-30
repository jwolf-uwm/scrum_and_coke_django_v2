from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages
from ta_assign import models


class AccessInfoTests(TestCase):

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
        response = client.get('/access_info/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "Please login first.")
        self.assertEqual(response.get('location'), '/login/')

    def test_instructor_get(self):

        client = Client()
        session = client.session
        session['email'] = 'inst@uwm.edu'
        session['type'] = 'instructor'
        session.save()

        response = client.get('/access_info/')
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

        response = client.get('/access_info/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "You do not have access to this page.")
        self.assertEqual(response.get('location'), '/index/')

    def test_access_info_admin(self):

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        big_string = str(all_messages[0])
        parse_string = big_string.split("\n")
        self.assertEqual(parse_string[0], "Administrator:")
        self.assertEqual(parse_string[1], "DEFAULT | ta_assign_admin@uwm.edu | 000.000.0000")
        self.assertEqual(parse_string[2], "")
        self.assertEqual(parse_string[3], "Supervisor:")
        self.assertEqual(parse_string[4], "DEFAULT | ta_assign_super@uwm.edu | 000.000.0000")

    def test_access_info_super(self):

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()

        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        big_string = str(all_messages[0])
        parse_string = big_string.split("\n")
        self.assertEqual(parse_string[0], "Administrator:")
        self.assertEqual(parse_string[1], "DEFAULT | ta_assign_admin@uwm.edu | 000.000.0000")
        self.assertEqual(parse_string[2], "")
        self.assertEqual(parse_string[3], "Supervisor:")
        self.assertEqual(parse_string[4], "DEFAULT | ta_assign_super@uwm.edu | 000.000.0000")

    def test_access_info_instructor_no_class(self):

        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        big_string = str(all_messages[0])
        parse_string = big_string.split("\n")
        self.assertEqual(parse_string[6], "Instructors:")
        self.assertEqual(parse_string[7], "DEFAULT | instructor@uwm.edu | 000.000.0000")

    def test_access_info_ta_no_class(self):

        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        big_string = str(all_messages[0])
        parse_string = big_string.split("\n")
        self.assertEqual(parse_string[8], "TAs:")
        self.assertEqual(parse_string[9], "DEFAULT | ta@uwm.edu | 000.000.0000")

    def test_access_info_inst_one_course(self):

        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        course1 = models.Course()
        course1.course_id = "CS101-401"
        course1.instructor = "instructor@uwm.edu"
        course1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        big_string = str(all_messages[0])
        parse_string = big_string.split("\n")
        self.assertEqual(parse_string[8], "\tCourse: CS101-401")

    def test_access_info_ta_one_course(self):

        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        course1 = models.Course()
        course1.course_id = "CS101-401"
        course1.instructor = "instructor@uwm.edu"
        course1.save()

        ta1_course1 = models.TACourse()
        ta1_course1.course = course1
        ta1_course1.TA = ta1
        ta1_course1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        big_string = str(all_messages[0])
        parse_string = big_string.split("\n")
        self.assertEqual(parse_string[10], "\tCourse: CS101-401")

    def test_access_info_just_course(self):

        course1 = models.Course()
        course1.course_id = "CS101-401"
        course1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        big_string = str(all_messages[0])
        parse_string = big_string.split("\n")
        self.assertEqual(parse_string[10], "Courses:")
        self.assertEqual(parse_string[11], "CS101-401")

    def test_access_info_all_the_things(self):

        inst1 = models.User()
        inst1.email = "inst1@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        inst2 = models.User()
        inst2.email = "inst2@uwm.edu"
        inst2.type = "instructor"
        inst2.save()

        ta1 = models.User()
        ta1.email = "ta1@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        ta2 = models.User()
        ta2.email = "ta2@uwm.edu"
        ta2.type = "ta"
        ta2.save()

        course1 = models.Course()
        course1.course_id = "CS101-401"
        course1.instructor = "inst1@uwm.edu"
        course1.save()

        course2 = models.Course()
        course2.course_id = "CS102-401"
        course2.instructor = "inst2@uwm.edu"
        course2.save()

        ta1_course1 = models.TACourse()
        ta1_course1.course = course1
        ta1_course1.TA = ta1
        ta1_course1.save()

        ta2_course2 = models.TACourse()
        ta2_course2.course = course2
        ta2_course2.TA = ta2
        ta2_course2.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        big_string = str(all_messages[0])
        parse_info = big_string.split("\n")
        self.assertEqual(parse_info[0], "Administrator:")
        self.assertEqual(parse_info[1], "DEFAULT | ta_assign_admin@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[2], "")
        self.assertEqual(parse_info[3], "Supervisor:")
        self.assertEqual(parse_info[4], "DEFAULT | ta_assign_super@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[5], "")
        self.assertEqual(parse_info[6], "Instructors:")
        self.assertEqual(parse_info[7], "DEFAULT | inst1@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[8], "\tCourse: CS101-401")
        self.assertEqual(parse_info[9], "")
        self.assertEqual(parse_info[10], "DEFAULT | inst2@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[11], "\tCourse: CS102-401")
        self.assertEqual(parse_info[12], "")
        self.assertEqual(parse_info[13], "")
        self.assertEqual(parse_info[14], "TAs:")
        self.assertEqual(parse_info[15], "DEFAULT | ta1@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[16], "\tCourse: CS101-401")
        self.assertEqual(parse_info[17], "")
        self.assertEqual(parse_info[18], "DEFAULT | ta2@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[19], "\tCourse: CS102-401")
        self.assertEqual(parse_info[20], "")
        self.assertEqual(parse_info[21], "")
        self.assertEqual(parse_info[22], "Courses:")
        self.assertEqual(parse_info[23], "CS101-401")
        self.assertEqual(parse_info[24], "CS102-401")
