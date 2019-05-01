from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class TestCreateAccount(TestCase):
    def setUp(self):
        return

    def test_create_course_as_administrator(self):
        # create a new course as admin
        self.assertEqual(Commands.create_course("CS361-401", 3), "Course created successfully")
        # get the added course from the db
        da_course = models.Course.objects.get(course_id="CS361-401")
        # make sure found course is the same
        self.assertEqual(da_course.course_id, "CS361-401")
        self.assertEqual(da_course.num_labs, 3)
        self.assertEqual(da_course.instructor, "no Instructor")

    def test_create_course_again(self):
        Commands.create_course("CS361-401", 3)
        # create the same course again with no changes
        self.assertEqual(Commands.create_course("CS361-401", 3), "Course already exists")
        # create the same course with a different number of labs
        self.assertEqual(Commands.create_course("CS361-401", 2), "Course already exists")
        # create the same course with a different section number (technically a new course)
        self.assertEqual(Commands.create_course("CS361-402", 3), "Course created successfully")
        da_course = models.Course.objects.get(course_id="CS361-402")
        # make sure found course is the same
        self.assertEqual(da_course.course_id, "CS361-402")
        self.assertEqual(da_course.num_labs, 3)
        self.assertEqual(da_course.instructor, "no Instructor")

    def test_create_course_missing_parameters(self):
        with self.assertRaises(TypeError):
            Commands.create_course("CS101-401")
        # missing course_id/wrong type
        with self.assertRaises(TypeError):
            Commands.create_course(3)

    def test_create_course_long_course_id(self):
        # course_id too long and not right format
        self.assertEqual(Commands.create_course("totally_a_good_course_id", 2),
                         "course_id is the wrong size to be of the right form (CS###-###)")

    def test_create_course_course_id_incorrect(self):
        # course_id missing CS at beginning
        self.assertEqual(Commands.create_course("123456789", 2), "course_id is not a CS course (CS###-###)")
        # course_id does not start with uppercase CS
        self.assertEqual(Commands.create_course("cs361-401", 2), "course_id is not a CS course (CS###-###)")
        # course_id doesn't have only numbers for course number
        self.assertEqual(Commands.create_course("CS3F4-321", 2),
                         "The course number contains an invalid digit (CS###-###)")
        # course_id doesn't have a hyphen to separate course number and section number
        self.assertEqual(Commands.create_course("CS3611234", 2),
                         "The course and section number should be separated by a hyphen (CS###-###)")
        # course_id doesn't have only numbers for section number
        self.assertEqual(Commands.create_course("CS361-1F3", 2),
                         "The section number contains an invalid digit (CS###-###)")

    def test_create_course_bad_num_sections(self):
        # number of sections too big
        self.assertEqual(Commands.create_course("CS361-401", 99),
                         "The number of lab sections should be positive and not exceed 5")
        # number of sections is less than 0
        self.assertEqual(Commands.create_course("CS361-401", -1),
                         "The number of lab sections should be positive and not exceed 5")
