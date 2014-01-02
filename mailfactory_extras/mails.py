# coding=utf-8

from mail_factory import factory
from mail_factory.mails import BaseMail

from .messages import AsyncEmailMultiRelated


class CeleryMail(BaseMail):
    def __init__(self, *args, **kwargs):
        """Add async option to BaseMail

            :param async: True to send using task

        """
        self.async = kwargs.pop('async', False)
        super(CeleryMail, self).__init__(*args, **kwargs)

    def create_email_msg(
            self, emails, attachments=None, from_email=None, lang=None,
            message_class=AsyncEmailMultiRelated):
        return super(CeleryMail, self).create_email_msg(
            emails, attachments=attachments, from_email=from_email,
            lang=lang, message_class=message_class)

    def send(self, emails, attachments=None, from_email=None):
        message = self.create_email_msg(
            emails, attachments=attachments, from_email=from_email,
            message_class=message_class)
        message.send(fail_silently=False, async=self.async)



