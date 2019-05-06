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
        self.assertContains(response, "Administrator")
        self.assertContains(response, "ta_assign_admin@uwm.edu")

    def test_access_info_super(self):

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()

        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Supervisor")
        self.assertContains(response, "ta_assign_super@uwm.edu")

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
        self.assertContains(response, "Instructors")
        self.assertContains(response, "instructor@uwm.edu")

    def test_access_info_instructor_inst_page(self):
        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.name = "Bob"
        inst1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/instructor/instructor@uwm.edu/')
        self.assertContains(response, "Instructor: Bob")

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
        self.assertContains(response, "TAs")
        self.assertContains(response, "ta@uwm.edu")

    def test_access_info_ta_ta_page(self):

        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.name = "Ted"
        ta1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/ta/ta@uwm.edu/')
        self.assertContains(response, "TA: Ted")

    def test_access_info_course(self):
        course1 = models.Course()
        course1.course_dept_id = "COMPSCI100"
        course1.instructor = "instructor@uwm.edu"
        course1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "COMPSCI100")

    def test_access_info_inst_course_coursepage(self):

        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.name = "Bob"
        inst1.save()

        course1 = models.Course()
        course1.course_dept_id = "COMPSCI100"
        course1.instructor = "instructor@uwm.edu"
        course1.save()

        inst1_course1 = models.InstructorCourse()
        inst1_course1.instructor = inst1
        inst1_course1.course = course1
        inst1_course1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/course/COMPSCI100/')
        self.assertContains(response, "Course: COMPSCI100")
        self.assertContains(response, "Bob")

    def test_access_info_inst_course_instpage(self):

        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.name = "Bob"
        inst1.save()

        course1 = models.Course()
        course1.course_department = "COMPSCI"
        course1.course_id = "100"
        course1.course_dept_id = "COMPSCI100"
        course1.instructor = "instructor@uwm.edu"
        course1.save()

        inst1_course1 = models.InstructorCourse()
        inst1_course1.instructor = inst1
        inst1_course1.course = course1
        inst1_course1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/instructor/instructor@uwm.edu/')
        self.assertContains(response, "Instructor: Bob")
        self.assertContains(response, "COMPSCI100")

    def test_access_info_ta_course_coursepage(self):

        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.name = "Ted"
        ta1.save()

        course1 = models.Course()
        course1.course_department = "COMPSCI"
        course1.course_id = "100"
        course1.course_dept_id = "COMPSCI100"
        course1.ta = "ta@uwm.edu"
        course1.save()

        ta1_course1 = models.TACourse()
        ta1_course1.TA = ta1
        ta1_course1.course = course1
        ta1_course1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/course/COMPSCI100/')
        self.assertContains(response, "Course: COMPSCI100")
        self.assertContains(response, "Ted")

    def test_access_info_ta_course_tapage(self):

        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.name = "Ted"
        ta1.save()

        course1 = models.Course()
        course1.course_department = "COMPSCI"
        course1.course_id = "100"
        course1.course_dept_id = "COMPSCI100"
        course1.ta = "ta@uwm.edu"
        course1.save()

        ta1_course1 = models.TACourse()
        ta1_course1.TA = ta1
        ta1_course1.course = course1
        ta1_course1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/ta/ta@uwm.edu/')
        self.assertContains(response, "TA: Ted")
        self.assertContains(response, "COMPSCI100")

    def test_access_info_inst_course_lecture_coursepage(self):

        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.name = "Bob"
        inst1.save()

        course1 = models.Course()
        course1.course_department = "COMPSCI"
        course1.course_id = "100"
        course1.course_dept_id = "COMPSCI100"
        course1.instructor = "instructor@uwm.edu"
        course1.num_lectures = 1
        course1.current_num_lectures = 1
        course1.save()

        inst1_course1 = models.InstructorCourse()
        inst1_course1.instructor = inst1
        inst1_course1.course = course1
        inst1_course1.save()

        lecture1 = models.Lecture()
        lecture1.instructor = "instructor@uwm.edu"
        lecture1.course = course1
        lecture1.lecture_section = "401"
        lecture1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/course/COMPSCI100/')
        self.assertContains(response, "Lectures")
        self.assertContains(response, "COMPSCI100-401")

    def test_access_info_inst_course_lecture_instpage(self):

        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.name = "Bob"
        inst1.save()

        course1 = models.Course()
        course1.course_department = "COMPSCI"
        course1.course_id = "100"
        course1.course_dept_id = "COMPSCI100"
        course1.instructor = "instructor@uwm.edu"
        course1.num_lectures = 1
        course1.current_num_lectures = 1
        course1.save()

        inst1_course1 = models.InstructorCourse()
        inst1_course1.instructor = inst1
        inst1_course1.course = course1
        inst1_course1.save()

        lecture1 = models.Lecture()
        lecture1.instructor = "instructor@uwm.edu"
        lecture1.course = course1
        lecture1.lecture_section = "401"
        lecture1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/instructor/instructor@uwm.edu/')
        self.assertContains(response, "Lectures")
        self.assertContains(response, "COMPSCI100-401")

    def test_access_info_ta_course_lecture_coursepage(self):

        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.name = "Ted"
        ta1.save()

        course1 = models.Course()
        course1.course_department = "COMPSCI"
        course1.course_id = "100"
        course1.course_dept_id = "COMPSCI100"
        course1.TA = "ta@uwm.edu"
        course1.num_lectures = 1
        course1.current_num_lectures = 1
        course1.save()

        ta1_course1 = models.TACourse()
        ta1_course1.TA = ta1
        ta1_course1.course = course1
        ta1_course1.save()

        lecture1 = models.Lecture()
        lecture1.TA = "ta@uwm.edu"
        lecture1.course = course1
        lecture1.lecture_section = "401"
        lecture1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/course/COMPSCI100/')
        self.assertContains(response, "Lectures")
        self.assertContains(response, "COMPSCI100-401")

    def test_access_info_ta_course_lecture_tapage(self):

        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.name = "Ted"
        ta1.save()

        course1 = models.Course()
        course1.course_department = "COMPSCI"
        course1.course_id = "100"
        course1.course_dept_id = "COMPSCI100"
        course1.TA = "ta@uwm.edu"
        course1.num_lectures = 1
        course1.current_num_lectures = 1
        course1.save()

        ta1_course1 = models.TACourse()
        ta1_course1.TA = ta1
        ta1_course1.course = course1
        ta1_course1.save()

        lecture1 = models.Lecture()
        lecture1.TA = "ta@uwm.edu"
        lecture1.course = course1
        lecture1.lecture_section = "401"
        lecture1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/ta/ta@uwm.edu/')
        self.assertContains(response, "Lectures")
        self.assertContains(response, "COMPSCI100-401")

    def test_access_info_ta_course_lab_coursepage(self):

        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.name = "Ted"
        ta1.save()

        course1 = models.Course()
        course1.course_department = "COMPSCI"
        course1.course_id = "100"
        course1.course_dept_id = "COMPSCI100"
        course1.TA = "ta@uwm.edu"
        course1.num_labs = 1
        course1.current_num_labs = 1
        course1.save()

        ta1_course1 = models.TACourse()
        ta1_course1.TA = ta1
        ta1_course1.course = course1
        ta1_course1.save()

        lecture1 = models.Lab()
        lecture1.TA = "ta@uwm.edu"
        lecture1.course = course1
        lecture1.lab_section = "801"
        lecture1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/course/COMPSCI100/')
        self.assertContains(response, "Labs")
        self.assertContains(response, "COMPSCI100-801")

    def test_access_info_ta_course_lab_tapage(self):

        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.name = "Ted"
        ta1.save()

        course1 = models.Course()
        course1.course_department = "COMPSCI"
        course1.course_id = "100"
        course1.course_dept_id = "COMPSCI100"
        course1.TA = "ta@uwm.edu"
        course1.num_labs = 1
        course1.current_num_labs = 1
        course1.save()

        ta1_course1 = models.TACourse()
        ta1_course1.TA = ta1
        ta1_course1.course = course1
        ta1_course1.save()

        lecture1 = models.Lab()
        lecture1.TA = "ta@uwm.edu"
        lecture1.course = course1
        lecture1.lab_section = "801"
        lecture1.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/ta/ta@uwm.edu/')
        self.assertContains(response, "Labs")
        self.assertContains(response, "COMPSCI100-801")

