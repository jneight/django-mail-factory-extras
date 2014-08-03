# coding=utf-8

from celery import shared_task
from celery.contrib.methods import task_method

from mail_factory.messages import EmailMultiRelated

try:
    from app_metrics.utils import metric
except ImportError:
    metric = None


class CeleryEmailMultiRelated(EmailMultiRelated):
    @shared_task(
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


class CeleryEmailMultiRelatedMetric(CeleryEmailMultiRelated):
    """Metric are handled via django-app-metrics

    """
    waiting_metric = 'mails_waiting'
    sended_metric = 'mails_sended'

    @shared_task(
        name='AsyncEmailMultiRelatedMetric._send_async', filter=task_method)
    def _send(self, fail_silently=False):
        """With this decorator, celery will support calling class
        methods as tasks

        """
        result = super(EmailMultiRelated, self).send()
        if metric is not None:
            metric(self.sended_metric)
            metric(self.waiting_metric, -1)
        return result

    def send(self, fail_silently=False, async=False):
        if metric is not None:
            metric(self.waiting_metric)
        return super(CeleryEmailMultiRelatedMetric, self).send(
            fail_silently=fail_silently, async=async)

