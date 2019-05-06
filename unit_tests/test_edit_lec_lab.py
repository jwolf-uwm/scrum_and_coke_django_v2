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

        lab1 = models.Lab()
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

    def test_edit_lecture_location_and_bad_time(self):
        self.assertEqual(Commands.edit_lec_lab("COMPSCI", "361", "lecture", "401", "NEW LOCATION", "BAD"),
                         "Bad time format (HH:MM)")
        course = models.Course.objects.get(course_id="361")
        lec1 = models.Lecture.objects.get(course=course, lecture_section="401")
        self.assertEqual(lec1.lecture_location, "NEW LOCATION")
        self.assertEqual(lec1.lecture_time, datetime.time(12, 0))

    def test_edit_lecture_location_and_more_bad_time(self):
        self.assertEqual(Commands.edit_lec_lab("COMPSCI", "361", "lecture", "401", "NEW LOCATION", "24:00"),
                         "Bad time format (HH:MM)")
        course = models.Course.objects.get(course_id="361")
        lec1 = models.Lecture.objects.get(course=course, lecture_section="401")
        self.assertEqual(lec1.lecture_location, "NEW LOCATION")
        self.assertEqual(lec1.lecture_time, datetime.time(12, 0))

    def test_edit_lecture_bad_dept(self):
        self.assertEqual(Commands.edit_lec_lab("BAD DEPT", "361", "lecture", "401", "NEW LOCATION", "02:08"),
                         "That department is not offered")
        course = models.Course.objects.get(course_id="361")
        lec1 = models.Lecture.objects.get(course=course, lecture_section="401")
        self.assertEqual(lec1.lecture_location, "Somewhere")
        self.assertEqual(lec1.lecture_time, datetime.time(12, 0))

    def test_edit_lecture_bad_course_id(self):
        self.assertEqual(Commands.edit_lec_lab("COMPSCI", "BAD", "lecture", "401", "NEW LOCATION", "02:08"),
                         "Course ID must be a number")

    def test_edit_lecture_course_dne(self):
        self.assertEqual(Commands.edit_lec_lab("COMPSCI", "333", "lecture", "401", "NEW LOCATION", "02:08"),
                         "That course does not exist")

    def test_edit_lecture_bad_section_type(self):
        self.assertEqual(Commands.edit_lec_lab("COMPSCI", "361", "badness", "401", "NEW LOCATION", "02:08"),
                         "Invalid section type")

    def test_edit_lecture_section_dne(self):
        self.assertEqual(Commands.edit_lec_lab("COMPSCI", "361", "lecture", "411", "NEW LOCATION", "02:08"),
                         "That lecture does not exist")

    def test_edit_lecture_bad_section_id(self):
        self.assertEqual(Commands.edit_lec_lab("COMPSCI", "361", "lecture", "BAD", "NEW LOCATION", "02:08"),
                         "Section ID must be a number")

    def test_edit_lab_location_and_time(self):
        self.assertEqual(Commands.edit_lec_lab("COMPSCI", "361", "lab", "801", "NEW LOCATION", "02:08"),
                         "Section has been edited successfully.")
        course = models.Course.objects.get(course_id="361")
        lab1 = models.Lab.objects.get(course=course, lab_section="801")
        self.assertEqual(lab1.lab_location, "NEW LOCATION")
        self.assertEqual(lab1.lab_time, datetime.time(2, 8))

    def test_edit_lab_location(self):
        self.assertEqual(Commands.edit_lec_lab("COMPSCI", "361", "lab", "801", "NEW LOCATION", ""),
                         "Section has been edited successfully.")
        course = models.Course.objects.get(course_id="361")
        lab1 = models.Lab.objects.get(course=course, lab_section="801")
        self.assertEqual(lab1.lab_location, "NEW LOCATION")
        self.assertEqual(lab1.lab_time, datetime.time(12, 0))

    def test_edit_lab_time(self):
        self.assertEqual(Commands.edit_lec_lab("COMPSCI", "361", "lab", "801", "", "02:08"),
                         "Section has been edited successfully.")
        course = models.Course.objects.get(course_id="361")
        lab1 = models.Lab.objects.get(course=course, lab_section="801")
        self.assertEqual(lab1.lab_location, "Somewhere")
        self.assertEqual(lab1.lab_time, datetime.time(2, 8))

    def test_edit_lab_location_and_bad_time(self):
        self.assertEqual(Commands.edit_lec_lab("COMPSCI", "361", "lab", "801", "NEW LOCATION", "BAD"),
                         "Bad time format (HH:MM)")
        course = models.Course.objects.get(course_id="361")
        lab1 = models.Lab.objects.get(course=course, lab_section="801")
        self.assertEqual(lab1.lab_location, "NEW LOCATION")
        self.assertEqual(lab1.lab_time, datetime.time(12, 0))

    def test_edit_lab_location_and_more_bad_time(self):
        self.assertEqual(Commands.edit_lec_lab("COMPSCI", "361", "lab", "801", "NEW LOCATION", "24:00"),
                         "Bad time format (HH:MM)")
        course = models.Course.objects.get(course_id="361")
        lab1 = models.Lab.objects.get(course=course, lab_section="801")
        self.assertEqual(lab1.lab_location, "NEW LOCATION")
        self.assertEqual(lab1.lab_time, datetime.time(12, 0))

    def test_edit_lab_bad_dept(self):
        self.assertEqual(Commands.edit_lec_lab("BAD DEPT", "361", "lab", "801", "NEW LOCATION", "02:08"),
                         "That department is not offered")
        course = models.Course.objects.get(course_id="361")
        lab1 = models.Lab.objects.get(course=course, lab_section="801")
        self.assertEqual(lab1.lab_location, "Somewhere")
        self.assertEqual(lab1.lab_time, datetime.time(12, 0))

    def test_edit_lab_bad_course_id(self):
        self.assertEqual(Commands.edit_lec_lab("COMPSCI", "BAD", "lab", "801", "NEW LOCATION", "02:08"),
                         "Course ID must be a number")

    def test_edit_lab_course_dne(self):
        self.assertEqual(Commands.edit_lec_lab("COMPSCI", "333", "lab", "801", "NEW LOCATION", "02:08"),
                         "That course does not exist")

    def test_edit_lab_bad_section_type(self):
        self.assertEqual(Commands.edit_lec_lab("COMPSCI", "361", "badness", "801", "NEW LOCATION", "02:08"),
                         "Invalid section type")

    def test_edit_lab_section_dne(self):
        self.assertEqual(Commands.edit_lec_lab("COMPSCI", "361", "lab", "811", "NEW LOCATION", "02:08"),
                         "That lab does not exist")

    def test_edit_lab_bad_section_id(self):
        self.assertEqual(Commands.edit_lec_lab("COMPSCI", "361", "lab", "BAD", "NEW LOCATION", "02:08"),
                         "Section ID must be a number")
