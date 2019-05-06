from django.test import TestCase
from ta_assign import models
from classes.commands import Commands
import datetime


class TestEditLecLab(TestCase):
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

    def test_edit_lecture_location_and_time(self):
        self.assertEqual(Commands.edit_lec_lab("COMPSCI", "361", "lecture", "401", "NEW LOCATION", "02:08"),
                         "Section has been edited successfully.")
        course = models.Course.objects.get(course_id="361")
        lec1 = models.Lecture.objects.get(course=course, lecture_section="401")
        self.assertEqual(lec1.lecture_location, "NEW LOCATION")
        self.assertEqual(lec1.lecture_time, datetime.time(2, 8))

    def test_edit_lecture_location(self):
        self.assertEqual(Commands.edit_lec_lab("COMPSCI", "361", "lecture", "401", "NEW LOCATION", ""),
                         "Section has been edited successfully.")
        course = models.Course.objects.get(course_id="361")
        lec1 = models.Lecture.objects.get(course=course, lecture_section="401")
        self.assertEqual(lec1.lecture_location, "NEW LOCATION")
        self.assertEqual(lec1.lecture_time, datetime.time(12, 0))

    def test_edit_lecture_time(self):
        self.assertEqual(Commands.edit_lec_lab("COMPSCI", "361", "lecture", "401", "", "02:08"),
                         "Section has been edited successfully.")
        course = models.Course.objects.get(course_id="361")
        lec1 = models.Lecture.objects.get(course=course, lecture_section="401")
        self.assertEqual(lec1.lecture_location, "Somewhere")
        self.assertEqual(lec1.lecture_time, datetime.time(2, 8))

##########################################################################################
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
