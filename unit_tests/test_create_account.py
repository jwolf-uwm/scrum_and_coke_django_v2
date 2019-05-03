from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class TestCreateAccount(TestCase):

    def setUp(self):
        return

    def test_create_account_instructor(self):
        # Create Instructor Tests
        # create unused instructor account
        self.assertEquals(Commands.create_account("DustyBottoms@uwm.edu", "better_password", "instructor"),
                          "Account created!")
        # get account that was just setup
        test_model_ins = models.User.objects.get(email="DustyBottoms@uwm.edu")
        # make sure email is equal
        self.assertEqual(test_model_ins.email, "DustyBottoms@uwm.edu")
        # make sure password is equal
        self.assertEqual(test_model_ins.password, "better_password")
        # default name test
        self.assertEqual(test_model_ins.name, "DEFAULT")
        # default phone test
        self.assertEqual(test_model_ins.phone, "000.000.0000")
        # login false test
        self.assertFalse(test_model_ins.isLoggedOn)
        # default address test
        self.assertEqual(test_model_ins.address, "not set")

    def test_create_account_TA(self):
        # Create TA Tests
        # create unused ta account
        self.assertEquals(Commands.create_account("FredClaus@uwm.edu", "santa_bro", "ta"), "Account created!")
        # get account
        test_model_ta = models.User.objects.get(email="FredClaus@uwm.edu")
        # test email
        self.assertEqual(test_model_ta.email, "FredClaus@uwm.edu")
        # test password
        self.assertEqual(test_model_ta.password, "santa_bro")
        # default name test
        self.assertEqual(test_model_ta.name, "DEFAULT")
        # default phone test
        self.assertEqual(test_model_ta.phone, "000.000.0000")
        # login false test
        self.assertFalse(test_model_ta.isLoggedOn)
        # default address test
        self.assertEqual(test_model_ta.address, "not set")

    # Invalid account type tests
    def test_create_account_supervisor(self):
        # create supervisor test
        self.assertEquals(Commands.create_account("superdude@uwm.edu", "super1", "supervisor"),
                          "Invalid account type.")
        # not in db
        with self.assertRaises(models.User.DoesNotExist):
            models.User.objects.get(email="superdude@uwm.edu")

    def test_create_account_administrator(self):
        # create admin test
        self.assertEquals(Commands.create_account("adminotaur@uwm.edu", "labyrinth", "administrator"),
                          "Invalid account type.")
        # not in db
        with self.assertRaises(models.User.DoesNotExist):
            models.User.objects.get(email="adminotaur@uwm.edu")

    def test_create_account_other(self):
        # create whatever test
        self.assertEquals(Commands.create_account("farfelkugel@uwm.edu", "not_today", "horse"),
                          "Invalid account type.")
        # not in db
        with self.assertRaises(models.User.DoesNotExist):
            models.User.objects.get(email="farfelkugel@uwm.edu")

    # Invalid parameter tests
    def test_create_account_invalid_parameter_no_email(self):
        # no email
        with self.assertRaises(TypeError):
            Commands.create_account("password", "instructor")

    def test_create_account_invalid_parameter_no_password(self):
        # no password
        with self.assertRaises(TypeError):
            Commands.create_account("no_password@uwm.edu", "instructor")

    def test_create_account_invalid_parameter_no_account_type(self):
        # no account type
        with self.assertRaises(TypeError):
            Commands.create_account("some_doof@uwm.edu", "password3")

    def test_create_account_invalid_parameter_non_uwm_email(self):
        # non uwm email
        self.assertEquals(Commands.create_account("bobross@bobross.com", "happy_trees", "instructor"),
                          "Email address must be uwm address.")
        # not in db
        with self.assertRaises(models.User.DoesNotExist):
            models.User.objects.get(email="bobross@bobross.com")

    def test_create_account_invalid_parameter_weird_email(self):
        # weird email, props to Grant for this test
        self.assertEquals(Commands.create_account("bobross@uwm.edu@uwm.edu", "lotta_bob", "instructor"),
                          "Email address must be uwm address.")
        # not in db
        with self.assertRaises(models.User.DoesNotExist):
            models.User.objects.get(email="bobross@uwm.edu@uwm.edu")

    def test_create_account_invalid_parameter_not_an_email_addy(self):
        # not really an email addy
        self.assertEquals(Commands.create_account("TRUST_ME_IM_EMAIL", "seriously_real_address", "ta"),
                          "Email address must be uwm address.")
        # not in db
        with self.assertRaises(models.User.DoesNotExist):
            models.User.objects.get(email="TRUST_ME_IM_EMAIL")

    def test_create_account_invalid_parameter_wrong_arg_types(self):
        # int args
        with self.assertRaises(TypeError):
            Commands.create_account(7, 8, 9)
        with self.assertRaises(models.User.DoesNotExist):
            models.User.objects.get(email=7)

    def test_create_account_invalid_parameter_taken_email(self):
        # email taken
        Commands.create_account("FredClaus@uwm.edu", "santa_bro", "ta")
        self.assertEquals(Commands.create_account("FredClaus@uwm.edu", "santa_bro", "ta"), "Email address taken.")

    def test_bad_password(self):
        self.assertEquals(Commands.create_account("bad_password@uwm.edu", "", "ta"), "Bad password.")

    def test_create_account_max_email(self):
        self.assertEquals(Commands.create_account("thereallylongemailaddresslikefiftychars123@uwm.edu",
                                                  "better_password", "instructor"), "Account created!")
        test_model_ins = models.User.objects.get(email="thereallylongemailaddresslikefiftychars123@uwm.edu")
        self.assertEqual(test_model_ins.email, "thereallylongemailaddresslikefiftychars123@uwm.edu")

    def test_create_account_email_too_big(self):
        self.assertEquals(Commands.create_account("thereallylongemailaddresslikefiftychars1123@uwm.edu",
                                                  "better_password", "instructor"), "Email address must be 50 "
                                                                                    "characters or less.")

    def test_create_account_min_email(self):
        self.assertEquals(Commands.create_account("i@uwm.edu", "better_password", "instructor"), "Account created!")
        test_model_ins = models.User.objects.get(email="i@uwm.edu")
        self.assertEqual(test_model_ins.email, "i@uwm.edu")

    def test_create_account_max_password(self):
        self.assertEquals(Commands.create_account("DustyBottoms@uwm.edu", "bigol20charpassword1", "instructor"),
                          "Account created!")
        test_model_ins = models.User.objects.get(email="DustyBottoms@uwm.edu")
        self.assertEqual(test_model_ins.password, "bigol20charpassword1")

    def test_create_account_password_too_big(self):
        self.assertEquals(Commands.create_account("DustyBottoms@uwm.edu", "bigol20charpassword11", "instructor"),
                          "Password must be 20 characters or less.")

    def test_create_account_min_password(self):
        self.assertEquals(Commands.create_account("DustyBottoms@uwm.edu", "1", "instructor"),
                          "Account created!")
        test_model_ins = models.User.objects.get(email="DustyBottoms@uwm.edu")
        self.assertEqual(test_model_ins.password, "1")
