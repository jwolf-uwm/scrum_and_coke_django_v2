import unittest






class EmailTests(unittest.TestCase):

    def setup(self):

        self.TA = TA("ta@uwm.edu", "taPass")

        self.INS = Instructor("ins@uwm.edu", "insPass")

        self.SUP = Supervisor("sup@uwm.edu", "supPass")

        self.ADMIN = Administrator("admin@uwm.edu", "adminPass")



    """

        The send notification command will send the given message to all users in the system

        if the message is sent successfully via email, send notification is a success

        -"Message sent successfully"

        If message is not sent, send notification failed

        -"Message not sent"

        if access is denied

        -"access denied"

    """



    def test_email_admin(self):

        self.ui.command("Login admin@uwm.edu adminPass")

        self.assertEqual(self.ui.command("send_notification This is just a test"), "Message sent successfully")



    def test_email_sup(self):

        self.ui.command("Login super@uwm.edu superPass")

        self.assertEqual(self.ui.command("send_notification This is just a test"), "Message sent successfully")



    def test_email_ins(self):

        self.ui.command("Login instr@uwm.edu instrPass")

        self.assertEqual(self.ui.command("send_notification This is just a test"), "Message sent successfully")



    def test_email_ta(self):

        self.ui.command("Login t_ayy@uwm.edu t_ayyPass")

        self.assertEqual(self.ui.command("send_notification This is just a test"), "access denied")



    def test_send_notification_fail(self):

        self.ui.command("Login admin@uwm.edu adminPass")

        # if internet goes out or another weird anomaly occurs

        self.assertEqual(self.ui.command("send_notification This is just a test"), "Message not sent")



    def test_send_notification_no_message(self):

        self.assertEqual(self.ui.command("send_notification"), "No message to send")