from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class AssignInstructorLecTests(TestCase):

    def setUp(self):
        return

    def test_proper(self):
        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        inscourse = models.InstructorCourse()
        inscourse.instructor = inst1
        inscourse.course = course
        inscourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        response = Commands.assign_instructor_to_lec(inst1.email, course.course_id, lec.lecture_section,
                                                     course.course_department)
        self.assertEqual(response, "Instructor assigned to lecture")

    def test_valid_double(self):
        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 2
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        inscourse = models.InstructorCourse()
        inscourse.instructor = inst1
        inscourse.course = course
        inscourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        lec2 = models.Lecture()
        lec2.course = course
        lec2.lecture_section = "402"
        lec2.save()

        response = Commands.assign_instructor_to_lec(inst1.email, course.course_id, lec.lecture_section,
                                                     course.course_department)
        self.assertEqual(response, "Instructor assigned to lecture")
        response = Commands.assign_instructor_to_lec(inst1.email, course.course_id, lec2.lecture_section,
                                                     course.course_department)
        self.assertEqual(response, "Instructor assigned to lecture")

    def test_invalid_instructor(self):
        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        inscourse = models.InstructorCourse()
        inscourse.instructor = inst1
        inscourse.course = course
        inscourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        response = Commands.assign_instructor_to_lec("ins1@uwm.edu", course.course_id, lec.lecture_section,
                                                     course.course_department)
        self.assertEqual(response, "no such instructor")

    def test_invalid_course(self):
        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        inscourse = models.InstructorCourse()
        inscourse.instructor = inst1
        inscourse.course = course
        inscourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        response = Commands.assign_instructor_to_lec(inst1.email, "302", lec.lecture_section,
                                                     course.course_department)
        self.assertEqual(response, "no such course")

    def test_invalid_dept(self):
        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        inscourse = models.InstructorCourse()
        inscourse.instructor = inst1
        inscourse.course = course
        inscourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        response = Commands.assign_instructor_to_lec(inst1.email, course.course_id, lec.lecture_section,
                                                     "PHYSICS")
        self.assertEqual(response, "no such course")

    def test_assign_improper_ta(self):
        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        inscourse = models.InstructorCourse()
        inscourse.instructor = inst1
        inscourse.course = course
        inscourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        response = Commands.assign_instructor_to_lec(ta1.email, course.course_id, lec.lecture_section,
                                                     course.course_department)
        self.assertEqual(response, "no such instructor")

    def test_assign_improper_admin(self):
        ad1 = models.User()
        ad1.email = "admin@uwm.edu"
        ad1.type = "administrator"
        ad1.save()

        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        inscourse = models.InstructorCourse()
        inscourse.instructor = inst1
        inscourse.course = course
        inscourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        response = Commands.assign_instructor_to_lec(ad1.email, course.course_id, lec.lecture_section,
                                                     course.course_department)
        self.assertEqual(response, "no such instructor")

    def test_assign_improper_sup(self):
        sup1 = models.User()
        sup1.email = "sup@uwm.edu"
        sup1.type = "supervisor"
        sup1.save()

        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        inscourse = models.InstructorCourse()
        inscourse.instructor = inst1
        inscourse.course = course
        inscourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        response = Commands.assign_instructor_to_lec(sup1.email, course.course_id, lec.lecture_section,
                                                     course.course_department)
        self.assertEqual(response, "no such instructor")

    def test_not_assigned_course(self):
        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        inst2 = models.User()
        inst2.email = "instructor2@uwm.edu"
        inst2.type = "instructor"
        inst2.save()

        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        inscourse = models.InstructorCourse()
        inscourse.instructor = inst1
        inscourse.course = course
        inscourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        response = Commands.assign_instructor_to_lec(inst2.email, course.course_id, lec.lecture_section,
                                                     course.course_department)
        self.assertEqual(response, "Instructor not assigned to this course!")

    def test_invalid_section(self):
        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        inscourse = models.InstructorCourse()
        inscourse.instructor = inst1
        inscourse.course = course
        inscourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        response = Commands.assign_instructor_to_lec(inst1.email, course.course_id, "402",
                                                     course.course_department)
        self.assertEqual(response, "Lecture section does not exist")