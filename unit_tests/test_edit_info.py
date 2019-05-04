from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class TestEditInfo(TestCase):
    # TODO: split up these unit tests

    def setUp(self):
        return

    # password tests
    def test_change_admin_password(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_password("admin1@uwm.edu", "new_password"), "Password changed.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.password, "new_password")
        self.assertNotEquals(self.ad1.password, "password")

    def test_change_super_password(self):
        self.sup1 = models.User()
        self.sup1.email = "super1@uwm.edu"
        self.sup1.password = "password"
        self.sup1.type = "supervisor"
        self.sup1.save()
        self.assertEquals(Commands.change_password("super1@uwm.edu", "new_password"), "Password changed.")
        sup1 = models.User.objects.get(email="super1@uwm.edu")
        self.assertEquals(sup1.password, "new_password")
        self.assertNotEquals(sup1.password, "password")

    def test_change_instructor_password(self):
        self.inst1 = models.User()
        self.inst1.email = "inst1@uwm.edu"
        self.inst1.password = "password"
        self.inst1.type = "instructor"
        self.inst1.save()
        self.assertEquals(Commands.change_password("inst1@uwm.edu", "new_password"), "Password changed.")
        inst1 = models.User.objects.get(email="inst1@uwm.edu")
        self.assertEquals(inst1.password, "new_password")
        self.assertNotEquals(inst1.password, "password")

    def test_change_ta_password(self):
        self.ta1 = models.User()
        self.ta1.email = "ta1@uwm.edu"
        self.ta1.password = "password"
        self.ta1.type = "instructor"
        self.ta1.save()
        self.assertEquals(Commands.change_password("ta1@uwm.edu", "new_password"), "Password changed.")
        ta1 = models.User.objects.get(email="ta1@uwm.edu")
        self.assertEquals(ta1.password, "new_password")
        self.assertNotEquals(ta1.password, "password")

    def test_multi_user_change_password(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()

        self.sup1 = models.User()
        self.sup1.email = "super1@uwm.edu"
        self.sup1.password = "password"
        self.sup1.type = "supervisor"
        self.sup1.save()

        self.assertEquals(Commands.change_password("super1@uwm.edu", "new_password"), "Password changed.")
        sup1 = models.User.objects.get(email="super1@uwm.edu")
        self.assertEquals(sup1.password, "new_password")
        self.assertNotEquals(sup1.password, "password")

    def test_change_max_password(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_password("admin1@uwm.edu", "bigol20charpassword1"), "Password changed.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.password, "bigol20charpassword1")
        self.assertNotEquals(self.ad1.password, "password")

    def test_change_min_password(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_password("admin1@uwm.edu", "1"), "Password changed.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.password, "1")
        self.assertNotEquals(self.ad1.password, "password")

    def test_change_password_too_big(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_password("admin1@uwm.edu", "bigol20charpassword11"),
                          "Password must be 20 characters or less.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.password, "password")
        self.assertNotEquals(self.ad1.password, "bigol20charpassword11")

    def test_change_password_too_small(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_password("admin1@uwm.edu", ""),
                          "Bad password.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.password, "password")
        self.assertNotEquals(self.ad1.password, "")

    def test_change_password_no_email(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()

        with self.assertRaises(TypeError):
            Commands.change_password("new_password")

    def test_change_password_no_password(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()

        with self.assertRaises(TypeError):
            Commands.change_password("admin1@uwm.edu")

    def test_change_password_wrong_types(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()

        with self.assertRaises(TypeError):
            Commands.change_password(1, 2)

    def test_change_password_no_args(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()

        with self.assertRaises(TypeError):
            Commands.change_password()

    # email tests

    def test_change_admin_email(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_email("admin1@uwm.edu", "new_email@uwm.edu"), "Email address changed.")
        self.ad1 = models.User.objects.get(email="new_email@uwm.edu")
        self.assertEquals(self.ad1.email, "new_email@uwm.edu")
        self.assertNotEquals(self.ad1.email, "admin1@uwm.edu")

    def test_change_super_email(self):
        self.sup1 = models.User()
        self.sup1.email = "super1@uwm.edu"
        self.sup1.password = "password"
        self.sup1.type = "supervisor"
        self.sup1.save()
        self.assertEquals(Commands.change_email("super1@uwm.edu", "new_email@uwm.edu"), "Email address changed.")
        self.sup1 = models.User.objects.get(email="new_email@uwm.edu")
        self.assertEquals(self.sup1.email, "new_email@uwm.edu")
        self.assertNotEquals(self.sup1.email, "super1@uwm.edu")

    def test_change_inst_email(self):
        self.inst1 = models.User()
        self.inst1.email = "inst1@uwm.edu"
        self.inst1.password = "password"
        self.inst1.type = "instructor"
        self.inst1.save()
        self.assertEquals(Commands.change_email("inst1@uwm.edu", "new_email@uwm.edu"), "Email address changed.")
        self.inst1 = models.User.objects.get(email="new_email@uwm.edu")
        self.assertEquals(self.inst1.email, "new_email@uwm.edu")
        self.assertNotEquals(self.inst1.email, "inst1@uwm.edu")

    def test_change_ta_email(self):
        self.ta1 = models.User()
        self.ta1.email = "ta1@uwm.edu"
        self.ta1.password = "password"
        self.ta1.type = "ta"
        self.ta1.save()
        self.assertEquals(Commands.change_email("ta1@uwm.edu", "new_email@uwm.edu"), "Email address changed.")
        self.ta1 = models.User.objects.get(email="new_email@uwm.edu")
        self.assertEquals(self.ta1.email, "new_email@uwm.edu")
        self.assertNotEquals(self.ta1.email, "ta1@uwm.edu")

    def test_change_email_multi_user(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()

        self.sup1 = models.User()
        self.sup1.email = "super1@uwm.edu"
        self.sup1.password = "password"
        self.sup1.type = "supervisor"
        self.sup1.save()

        self.assertEquals(Commands.change_email("admin1@uwm.edu", "new_email@uwm.edu"), "Email address changed.")
        self.ad1 = models.User.objects.get(email="new_email@uwm.edu")
        self.assertEquals(self.ad1.email, "new_email@uwm.edu")
        self.assertNotEquals(self.ad1.email, "admin1@uwm.edu")

    def test_change_email_taken(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()

        self.sup1 = models.User()
        self.sup1.email = "super1@uwm.edu"
        self.sup1.password = "password"
        self.sup1.type = "supervisor"
        self.sup1.save()

        self.assertEquals(Commands.change_email("admin1@uwm.edu", "super1@uwm.edu"), "Email address taken.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.email, "admin1@uwm.edu")
        self.assertNotEquals(self.ad1.email, "super1@uwm.edu")

    def test_change_min_email(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_email("admin1@uwm.edu", "a@uwm.edu"), "Email address changed.")
        self.ad1 = models.User.objects.get(email="a@uwm.edu")
        self.assertEquals(self.ad1.email, "a@uwm.edu")
        self.assertNotEquals(self.ad1.email, "admin1@uwm.edu")

    def test_change_max_email(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_email("admin1@uwm.edu", "thereallylongemailaddresslikefiftychars123@uwm.edu"),
                          "Email address changed.")
        self.ad1 = models.User.objects.get(email="thereallylongemailaddresslikefiftychars123@uwm.edu")
        self.assertEquals(self.ad1.email, "thereallylongemailaddresslikefiftychars123@uwm.edu")
        self.assertNotEquals(self.ad1.email, "admin1@uwm.edu")

    def test_change_too_big_email(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_email("admin1@uwm.edu",
                          "thereallylongemailaddresslikefiftychars123@uwm.edu1"),
                          "Email address must be 50 characters or less.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.email, "admin1@uwm.edu")
        self.assertNotEquals(self.ad1.email, "thereallylongemailaddresslikefiftychars123@uwm.edu1")

    def test_change_blank_email(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_email("admin1@uwm.edu", ""), "Email address must be uwm address.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.email, "admin1@uwm.edu")
        self.assertNotEquals(self.ad1.email, "")

    def test_change_wrong_email(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_email("admin1@uwm.edu", "admin1@uwm.com"),
                          "Email address must be uwm address.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.email, "admin1@uwm.edu")
        self.assertNotEquals(self.ad1.email, "admin1@uwm.com")

    def test_change_weird_email(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_email("admin1@uwm.edu", "admin1@uwm.edu@uwm.edu"),
                          "Email address must be uwm address.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.email, "admin1@uwm.edu")
        self.assertNotEquals(self.ad1.email, "admin1@uwm.edu@uwm.edu")

    def test_change_email_just_string(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_email("admin1@uwm.edu", "admin1uwmedu"),
                          "Email address must be uwm address.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.email, "admin1@uwm.edu")
        self.assertNotEquals(self.ad1.email, "admin1uwmedu")

    def test_change_email_no_old_email(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        with self.assertRaises(TypeError):
            Commands.change_email("new_email@uwm.edu")

    def test_change_email_no_new_email(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        with self.assertRaises(TypeError):
            Commands.change_email("admin@uwm.edu")

    def test_change_email_no_args(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        with self.assertRaises(TypeError):
            Commands.change_email()

    def test_change_email_wrong_arg_type(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        with self.assertRaises(TypeError):
            Commands.change_email(1, 2)

    # phone tests

    def test_change_admin_phone(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_phone("admin1@uwm.edu", "414.111.1111"), "Phone number changed.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.phone, "414.111.1111")
        self.assertNotEquals(self.ad1.phone, "000.000.0000")

    def test_change_super_phone(self):
        self.sup1 = models.User()
        self.sup1.email = "super1@uwm.edu"
        self.sup1.password = "password"
        self.sup1.type = "supervisor"
        self.sup1.save()
        self.assertEquals(Commands.change_phone("super1@uwm.edu", "414.111.1111"), "Phone number changed.")
        self.sup1 = models.User.objects.get(email="super1@uwm.edu")
        self.assertEquals(self.sup1.phone, "414.111.1111")
        self.assertNotEquals(self.sup1.phone, "000.000.0000")

    def test_change_inst_phone(self):
        self.inst1 = models.User()
        self.inst1.email = "inst1@uwm.edu"
        self.inst1.password = "password"
        self.inst1.type = "instructor"
        self.inst1.save()
        self.assertEquals(Commands.change_phone("inst1@uwm.edu", "414.111.1111"), "Phone number changed.")
        self.inst1 = models.User.objects.get(email="inst1@uwm.edu")
        self.assertEquals(self.inst1.phone, "414.111.1111")
        self.assertNotEquals(self.inst1.phone, "000.000.0000")

    def test_change_ta_phone(self):
        self.ta1 = models.User()
        self.ta1.email = "ta1@uwm.edu"
        self.ta1.password = "password"
        self.ta1.type = "ta"
        self.ta1.save()
        self.assertEquals(Commands.change_phone("ta1@uwm.edu", "414.111.1111"), "Phone number changed.")
        self.ta1 = models.User.objects.get(email="ta1@uwm.edu")
        self.assertEquals(self.ta1.phone, "414.111.1111")
        self.assertNotEquals(self.ta1.phone, "000.000.0000")

    def test_change_phone_multi_user(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()

        self.sup1 = models.User()
        self.sup1.email = "super1@uwm.edu"
        self.sup1.password = "password"
        self.sup1.type = "supervisor"
        self.sup1.save()

        self.assertEquals(Commands.change_phone("admin1@uwm.edu", "414.111.1111"), "Phone number changed.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.phone, "414.111.1111")
        self.assertNotEquals(self.ad1.phone, "000.000.0000")

    def test_change_max_phone(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_phone("admin1@uwm.edu", "999.999.9999"), "Phone number changed.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.phone, "999.999.9999")
        self.assertNotEquals(self.ad1.phone, "000.000.0000")

    def test_change_too_big_phone(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_phone("admin1@uwm.edu", "9999.9999.99999"), "Invalid phone format.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.phone, "000.000.0000")
        self.assertNotEquals(self.ad1.phone, "9999.9999.99999")

    def test_change_blank_phone(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_phone("admin1@uwm.edu", ""), "Invalid phone format.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.phone, "000.000.0000")
        self.assertNotEquals(self.ad1.phone, "")

    def test_change_too_small_phone(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_phone("admin1@uwm.edu", "99.99.999"), "Invalid phone format.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.phone, "000.000.0000")
        self.assertNotEquals(self.ad1.phone, "99.99.999")

    def test_change_phone_just_string(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_phone("admin1@uwm.edu", "I'M A PHONE NUMBER"), "Invalid phone format.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.phone, "000.000.0000")
        self.assertNotEquals(self.ad1.phone, "I'M A PHONE NUMBER")

    def test_change_phone_no_number(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        with self.assertRaises(TypeError):
            Commands.change_phone("admin1@uwm.edu")

    def test_change_phone_no_email(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        with self.assertRaises(TypeError):
            Commands.change_phone("414.111.1111")

    def test_change_phone_no_args(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        with self.assertRaises(TypeError):
            Commands.change_phone()

    def test_change_phone_wrong_arg_type(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        with self.assertRaises(AttributeError):
            Commands.change_phone(1, 2)

    # name tests

    def test_change_admin_name(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_name("admin1@uwm.edu", "Admin Guy"), "Name changed.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.name, "Admin Guy")
        self.assertNotEquals(self.ad1.name, "DEFAULT")

    def test_change_super_name(self):
        self.sup1 = models.User()
        self.sup1.email = "super1@uwm.edu"
        self.sup1.password = "password"
        self.sup1.type = "supervisor"
        self.sup1.save()
        self.assertEquals(Commands.change_name("super1@uwm.edu", "Super Guy"), "Name changed.")
        sup1 = models.User.objects.get(email="super1@uwm.edu")
        self.assertEquals(sup1.name, "Super Guy")
        self.assertNotEquals(sup1.name, "DEFAULT")

    def test_change_instructor_name(self):
        self.inst1 = models.User()
        self.inst1.email = "inst1@uwm.edu"
        self.inst1.password = "password"
        self.inst1.type = "instructor"
        self.inst1.save()
        self.assertEquals(Commands.change_name("inst1@uwm.edu", "Instructor Guy"), "Name changed.")
        inst1 = models.User.objects.get(email="inst1@uwm.edu")
        self.assertEquals(inst1.name, "Instructor Guy")
        self.assertNotEquals(inst1.name, "DEFAULT")

    def test_change_ta_name(self):
        self.ta1 = models.User()
        self.ta1.email = "ta1@uwm.edu"
        self.ta1.password = "password"
        self.ta1.type = "ta"
        self.ta1.save()
        self.assertEquals(Commands.change_name("ta1@uwm.edu", "TA Guy"), "Name changed.")
        ta1 = models.User.objects.get(email="ta1@uwm.edu")
        self.assertEquals(ta1.name, "TA Guy")
        self.assertNotEquals(ta1.name, "DEFAULT")

    def test_multi_user_change_name(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()

        self.sup1 = models.User()
        self.sup1.email = "super1@uwm.edu"
        self.sup1.password = "password"
        self.sup1.type = "supervisor"
        self.sup1.save()

        self.assertEquals(Commands.change_name("admin1@uwm.edu", "Admin Guy"), "Name changed.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.name, "Admin Guy")
        self.assertNotEquals(self.ad1.name, "DEFAULT")

    def test_change_max_name(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_name("admin1@uwm.edu",
                                               "John Jacob Jingle Heimer Schmitenhoffenvuelerstein"), "Name changed.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.name, "John Jacob Jingle Heimer Schmitenhoffenvuelerstein")
        self.assertNotEquals(self.ad1.name, "DEFAULT")

    def test_change_min_name(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_name("admin1@uwm.edu", "A"), "Name changed.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.name, "A")
        self.assertNotEquals(self.ad1.name, "DEFAULT")

    def test_change_name_too_big(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_name("admin1@uwm.edu",
                                               "John Jacob Jingle Heimer Schmitenhoffenvuelerstein1"),
                          "Name must be 50 characters or less.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.name, "DEFAULT")
        self.assertNotEquals(self.ad1.name, "John Jacob Jingle Heimer Schmitenhoffenvuelerstein1")

    def test_change_name_too_small(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_name("admin1@uwm.edu", ""),
                          "Bad name.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.name, "DEFAULT")
        self.assertNotEquals(self.ad1.name, "")

    def test_change_name_no_name(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()

        with self.assertRaises(TypeError):
            Commands.change_name("admin1@uwm.edu")

    def test_change_name_no_email(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()

        with self.assertRaises(TypeError):
            Commands.change_name("Admin Guy")

    def test_change_name_wrong_types(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()

        with self.assertRaises(TypeError):
            Commands.change_name(1, 2)

    def test_change_name_no_args(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()

        with self.assertRaises(TypeError):
            Commands.change_password()

    # address tests
    def test_change_admin_address(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_address("admin1@uwm.edu", "1234 5th Street Milwaukee, WI 53111"),
                          "Address changed.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.address, "1234 5th Street Milwaukee, WI 53111")
        self.assertNotEquals(self.ad1.address, "not set")

    def test_change_super_address(self):
        self.sup1 = models.User()
        self.sup1.email = "super1@uwm.edu"
        self.sup1.password = "password"
        self.sup1.type = "supervisor"
        self.sup1.save()
        self.assertEquals(Commands.change_address("super1@uwm.edu", "1234 5th Street Milwaukee, WI 53111"),
                          "Address changed.")
        sup1 = models.User.objects.get(email="super1@uwm.edu")
        self.assertEquals(sup1.address, "1234 5th Street Milwaukee, WI 53111")
        self.assertNotEquals(sup1.address, "not set")

    def test_change_instructor_address(self):
        self.inst1 = models.User()
        self.inst1.email = "inst1@uwm.edu"
        self.inst1.password = "password"
        self.inst1.type = "instructor"
        self.inst1.save()
        self.assertEquals(Commands.change_address("inst1@uwm.edu", "1234 5th Street Milwaukee, WI 53111"),
                          "Address changed.")
        inst1 = models.User.objects.get(email="inst1@uwm.edu")
        self.assertEquals(inst1.address, "1234 5th Street Milwaukee, WI 53111")
        self.assertNotEquals(inst1.address, "not set")

    def test_change_ta_address(self):
        self.ta1 = models.User()
        self.ta1.email = "ta1@uwm.edu"
        self.ta1.password = "password"
        self.ta1.type = "ta"
        self.ta1.save()
        self.assertEquals(Commands.change_address("ta1@uwm.edu", "1234 5th Street Milwaukee, WI 53111"),
                          "Address changed.")
        ta1 = models.User.objects.get(email="ta1@uwm.edu")
        self.assertEquals(ta1.address, "1234 5th Street Milwaukee, WI 53111")
        self.assertNotEquals(ta1.address, "not set")

    def test_multi_user_change_address(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()

        self.sup1 = models.User()
        self.sup1.email = "super1@uwm.edu"
        self.sup1.password = "password"
        self.sup1.type = "supervisor"
        self.sup1.save()

        self.assertEquals(Commands.change_address("admin1@uwm.edu", "1234 5th Street Milwaukee, WI 53111"),
                          "Address changed.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.address, "1234 5th Street Milwaukee, WI 53111")
        self.assertNotEquals(self.ad1.address, "not set")

    def test_change_max_address(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_address("admin1@uwm.edu",
                                                 "123456789123 Longstreetnamed St, Except In The Basement, "
                                                 "Really Big Town Name Like So Huge, NY 21221"),
                                                 "Address changed.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.address, "123456789123 Longstreetnamed St, Except In The Basement, "
                                            "Really Big Town Name Like So Huge, NY 21221")
        self.assertNotEquals(self.ad1.address, "not set")

    def test_change_min_address(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_address("admin1@uwm.edu", "1"),
                          "Address changed.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertEquals(self.ad1.address, "1")
        self.assertNotEquals(self.ad1.address, "not set")

    def test_change_address_too_big(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_address("admin1@uwm.edu",
                                                  "1123456789123 Longstreetnamed St, Except In The Basement, "
                                                  "Really Big Town Name Like So Huge, NY 21221"),
                          "Address must be 100 characters or less.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertNotEquals(self.ad1.address, "1123456789123 Longstreetnamed St, Except In The Basement, "
                                               "Really Big Town Name Like So Huge, NY 21221")
        self.assertEquals(self.ad1.address, "not set")

    def test_change_address_too_small(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()
        self.assertEquals(Commands.change_address("admin1@uwm.edu", ""),
                          "Bad address.")
        self.ad1 = models.User.objects.get(email="admin1@uwm.edu")
        self.assertNotEquals(self.ad1.address, "")
        self.assertEquals(self.ad1.address, "not set")

    def test_change_address_no_address(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()

        with self.assertRaises(TypeError):
            Commands.change_address("admin1@uwm.edu")

    def test_change_address_no_email(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()

        with self.assertRaises(TypeError):
            Commands.change_address("1234 5th Street Milwaukee, WI 53111")

    def test_change_address_wrong_types(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()

        with self.assertRaises(TypeError):
            Commands.change_address(1, 2)

    def test_change_address_no_args(self):
        self.ad1 = models.User()
        self.ad1.email = "admin1@uwm.edu"
        self.ad1.password = "password"
        self.ad1.type = "administrator"
        self.ad1.save()

        with self.assertRaises(TypeError):
            Commands.change_address()