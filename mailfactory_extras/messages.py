# coding=utf-8

from celery import shared_task, current_app
from celery.contrib.methods import task_method

from mail_factory.messages import EmailMultiRelated


class AsyncEmailMultiRelated(EmailMultiRelated):
    @current_app.task(
        name='AsyncEmailMultiRelated._send_async', filter=task_method)
    def _send(self, fail_silently=False):
        """With this decorator, celery will support calling class
        methods as tasks

        """
        return super(EmailMultiRelated, self).send()

    def send(self, fail_silently=False, async=False):
        """Check if mail will be sent using async task or not

        """
        if async:
            return self._send.delay(fail_silently=fail_silently)
        return self._send(fail_silently=fail_silently)

