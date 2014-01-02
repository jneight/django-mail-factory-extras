# coding=utf-8

from celery import shared_task
from celery.contrib.methods import task_method

from mail_factory.messages import EmailMultiRelated


class AsyncEmailMultiRelated(EmailMultiRelated):
    @shared_task(filter=task_method)
    def _send_async(self, fail_silently=False):
        return super(AsyncEmailMultiRelated, self).send()

    def _send_sync(self, fail_silently=False):
        return super(AsyncEmailMultiRelated, self).send()

    def send(self, fail_silently=False, async=False):
        if async:
            return self._send_async(fail_silently=fail_silently)
        return self._send_sync(fail_silently=fail_silently)

