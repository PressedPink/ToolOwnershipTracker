import uuid
from django.core import mail
from django.test import TestCase
from unittest.mock import patch
from capstoneMain.ToolOwnershipTracker.models import User
from capstoneMain.ToolOwnershipTracker.classes.Users import check_reset_password_token, send_forget_password_mail, forget_password, change_password


class TestUtils(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

    def test_check_reset_password_token(self):
        token = str(uuid.uuid4())
        self.user.forget_password_token = token
        self.user.save()
        self.assertTrue(check_reset_password_token('testuser@example.com', token))
        self.assertFalse(check_reset_password_token('testuser@example.com', 'invalid_token'))

    def test_send_forget_password_mail(self):
        send_forget_password_mail('testuser@example.com', 'valid_token')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Your password reset link')
        self.assertEqual(mail.outbox[0].to, ['testuser@example.com'])

    @patch('app.utils.UserClass.send_forget_password_mail')
    def test_forget_password(self, mock_send_forget_password_mail):
        forget_password('testuser@example.com')
        self.assertTrue(mock_send_forget_password_mail.called)
        self.assertEqual(mock_send_forget_password_mail.call_args[0][0], 'testuser@example.com')
        self.assertEqual(len(User.objects.filter(forget_password_token__isnull=False)), 1)

    def test_change_password(self):
        self.user.forget_password_token = str(uuid.uuid4())
        self.user.save()
        self.assertTrue(change_password('testuser@example.com', 'newpassword', 'newpassword'))
        self.assertFalse(User.objects.filter(forget_password_token__isnull=False).exists())
        self.assertTrue(self.user.check_password('newpassword'))