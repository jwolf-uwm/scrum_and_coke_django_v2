from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages
from ta_assign import models
import datetime


class EditLecLabTest(TestCase):
    def setUp(self):
        course1 = models.Course()
        course1.course_department = "COMPSCI"
        course1.course_id = 361
        course1.num_lectures = 1
        course1.num_labs = 1
        course1.save()

        lec1 = models.Lecture()
        lec1.course = course1
        lec1.lecture_section = "401"
        lec1.lecture_location = "Somewhere"
        lec1.lecture_time = datetime.time(12, 00)
        lec1.save()

        lab1 = models.Lecture()
        lab1.course = course1
        lab1.lab_section = "801"
        lab1.lab_location = "Somewhere"
        lab1.lab_time = datetime.time(12, 00)
        lab1.save()

    def test_no_login_get(self):
        client = Client()
        response = client.get('/edit_lec_lab/')
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
        response = client.get('/edit_lec_lab/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Lecture/Lab")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_super_get(self):
        client = Client()
        session = client.session
        session['email'] = 'super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.get('/edit_lec_lab/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Lecture/Lab")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_instructor_get(self):
        client = Client()
        session = client.session
        session['email'] = 'inst@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.get('/edit_lec_lab/')
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
        response = client.get('/edit_lec_lab/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "You do not have access to this page.")
        self.assertEqual(response.get('location'), '/index/')

    def test_edit_lecture_location_and_time(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_lec_lab/', data={'course_department': "COMPSCI", 'course_id': "361",
                                                       'section': "lecture", 'section_id': "401",
                                                       'location': "New Location", 'time': "02:08"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Lecture/Lab")
        self.assertContains(response, "Section has been edited successfully")

    def test_edit_lecture_location(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_lec_lab/', data={'course_department': "COMPSCI", 'course_id': "361",
                                                       'section': "lecture", 'section_id': "401",
                                                       'location': "New Location", 'time': ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Lecture/Lab")
        self.assertContains(response, "Section has been edited successfully")

    def test_edit_lecture_time(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_lec_lab/', data={'course_department': "COMPSCI", 'course_id': "361",
                                                       'section': "lecture", 'section_id': "401",
                                                       'location': "", 'time': "02:08"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Lecture/Lab")
        self.assertContains(response, "Section has been edited successfully")

    def test_edit_lecture_location_and_bad_time(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_lec_lab/', data={'course_department': "COMPSCI", 'course_id': "361",
                                                       'section': "lecture", 'section_id': "401",
                                                       'location': "New Location", 'time': "New Time"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Lecture/Lab")
        self.assertContains(response, "Bad time format (HH:MM)")

    def test_edit_lecture_location_and_more_bad_time(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_lec_lab/', data={'course_department': "COMPSCI", 'course_id': "361",
                                                       'section': "lecture", 'section_id': "401",
                                                       'location': "New Location", 'time': "24:00"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Lecture/Lab")
        self.assertContains(response, "Bad time format (HH:MM)")

    def test_edit_lecture_bad_dept(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_lec_lab/', data={'course_department': "BAD DEPT", 'course_id': "361",
                                                       'section': "lecture", 'section_id': "401",
                                                       'location': "New Location", 'time': "24:00"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Lecture/Lab")
        self.assertContains(response, "That department is not offered")

    def test_edit_lecture_bad_course_id(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_lec_lab/', data={'course_department': "COMPSCI", 'course_id': "BAD",
                                                       'section': "lecture", 'section_id': "401",
                                                       'location': "New Location", 'time': "24:00"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Lecture/Lab")
        self.assertContains(response, "Course ID must be a number")

    def test_edit_lecture_course_dne(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_lec_lab/', data={'course_department': "COMPSCI", 'course_id': "333",
                                                       'section': "lecture", 'section_id': "401",
                                                       'location': "New Location", 'time': "24:00"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Lecture/Lab")
        self.assertContains(response, "That course does not exist")

    def test_edit_lecture_bad_section_type(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_lec_lab/', data={'course_department': "COMPSCI", 'course_id': "361",
                                                       'section': "BADNESS", 'section_id': "401",
                                                       'location': "New Location", 'time': "24:00"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Lecture/Lab")
        self.assertContains(response, "Invalid section type")

    def test_edit_lecture_section_dne(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_lec_lab/', data={'course_department': "COMPSCI", 'course_id': "361",
                                                       'section': "lecture", 'section_id': "123",
                                                       'location': "New Location", 'time': "24:00"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Lecture/Lab")
        self.assertContains(response, "That lecture does not exist")

    def test_edit_lecture_bad_section_id(self):
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_lec_lab/', data={'course_department': "COMPSCI", 'course_id': "361",
                                                       'section': "lecture", 'section_id': "BAD",
                                                       'location': "New Location", 'time': "24:00"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Lecture/Lab")
        self.assertContains(response, "Section ID must be a number")
