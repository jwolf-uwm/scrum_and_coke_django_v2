from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class TestViewInfo(TestCase):

    def setUp(self):
        return

    def test_view_info_person1(self):
        self.person1 = models.User()
        self.person1.email = "person1@uwm.edu"
        self.person1.password = "DEFAULT_PASSWORD"
        self.person1.save()

        self.assertEquals(Commands.view_info("person1@uwm.edu"),
                          ["person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT", "000.000.0000", "not set"])

    def test_view_info_two_users(self):
        self.person1 = models.User()
        self.person1.email = "person1@uwm.edu"
        self.person1.password = "DEFAULT_PASSWORD"
        self.person1.save()

        self.person2 = models.User()
        self.person2.email = "person2@uwm.edu"
        self.person2.password = "DEFAULT_PASSWORD"
        self.person2.save()
        self.assertEquals(Commands.view_info("person2@uwm.edu"),
                          ["person2@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT", "000.000.0000", "not set"])

    def test_view_info_default_admin(self):
        self.ad1 = models.User()
        self.ad1.email = "ta_assign_admin@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "admin"
        self.ad1.save()
        self.assertEquals(Commands.view_info(self.ad1.email),
                          [self.ad1.email, self.ad1.password, self.ad1.name, self.ad1.phone, self.ad1.address])

    def test_view_info_default_super(self):
        self.sup1 = models.User()
        self.sup1.email = "ta_super_admin@uwm.edu"
        self.sup1.password = "password"
        self.sup1.type = "supervisor"
        self.sup1.save()
        self.assertEquals(Commands.view_info(self.sup1.email),
                          [self.sup1.email, self.sup1.password, self.sup1.name, self.sup1.phone, self.sup1.address])

    def test_view_info_default_inst(self):
        self.inst1 = models.User()
        self.inst1.email = "inst1@uwm.edu"
        self.inst1.password = "password"
        self.inst1.type = "instructor"
        self.inst1.save()
        self.assertEquals(Commands.view_info(self.inst1.email),
                          [self.inst1.email, self.inst1.password, self.inst1.name, self.inst1.phone,
                           self.inst1.address])

    def test_view_info_default_ta(self):
        self.ta1 = models.User()
        self.ta1.email = "ta1@uwm.edu"
        self.ta1.password = "password"
        self.ta1.type = "ta"
        self.ta1.save()
        self.assertEquals(Commands.view_info(self.ta1.email),
                          [self.ta1.email, self.ta1.password, self.ta1.name, self.ta1.phone,
                           self.ta1.address])

    def test_view_info_custom_admin(self):
        self.ad1 = models.User()
        self.ad1.email = "the_admin@uwm.edu"
        self.ad1.password = "secure_password"
        self.ad1.type = "administrator"
        self.ad1.name = "Adminbot 4000"
        self.ad1.phone = "414.111.1111"
        self.ad1.address = "1234 5th Street Milwaukee, WI 53111"
        self.ad1.save()
        self.assertEquals(Commands.view_info(self.ad1.email),
                          [self.ad1.email, self.ad1.password, self.ad1.name, self.ad1.phone, self.ad1.address])

    def test_view_info_custom_super(self):
        self.sup1 = models.User()
        self.sup1.email = "super_dude@uwm.edu"
        self.sup1.password = "dudeword"
        self.sup1.type = "supervisor"
        self.sup1.name = "Slurms McKenzie"
        self.sup1.phone = "414.420.2407"
        self.sup1.address = "1234 5th Street Milwaukee, WI 53111"
        self.sup1.save()
        self.assertEquals(Commands.view_info(self.sup1.email),
                          [self.sup1.email, self.sup1.password, self.sup1.name, self.sup1.phone, self.sup1.address])

    def test_view_info_custom_inst(self):
        self.inst1 = models.User()
        self.inst1.email = "instructinator@uwm.edu"
        self.inst1.password = "die_students"
        self.inst1.type = "instructor"
        self.inst1.name = "Der Instructinator"
        self.inst1.phone = "414.187.0666"
        self.inst1.address = "1234 5th Street Milwaukee, WI 53111"
        self.inst1.save()
        self.assertEquals(Commands.view_info(self.inst1.email),
                          [self.inst1.email, self.inst1.password, self.inst1.name, self.inst1.phone,
                           self.inst1.address])

    def test_view_info_custom_ta(self):
        self.ta1 = models.User()
        self.ta1.email = "grading_gradeguy@uwm.edu"
        self.ta1.password = "gradeymcgradersonword"
        self.ta1.type = "ta"
        self.ta1.name = "Gradey Von Gradenhoffen III"
        self.ta1.phone = "414.100.0100"
        self.ta1.address = "1234 5th Street Milwaukee, WI 53111"
        self.ta1.save()
        self.assertEquals(Commands.view_info(self.ta1.email),
                          [self.ta1.email, self.ta1.password, self.ta1.name, self.ta1.phone,
                           self.ta1.address])

    def test_view_info_user_big_email(self):
        self.ad1 = models.User()
        self.ad1.email = "thereallylongemailaddresslikefiftychars123@uwm.edu"
        self.ad1.password = "secure_password"
        self.ad1.type = "administrator"
        self.ad1.name = "Adminbot 4000"
        self.ad1.phone = "414.111.1111"
        self.ad1.address = "1234 5th Street Milwaukee, WI 53111"
        self.ad1.save()
        self.assertEquals(Commands.view_info(self.ad1.email),
                          [self.ad1.email, self.ad1.password, self.ad1.name, self.ad1.phone, self.ad1.address])

    def test_view_info_user_small_email(self):
        self.ad1 = models.User()
        self.ad1.email = "a@uwm.edu"
        self.ad1.password = "secure_password"
        self.ad1.type = "administrator"
        self.ad1.name = "Adminbot 4000"
        self.ad1.phone = "414.111.1111"
        self.ad1.address = "1234 5th Street Milwaukee, WI 53111"
        self.ad1.save()
        self.assertEquals(Commands.view_info(self.ad1.email),
                          [self.ad1.email, self.ad1.password, self.ad1.name, self.ad1.phone, self.ad1.address])

    def test_view_info_user_big_password(self):
        self.ad1 = models.User()
        self.ad1.email = "the_admin@uwm.edu@uwm.edu"
        self.ad1.password = "bigol20charpassword1"
        self.ad1.type = "administrator"
        self.ad1.name = "Adminbot 4000"
        self.ad1.phone = "414.111.1111"
        self.ad1.address = "1234 5th Street Milwaukee, WI 53111"
        self.ad1.save()
        self.assertEquals(Commands.view_info(self.ad1.email),
                          [self.ad1.email, self.ad1.password, self.ad1.name, self.ad1.phone, self.ad1.address])

    def test_view_info_user_tiny_password(self):
        self.ad1 = models.User()
        self.ad1.email = "the_admin@uwm.edu@uwm.edu"
        self.ad1.password = "1"
        self.ad1.type = "administrator"
        self.ad1.name = "Adminbot 4000"
        self.ad1.phone = "414.111.1111"
        self.ad1.address = "1234 5th Street Milwaukee, WI 53111"
        self.ad1.save()
        self.assertEquals(Commands.view_info(self.ad1.email),
                          [self.ad1.email, self.ad1.password, self.ad1.name, self.ad1.phone, self.ad1.address])

    def test_view_info_user_big_name(self):
        self.ad1 = models.User()
        self.ad1.email = "the_admin@uwm.edu@uwm.edu"
        self.ad1.password = "secure_password"
        self.ad1.type = "administrator"
        self.ad1.name = "John Jacob Jingle Heimer Schmitenhoffenvuelerstein"
        self.ad1.phone = "414.111.1111"
        self.ad1.address = "1234 5th Street Milwaukee, WI 53111"
        self.ad1.save()
        self.assertEquals(Commands.view_info(self.ad1.email),
                          [self.ad1.email, self.ad1.password, self.ad1.name, self.ad1.phone, self.ad1.address])

    def test_view_info_user_small_name(self):
        self.ad1 = models.User()
        self.ad1.email = "the_admin@uwm.edu@uwm.edu"
        self.ad1.password = "secure_password"
        self.ad1.type = "administrator"
        self.ad1.name = "A"
        self.ad1.phone = "414.111.1111"
        self.ad1.address = "1234 5th Street Milwaukee, WI 53111"
        self.ad1.save()
        self.assertEquals(Commands.view_info(self.ad1.email),
                          [self.ad1.email, self.ad1.password, self.ad1.name, self.ad1.phone, self.ad1.address])

    def test_view_info_user_max_phone(self):
        self.ad1 = models.User()
        self.ad1.email = "the_admin@uwm.edu@uwm.edu"
        self.ad1.password = "secure_password"
        self.ad1.type = "administrator"
        self.ad1.name = "Adminbot 4000"
        self.ad1.phone = "999.999.9999"
        self.ad1.address = "1234 5th Street Milwaukee, WI 53111"
        self.ad1.save()
        self.assertEquals(Commands.view_info(self.ad1.email),
                          [self.ad1.email, self.ad1.password, self.ad1.name, self.ad1.phone, self.ad1.address])

    def test_view_info_user_big_address(self):
        self.ad1 = models.User()
        self.ad1.email = "the_admin@uwm.edu@uwm.edu"
        self.ad1.password = "secure_password"
        self.ad1.type = "administrator"
        self.ad1.name = "Adminbot 4000"
        self.ad1.phone = "414.111.1111"
        self.ad1.address = "123456789123 Longstreetnamed St, Except In The Basement, " \
                           "Really Big Town Name Like So Huge, NY 21221"
        self.ad1.save()
        self.assertEquals(Commands.view_info(self.ad1.email),
                          [self.ad1.email, self.ad1.password, self.ad1.name, self.ad1.phone, self.ad1.address])

    def test_view_info_user_tiny_address(self):
        self.ad1 = models.User()
        self.ad1.email = "the_admin@uwm.edu@uwm.edu"
        self.ad1.password = "secure_password"
        self.ad1.type = "administrator"
        self.ad1.name = "Adminbot 4000"
        self.ad1.phone = "414.111.1111"
        self.ad1.address = "1"
        self.ad1.save()
        self.assertEquals(Commands.view_info(self.ad1.email),
                          [self.ad1.email, self.ad1.password, self.ad1.name, self.ad1.phone, self.ad1.address])
