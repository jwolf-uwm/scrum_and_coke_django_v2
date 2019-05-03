from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class TestCreateCourse(TestCase):
    def setUp(self):
        return

    def test_create_course_with_labs(self):
        # create a new course as admin
        self.assertEqual(Commands.create_course("COMPSCI", "361", "1", "2"), "Course created successfully")
        # get the added course from the db
        da_course = models.Course.objects.get(course_id="361")
        # make sure found course is the same
        self.assertEqual(da_course.course_department, "COMPSCI")
        self.assertEqual(da_course.course_id, 361)
        self.assertEqual(da_course.num_lectures, 1)
        self.assertEqual(da_course.num_labs, 2)

        # should find one lecture section
        da_lecture = models.Lecture.objects.filter(course=da_course)
        self.assertEqual(da_lecture[0].lecture_section, "401")
        self.assertEqual(da_lecture[0].course, da_course)
        # shouldn't be able to access any more lectures tied to course
        with self.assertRaises(IndexError):
            print(da_lecture[1])

        # should find two lab sections
        da_labs = models.Lab.objects.filter(course=da_course)
        self.assertEqual(da_labs[0].lab_section, "801")
        self.assertEqual(da_labs[0].course, da_course)
        self.assertEqual(da_labs[1].lab_section, "802")
        self.assertEqual(da_labs[1].course, da_course)

    def test_create_course_without_labs(self):
        # create a new course as admin
        self.assertEqual(Commands.create_course("COMPSCI", "361", "2", "0"), "Course created successfully")
        # get the added course from the db
        da_course = models.Course.objects.get(course_id="361")
        # make sure found course is the same
        self.assertEqual(da_course.course_department, "COMPSCI")
        self.assertEqual(da_course.course_id, 361)
        self.assertEqual(da_course.num_lectures, 2)
        self.assertEqual(da_course.num_labs, 0)

        # should find two lecture section
        da_lecture = models.Lecture.objects.filter(course=da_course)
        self.assertEqual(da_lecture[0].lecture_section, "001")
        self.assertEqual(da_lecture[0].course, da_course)
        self.assertEqual(da_lecture[1].lecture_section, "002")
        self.assertEqual(da_lecture[1].course, da_course)
        # shouldn't be able to access any more lectures tied to course
        with self.assertRaises(IndexError):
            print(da_lecture[2])

        # shouldn't find any lab sections
        with self.assertRaises(models.Lab.DoesNotExist):
            models.Lab.objects.get(course=da_course)

    def test_create_course_again(self):
        Commands.create_course("COMPSCI", "361", "1", "2")
        # create the same course again with no changes
        self.assertEqual(Commands.create_course("COMPSCI", "361", "1", "2"), "Course already exists")
        # create the same course with a different number of labs
        self.assertEqual(Commands.create_course("COMPSCI", "361", "1", "3"), "Course already exists")
        # create the same course with a different section number
        self.assertEqual(Commands.create_course("COMPSCI", "361", "2", "2"), "Course already exists")
        da_course = models.Course.objects.get(course_id="361")
        # make sure found course is the same
        self.assertEqual(da_course.course_department, "COMPSCI")
        self.assertEqual(da_course.course_id, 361)
        self.assertEqual(da_course.num_lectures, 1)
        self.assertEqual(da_course.num_labs, 2)

    def test_create_course_missing_parameters(self):
        with self.assertRaises(TypeError):
            Commands.create_course("COMPSCI")
        # missing course_id/wrong type
        with self.assertRaises(TypeError):
            Commands.create_course(3)

    def test_create_course_bad_department(self):
        self.assertEqual(Commands.create_course("BUTTS", "361", "1", "2"), "That department is not offered")

    def test_create_course_course_id_letters(self):
        self.assertEqual(Commands.create_course("COMPSCI", "3F5", "1", "2"), "Course ID must be a number")

    def test_create_course_course_id_too_big(self):
        self.assertEqual(Commands.create_course("COMPSCI", "1234", "1", "2"),
                         "Course ID must be 3 digits long and between 101 and 999")

    def test_create_course_course_id_too_small(self):
        self.assertEqual(Commands.create_course("COMPSCI", "35", "1", "2"),
                         "Course ID must be 3 digits long and between 101 and 999")

    def test_create_course_num_lectures_letters(self):
        self.assertEqual(Commands.create_course("COMPSCI", "361", "F", "2"),
                         "Number of lecture sections must be a number")

    def test_create_course_num_lectures_too_big(self):
        self.assertEqual(Commands.create_course("COMPSCI", "361", "100", "2"),
                         "Number of lecture sections cannot be less than 1 or greater than 5")

    def test_create_course_num_lectures_zero(self):
        self.assertEqual(Commands.create_course("COMPSCI", "361", "0", "2"),
                         "Number of lecture sections cannot be less than 1 or greater than 5")

    def test_create_course_num_lectures_neg(self):
        self.assertEqual(Commands.create_course("COMPSCI", "361", "-1", "2"),
                         "Number of lecture sections must be a number")

    def test_create_course_num_labs_letters(self):
        self.assertEqual(Commands.create_course("COMPSCI", "361", "3", "G"),
                         "Number of lab sections must be a number")

    def test_create_course_num_labs_too_big(self):
        self.assertEqual(Commands.create_course("COMPSCI", "361", "3", "44"),
                         "Number of lab sections cannot be less than 0 or greater than 5")

    def test_create_course_num_labs_neg(self):
        self.assertEqual(Commands.create_course("COMPSCI", "361", "3", "-32"),
                         "Number of lab sections must be a number")
