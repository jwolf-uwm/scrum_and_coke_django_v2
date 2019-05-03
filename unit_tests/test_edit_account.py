from django.test import TestCase
from ta_assign import models
from classes.commands import Commands


class TestEditAccount(TestCase):
    def setUp(self):
        return

    def test_edit_account_password(self):
        # create a test user in the system
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.save()
        # test edit password
        Commands.edit_account("rando@uwm.edu", "password", "new_pass")

        tester = models.User.objects.get(email="rando@uwm.edu")
        self.assertEqual(tester.password, "new_pass")

    def test_edit_account_email(self):
        # create a test user in the system
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.save()
        # test edit email
        Commands.edit_account("rando@uwm.edu", "email", "NEW_EMAIL@uwm.edu")
        with self.assertRaises(models.User.DoesNotExist):
            models.User.objects.get(email="rando@uwm.edu")
        tester = models.User.objects.get(email="NEW_EMAIL@uwm.edu")
        self.assertEqual(tester.email, "NEW_EMAIL@uwm.edu")

    def test_edit_account_two_email_endings(self):
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.save()
        self.assertEqual(Commands.edit_account("rando@uwm.edu", "email", "badEmail@uwm.edu@uwm.edu"),
                         "Entered email does not end in uwm.edu")
        with self.assertRaises(models.User.DoesNotExist):
            models.User.objects.get(email="badEmail@uwm.edu@uwm.edu")
        tester = models.User.objects.get(email="rando@uwm.edu")
        self.assertEqual(tester.email, "rando@uwm.edu")

    def test_edit_account_email_not_uwm(self):
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.save()
        self.assertEqual(Commands.edit_account("rando@uwm.edu", "email", "badEmail@gmail.com"),
                         "Entered email does not end in uwm.edu")
        with self.assertRaises(models.User.DoesNotExist):
            models.User.objects.get(email="badEmail@gmail.com")
        tester = models.User.objects.get(email="rando@uwm.edu")
        self.assertEqual(tester.email, "rando@uwm.edu")

    def test_edit_account_email_no_end(self):
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.save()
        self.assertEqual(Commands.edit_account("rando@uwm.edu", "email", "badEmail"),
                         "Entered email does not end in uwm.edu")
        with self.assertRaises(models.User.DoesNotExist):
            models.User.objects.get(email="badEmail")
        tester = models.User.objects.get(email="rando@uwm.edu")
        self.assertEqual(tester.email, "rando@uwm.edu")

    def test_edit_account_phone(self):
        # create a test user in the system
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.save()
        # test edit phone
        self.assertTrue(Commands.edit_account("rando@uwm.edu", "phone", "111.111.1111"))
        tester = models.User.objects.get(email="rando@uwm.edu")
        self.assertEqual(tester.phone, "111.111.1111")

    def test_edit_account_phone_nan(self):
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.save()
        self.assertEqual(Commands.edit_account("rando@uwm.edu", "phone", "not a number"),
                         "Phone number is not of the correct form (###.###.####)")
        tester = models.User.objects.get(email="rando@uwm.edu")
        self.assertEqual(tester.phone, "000.000.0000")

    def test_edit_account_phone_too_short(self):
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.save()
        self.assertEqual(Commands.edit_account("rando@uwm.edu", "phone", "1234"),
                         "Phone number is not of the correct form (###.###.####)")
        tester = models.User.objects.get(email="rando@uwm.edu")
        self.assertEqual(tester.phone, "000.000.0000")

    def test_edit_account_phone_too_long(self):
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.save()
        self.assertEqual(Commands.edit_account("rando@uwm.edu", "phone", "1234567890987654"),
                         "Phone number is not of the correct form (###.###.####)")
        tester = models.User.objects.get(email="rando@uwm.edu")
        self.assertEqual(tester.phone, "000.000.0000")

    def test_edit_account_phone_dashes(self):
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.save()
        self.assertEqual(Commands.edit_account("rando@uwm.edu", "phone", "414-414-4141"),
                         "Phone number is not of the correct form (###.###.####)")
        tester = models.User.objects.get(email="rando@uwm.edu")
        self.assertEqual(tester.phone, "000.000.0000")

    def test_edit_account_phone_mixed_form(self):
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.save()
        self.assertEqual(Commands.edit_account("rando@uwm.edu", "phone", "(414)414-4141"),
                         "Phone number is not of the correct form (###.###.####)")
        tester = models.User.objects.get(email="rando@uwm.edu")
        self.assertEqual(tester.phone, "000.000.0000")

    def test_edit_account_phone_letters(self):
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.save()
        self.assertEqual(Commands.edit_account("rando@uwm.edu", "phone", "abc.abc.abcd"),
                         "Phone number is not of the correct form (###.###.####)")
        tester = models.User.objects.get(email="rando@uwm.edu")
        self.assertEqual(tester.phone, "000.000.0000")

    def test_edit_account_phone_too_long_again(self):
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.save()
        self.assertEqual(Commands.edit_account("rando@uwm.edu", "phone", "1234.1234.1234"),
                         "Phone number is not of the correct form (###.###.####)")
        tester = models.User.objects.get(email="rando@uwm.edu")
        self.assertEqual(tester.phone, "000.000.0000")

    def test_edit_account_name(self):
        # create a test user in the system
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.save()
        # test edit name
        Commands.edit_account("rando@uwm.edu", "name", "Howard Stern")

        tester = models.User.objects.get(email="rando@uwm.edu")
        self.assertEqual(tester.name, "Howard Stern")

    def test_edit_account_dne(self):
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.save()
        self.assertEqual(Commands.edit_account("wrong_email@uwm.edu", "password", "new_pass"),
                         "Entered user does not exist")

    def test_edit_account_bad_field(self):
        tester = models.User()
        tester.email = "rando@uwm.edu"
        tester.password = "random_password"
        tester.save()
        self.assertEqual(Commands.edit_account("rando@uwm.edu", "wrong_field", "new_pass"),
                         "The entered data field does not exist")
