from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages
from ta_assign import models


class ViewCourseAssignmentsTests(TestCase):

    def setUp(self):
        return

    def test_no_login_get(self):

        client = Client()
        response = client.get('/view_course_assignments/')
        # this gets any messages
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        # this should be the first and only message, tagged error
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "Please login first.")
        # since we returned a redirect, we can check the location
        self.assertEqual(response.get('location'), '/login/')

    def test_instructor_get(self):
        inst1 = models.User()
        inst1.email = "inst@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        client = Client()
        session = client.session
        session['email'] = 'inst@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.get('/view_course_assignments/')
        # status code 200, we loaded the correct page
        self.assertEqual(response.status_code, 200)
        # since we returned a render, it has all the content of the page
        # we'll just look for the header
        self.assertContains(response, "Courses Assigned to You:")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        # no error messages
        self.assertEqual(len(all_messages), 0)

    def test_ta_get(self):

        client = Client()
        session = client.session
        session['email'] = 'ta@uwm.edu'
        session['type'] = 'ta'
        session.save()
        response = client.get('/view_course_assignments/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "You do not have access to this page.")
        self.assertEqual(response.get('location'), '/index/')

    def test_admin_get(self):

        client = Client()
        session = client.session
        session['email'] = 'admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.get('/view_course_assignments/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "You do not have access to this page.")
        self.assertEqual(response.get('location'), '/index/')

    def test_sup_get(self):

        client = Client()
        # make a session, email and type are all you need
        session = client.session
        session['email'] = 'sup@uwm.edu'
        session['type'] = 'supervisor'
        # save the session
        session.save()
        response = client.get('/view_course_assignments/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "You do not have access to this page.")
        self.assertEqual(response.get('location'), '/index/')

    def test_add_one_course(self):
        inst1 = models.User()
        inst1.email = "inst@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        course = models.Course()
        course.course_department = "COMPSCI"
        course.course_id = "301"
        course.save()

        insCourse = models.InstructorCourse()
        insCourse.course = course
        insCourse.instructor = inst1
        insCourse.save()

        client = Client()
        session = client.session
        session['email'] = 'inst@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.get('/view_course_assignments/')
        # status code 200, we loaded the correct page
        self.assertEqual(response.status_code, 200)
        # since we returned a render, it has all the content of the page
        # we'll just look for the header
        self.assertContains(response, "Courses Assigned to You:")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        # no error messages
        info_string = str(all_messages[0])
        self.assertEqual(info_string, "COMPSCI: 301 \n")
        self.assertEqual(len(all_messages), 1)

    def test_add_two_course(self):
        inst1 = models.User()
        inst1.email = "inst@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        course = models.Course()
        course.course_department = "COMPSCI"
        course.course_id = "301"
        course.save()

        course2 = models.Course()
        course2.course_department = "COMPSCI"
        course2.course_id = "351"
        course2.save()

        insCourse = models.InstructorCourse()
        insCourse.course = course
        insCourse.instructor = inst1
        insCourse.save()

        insCourse = models.InstructorCourse()
        insCourse.course = course2
        insCourse.instructor = inst1
        insCourse.save()

        client = Client()
        session = client.session
        session['email'] = 'inst@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.get('/view_course_assignments/')
        # status code 200, we loaded the correct page
        self.assertEqual(response.status_code, 200)
        # since we returned a render, it has all the content of the page
        # we'll just look for the header
        self.assertContains(response, "Courses Assigned to You:")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        # no error messages
        info_string = str(all_messages[0])
        self.assertEqual(info_string, "COMPSCI: 301 \nCOMPSCI: 351 \n")
        self.assertEqual(len(all_messages), 1)