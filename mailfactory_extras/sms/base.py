# coding=utf-8

import os

from abc import ABCMeta, abstractmethod

from django.utils import six
from django.template import TemplateDoesNotExist

from mail_factory.mails import BaseMail


class BaseSMS(BaseMail, six.with_metaclass(ABCMeta)):
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

    @abstractmethod
    def send(self, to_phone, from_phone=None):
        return
