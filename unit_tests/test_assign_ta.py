from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class AssignTACourse(TestCase):
    def setUp(self):
        return

    def test_assign_ta_proper(self):
        ta1 = models.User()
        ta1.email = "ta1@uwm.edu"
        ta1.type = "ta"
        ta1.save()
        course1 = models.Course()
        course1.course_id = "CS301-001"
        course1.num_labs = 3
        course1.save()
        proper = Commands.assign_ta(ta1.email, course1.course_id)
        self.assertEqual(proper, "TA Assigned!")

    def test_assign_ta_course_improper_ta(self):
        ta1 = models.User()
        ta1.email = "ta1@uwm.edu"
        ta1.type = "ta"
        ta1.save()
        course1 = models.Course()
        course1.course_id = "CS301-001"
        course1.num_labs = 3
        course1.save()
        proper = Commands.assign_ta("ta2@uwm.edu", course1.course_id)
        self.assertEqual(proper, "no such ta")

    def test_assign_ta_improper_course(self):
        ta1 = models.User()
        ta1.email = "ta1@uwm.edu"
        ta1.type = "ta"
        ta1.save()
        course1 = models.Course()
        course1.course_id = "CS301-001"
        course1.num_labs = 3
        course1.save()
        proper = Commands.assign_ta(ta1.email, "CS302-002")
        self.assertEqual(proper, "no such course")

    def test_assign_ta_admin(self):
        ad1 = models.User()
        ad1.email = "ad1@uwm.edu"
        ad1.type = "administrator"
        ad1.save()
        course1 = models.Course()
        course1.course_id = "CS301-001"
        course1.num_labs = 3
        course1.save()
        proper = Commands.assign_ta(ad1.email, course1.course_id)
        self.assertEqual(proper, "no such ta")

    def test_assign_ta_sup(self):
        sup1 = models.User()
        sup1.email = "sup1@uwm.edu"
        sup1.type = "supervisor"
        sup1.save()
        course1 = models.Course()
        course1.course_id = "CS301-001"
        course1.num_labs = 3
        course1.save()
        proper = Commands.assign_ta(sup1.email, course1.course_id)
        self.assertEqual(proper, "no such ta")

    def test_assign_ta_ins(self):
        ins1 = models.User()
        ins1.email = "ins1@uwm.edu"
        ins1.type = "instructor"
        ins1.save()
        course1 = models.Course()
        course1.course_id = "CS301-001"
        course1.num_labs = 3
        course1.save()
        proper = Commands.assign_ta(ins1.email, course1.course_id)
        self.assertEqual(proper, "no such ta")
    
