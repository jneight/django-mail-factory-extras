# coding=utf-8

from django.conf import settings

from ..base import BaseSMS
from twilio.rest import TwilioRestClient


class TwilioSMS(BaseSMS):
    def send(self, to_phone, from_phone=None):
        from_phone = from_phone or settings.TWILIO_PHONE_SERVER
        message = self.create_sms_msg()
        client = TwilioRestClient(
            settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        response = client.messages.create(
            to=to_phone, from_=from_phone, body=message)
        return response

