from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class TestPublicInfo(TestCase):

    def setUp(self):
        return

    def test_no_info(self):
        users = Commands.read_public()
        self.assertEquals(len(users), 0)

    def test_admin_only(self):
        ad1 = models.User()
        ad1.email = "admin@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.save()

        users = Commands.read_public()
        self.assertEquals(users[0], ad1)

    def test_super_only(self):
        sup1 = models.User()
        sup1.email = "super@uwm.edu"
        sup1.password = "password"
        sup1.type = "supervisor"
        sup1.save()

        users = Commands.read_public()
        self.assertEquals(users[0], sup1)

    def test_inst_only(self):
        inst1 = models.User()
        inst1.email = "inst1@uwm.edu"
        inst1.password = "password"
        inst1.type = "instructor"
        inst1.save()

        users = Commands.read_public()
        self.assertEquals(users[0], inst1)

    def test_ta_only(self):
        ta1 = models.User()
        ta1.email = "ta1@uwm.edu"
        ta1.password = "password"
        ta1.type = "ta"
        ta1.save()

        users = Commands.read_public()
        self.assertEquals(users[0], ta1)

    def test_admin_super_default(self):
        ad1 = models.User()
        ad1.email = "admin@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.save()

        sup1 = models.User()
        sup1.email = "super@uwm.edu"
        sup1.password = "password"
        sup1.type = "supervisor"
        sup1.save()

        users = Commands.read_public()
        self.assertEquals(users[0], ad1)
        self.assertEquals(users[1], sup1)

    def test_each_user(self):
        ad1 = models.User()
        ad1.email = "admin@uwm.edu"
        ad1.password = "password"
        ad1.type = "administrator"
        ad1.save()

        sup1 = models.User()
        sup1.email = "super@uwm.edu"
        sup1.password = "password"
        sup1.type = "supervisor"
        sup1.save()

        inst1 = models.User()
        inst1.email = "inst1@uwm.edu"
        inst1.password = "password"
        inst1.type = "instructor"
        inst1.save()

        ta1 = models.User()
        ta1.email = "ta1@uwm.edu"
        ta1.password = "password"
        ta1.type = "ta"
        ta1.save()

        users = Commands.read_public()
        self.assertEquals(users[0], ad1)
        self.assertEquals(users[1], sup1)
        self.assertEquals(users[2], inst1)
        self.assertEquals(users[3], ta1)
