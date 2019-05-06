from django.test import TestCase
from ta_assign import models
from classes.commands import Commands

class AssignTaTests(TestCase):

    def setUp(self):
        return

    def test_ins_post_lec(self):
        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        course = models.Course()
        course.num_labs = 0
        course.current_num_TA = 1
        course.num_lectures = 1
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        inscourse = models.InstructorCourse()
        inscourse.instructor = inst1
        inscourse.course = course
        inscourse.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()
        response = Commands.assign_ta_to_lablec(inst1.email, ta1.email, course.course_id, lec.lecture_section,
                                                course.course_department)
        self.assertEqual(response, "TA Assigned to Lecture!")

    def test_super_post_lec(self):
        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        sup1 = models.User()
        sup1.email = "ta_assign_super@uwm.edu"
        sup1.type = "supervisor"
        sup1.save()

        course = models.Course()
        course.num_labs = 0
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "ta@uwm.edu", 'course_id': "301",
                                             'course_department': "COMPSCI", 'course_section': "401"}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA")
        self.assertContains(response, "TA Assigned to Lecture!")

    def test_ins_post_lab(self):
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
        course.current_num_TA = 1
        course.num_lectures = 1
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        inscourse = models.InstructorCourse()
        inscourse.instructor = inst1
        inscourse.course = course
        inscourse.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lab()
        lec.course = course
        lec.lab_section = "801"
        lec.save()
        client = Client()
        session = client.session
        session['email'] = 'instructor@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "ta@uwm.edu", 'course_id': "301",
                                        'course_department': "COMPSCI", 'course_section': "801"}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA to Labs/Lectures")
        self.assertContains(response, "TA Assigned to Lab!")

    def test_super_post_lab(self):
        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        sup1 = models.User()
        sup1.email = "ta_assign_super@uwm.edu"
        sup1.type = "supervisor"
        sup1.save()

        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 1
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lab()
        lec.course = course
        lec.lab_section = "801"
        lec.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "ta@uwm.edu", 'course_id': "301",
                                             'course_department': "COMPSCI", 'course_section': "801"}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA")
        self.assertContains(response, "TA Assigned to Lab!")

    def test_invalid_ta_ins(self):
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
        course.current_num_TA = 1
        course.num_lectures = 1
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        inscourse = models.InstructorCourse()
        inscourse.instructor = inst1
        inscourse.course = course
        inscourse.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lab()
        lec.course = course
        lec.lab_section = "801"
        lec.save()
        client = Client()
        session = client.session
        session['email'] = 'instructor@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "ta3@uwm.edu", 'course_id': "301",
                                                           'course_department': "COMPSCI", 'course_section': "801"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA to Labs/Lectures")
        self.assertContains(response, "no such ta")

    def test_invalid_ta_sup(self):
        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        sup1 = models.User()
        sup1.email = "ta_assign_super@uwm.edu"
        sup1.type = "supervisor"
        sup1.save()

        course = models.Course()
        course.num_labs = 0
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "ta3@uwm.edu", 'course_id': "301",
                                                           'course_department': "COMPSCI", 'course_section': "401"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA to Labs/Lectures")
        self.assertContains(response, "no such ta")

    def test_invalid_course_ins(self):
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
        course.current_num_TA = 1
        course.num_lectures = 1
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        inscourse = models.InstructorCourse()
        inscourse.instructor = inst1
        inscourse.course = course
        inscourse.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lab()
        lec.course = course
        lec.lab_section = "801"
        lec.save()
        client = Client()
        session = client.session
        session['email'] = 'instructor@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "ta@uwm.edu", 'course_id': "302",
                                                           'course_department': "COMPSCI", 'course_section': "801"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA to Labs/Lectures")
        self.assertContains(response, "no such course")

    def test_invalid_course_sup(self):
        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        sup1 = models.User()
        sup1.email = "ta_assign_super@uwm.edu"
        sup1.type = "supervisor"
        sup1.save()

        course = models.Course()
        course.num_labs = 0
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "ta@uwm.edu", 'course_id': "302",
                                                           'course_department': "COMPSCI", 'course_section': "401"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA to Labs/Lectures")
        self.assertContains(response, "no such course")

    def test_invalid_course_department_sup(self):
        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        sup1 = models.User()
        sup1.email = "ta_assign_super@uwm.edu"
        sup1.type = "supervisor"
        sup1.save()

        course = models.Course()
        course.num_labs = 0
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "ta@uwm.edu", 'course_id': "301",
                                                           'course_department': "PHYSICS", 'course_section': "401"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA to Labs/Lectures")
        self.assertContains(response, "no such course")

    def test_invalid_course_department_ins(self):
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
        course.current_num_TA = 1
        course.num_lectures = 1
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        inscourse = models.InstructorCourse()
        inscourse.instructor = inst1
        inscourse.course = course
        inscourse.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lab()
        lec.course = course
        lec.lab_section = "801"
        lec.save()
        client = Client()
        session = client.session
        session['email'] = 'instructor@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "ta@uwm.edu", 'course_id': "301",
                                                           'course_department': "PHYSICS", 'course_section': "801"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA to Labs/Lectures")
        self.assertContains(response, "no such course")

    def test_assign_improper_ins_ins(self):
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
        course.current_num_TA = 1
        course.num_lectures = 1
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        inscourse = models.InstructorCourse()
        inscourse.instructor = inst1
        inscourse.course = course
        inscourse.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lab()
        lec.course = course
        lec.lab_section = "801"
        lec.save()
        client = Client()
        session = client.session
        session['email'] = 'instructor@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "instructor@uwm.edu", 'course_id': "301",
                                                           'course_department': "COMPSCI", 'course_section': "801"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA to Labs/Lectures")
        self.assertContains(response, "no such ta")

    def test_improper_ins_sup(self):
        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        sup1 = models.User()
        sup1.email = "ta_assign_super@uwm.edu"
        sup1.type = "supervisor"
        sup1.save()

        course = models.Course()
        course.num_labs = 0
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "instructor@uwm.edu", 'course_id': "301",
                                                           'course_department': "COMPSCI", 'course_section': "401"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA to Labs/Lectures")
        self.assertContains(response, "no such ta")

    def test_assign_improper_admin_sup(self):
        ad1 = models.User()
        ad1.email = "admin@uwm.edu"
        ad1.type = "administrator"
        ad1.save()

        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        sup1 = models.User()
        sup1.email = "ta_assign_super@uwm.edu"
        sup1.type = "supervisor"
        sup1.save()

        course = models.Course()
        course.num_labs = 0
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "ad1@uwm.edu", 'course_id': "301",
                                                           'course_department': "COMPSCI", 'course_section': "401"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA to Labs/Lectures")
        self.assertContains(response, "no such ta")

    def test_improper_admin_ins(self):
        ad1 = models.User()
        ad1.email = "admin@uwm.edu"
        ad1.type = "administrator"
        ad1.save()

        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        sup1 = models.User()
        sup1.email = "ta_assign_super@uwm.edu"
        sup1.type = "supervisor"
        sup1.save()

        course = models.Course()
        course.num_labs = 0
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "admin@uwm.edu", 'course_id': "301",
                                                           'course_department': "COMPSCI", 'course_section': "401"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA to Labs/Lectures")
        self.assertContains(response, "no such ta")

    def test_assign_improper_sup_ins(self):
        sup1 = models.User()
        sup1.email = "sup@uwm.edu"
        sup1.type = "supervisor"
        sup1.save()

        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        sup1 = models.User()
        sup1.email = "ta_assign_super@uwm.edu"
        sup1.type = "supervisor"
        sup1.save()

        course = models.Course()
        course.num_labs = 0
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "sup@uwm.edu", 'course_id': "301",
                                                           'course_department': "COMPSCI", 'course_section': "401"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA to Labs/Lectures")
        self.assertContains(response, "no such ta")

    def test_assign_sup_sup(self):

        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        sup1 = models.User()
        sup1.email = "ta_assign_super@uwm.edu"
        sup1.type = "supervisor"
        sup1.save()

        course = models.Course()
        course.num_labs = 0
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "ta_assign_super@uwm.edu", 'course_id': "301",
                                                           'course_department': "COMPSCI", 'course_section': "401"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA to Labs/Lectures")
        self.assertContains(response, "no such ta")

    def test_not_assigned_to_course_ins(self):
        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        inst3 = models.User()
        inst3.email = "instructor3@uwm.edu"
        inst3.type = "instructor"
        inst3.save()

        course = models.Course()
        course.num_labs = 0
        course.current_num_TA = 1
        course.num_lectures = 1
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        inscourse = models.InstructorCourse()
        inscourse.instructor = inst1
        inscourse.course = course
        inscourse.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()
        client = Client()
        session = client.session
        session['email'] = 'instructor3@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "ta@uwm.edu", 'course_id': "301",
                                                           'course_department': "COMPSCI", 'course_section': "401"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA to Labs/Lectures")
        self.assertContains(response, "You are not assigned to this course")

    def test_ta_not_assigned_sup(self):
        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        sup1 = models.User()
        sup1.email = "ta_assign_super@uwm.edu"
        sup1.type = "supervisor"
        sup1.save()

        course = models.Course()
        course.num_labs = 0
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        course1 = models.Course()
        course1.num_labs = 0
        course1.current_num_TA = 0
        course1.num_lectures = 1
        course1.instructor = "DEFAULT"
        course1.course_id = "302"
        course1.course_department = "COMPSCI"
        course1.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "ta@uwm.edu", 'course_id': "302",
                                                           'course_department': "COMPSCI", 'course_section': "401"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA")
        self.assertContains(response, "TA not assigned to this course!")

    def test_ta_not_assigned_ins(self):
        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        course = models.Course()
        course.num_labs = 0
        course.current_num_TA = 1
        course.num_lectures = 1
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        course1 = models.Course()
        course1.num_labs = 0
        course1.current_num_TA = 0
        course1.num_lectures = 1
        course1.instructor = "DEFAULT"
        course1.course_id = "302"
        course1.course_department = "COMPSCI"
        course1.save()

        inscourse = models.InstructorCourse()
        inscourse.instructor = inst1
        inscourse.course = course
        inscourse.save()

        inscourse1= models.InstructorCourse()
        inscourse1.instructor = inst1
        inscourse1.course = course1
        inscourse1.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()
        client = Client()
        session = client.session
        session['email'] = 'instructor@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "ta@uwm.edu", 'course_id': "302",
                                                           'course_department': "COMPSCI", 'course_section': "401"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA to Labs/Lectures")
        self.assertContains(response, "TA not assigned to this course!")

    def test_no_lab_or_lec_ins(self):
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
        course.current_num_TA = 1
        course.num_lectures = 1
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        inscourse = models.InstructorCourse()
        inscourse.instructor = inst1
        inscourse.course = course
        inscourse.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lab()
        lec.course = course
        lec.lab_section = "801"
        lec.save()
        client = Client()
        session = client.session
        session['email'] = 'instructor@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "ta@uwm.edu", 'course_id': "301",
                                                           'course_department': "COMPSCI", 'course_section': "804"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA to Labs/Lectures")
        self.assertContains(response, "No Such Lab or Lecture")

    def test_no_such_lab_or_lec_sup(self):
        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        sup1 = models.User()
        sup1.email = "ta_assign_super@uwm.edu"
        sup1.type = "supervisor"
        sup1.save()

        course = models.Course()
        course.num_labs = 0
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "ta@uwm.edu", 'course_id': "301",
                                                           'course_department': "COMPSCI", 'course_section': "404"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA")
        self.assertContains(response, "No Such Lab or Lecture")

    def test_invalid_lec_assign_sup(self):
        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        sup1 = models.User()
        sup1.email = "ta_assign_super@uwm.edu"
        sup1.type = "supervisor"
        sup1.save()

        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "ta@uwm.edu", 'course_id': "301",
                                                           'course_department': "COMPSCI", 'course_section': "401"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA")
        self.assertContains(response, "TA cannot be assigned to this lecture(labs exist)!")

    def test_invalid_lec_assign_ins(self):
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
        course.current_num_TA = 1
        course.num_lectures = 1
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        inscourse = models.InstructorCourse()
        inscourse.instructor = inst1
        inscourse.course = course
        inscourse.save()

        tacourse = models.TACourse()
        tacourse.TA = ta1
        tacourse.course = course
        tacourse.save()

        lec = models.Lecture()
        lec.course = course
        lec.lecture_section = "401"
        lec.save()
        client = Client()
        session = client.session
        session['email'] = 'instructor@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.post('/assign_ta_lablec/', data={'email': "ta@uwm.edu", 'course_id': "301",
                                                           'course_department': "COMPSCI", 'course_section': "401"},
                               follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign TA to Labs/Lectures")
        self.assertContains(response, "TA cannot be assigned to this lecture(labs exist)!")