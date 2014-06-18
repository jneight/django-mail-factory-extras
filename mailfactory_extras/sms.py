# coding=utf-8

import os

from django.conf import settings
from django.template import TemplateDoesNotExist

from mail_factory.mails import BaseMail
from twilio.rest import TwilioRestClient


class BaseSMS(BaseMail):
    def get_template_part(self, part, lang=None):

        templates = []
        # 1/ localized: mails/invitation_code/fr/
        localized = os.path.join('sms', self.template_name, lang or self.lang, part)
        templates.append(localized)

        # 2/ fallback: mails/invitation_code/
        fallback = os.path.join('sms', self.template_name, part)
        templates.append(fallback)

        # return the list of templates path candidates
        return templates

    def mail_admins(self, attachments=None, from_email=None):
        raise NotImplementedError()

    def create_sms_msg(self, lang=None):
        try:
            body = self._render_part('body.txt', lang=lang)
        except TemplateDoesNotExist:
            raise TemplateDoesNotExist(
                'Txt template have not been found')
        return body

    def send(self, to_phone, from_phone=None):
        from_phone = from_phone or settings.TWILIO_PHONE_SERVER
        message = self.create_sms_msg()
        client = TwilioRestClient(
            settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        response = client.messages.create(
            to=to_phone, from_=from_phone, body=message)
        print response.__dict__
