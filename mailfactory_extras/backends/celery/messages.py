# coding=utf-8

from celery import shared_task, current_app
from celery.contrib.methods import task_method
from celery.utils.log import get_task_logger
logger_celery = get_task_logger(__name__)

from mail_factory.messages import EmailMultiRelated

try:
    from app_metrics.utils import metric
except ImportError:
    pass


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
        logger.celery.info('[TASK] [EMAIL] email waiting')
        if async:
            return self._send.delay(fail_silently=fail_silently)
        return self._send(fail_silently=fail_silently)


class AsyncEmailMultiRelatedMetric(AsyncEmailMultiRelated):
    """Metric are handled via django-app-metrics

    """
    waiting_metric = 'mails_waiting'
    sended_metric = 'mails_sended'

    @current_app.task(
        name='AsyncEmailMultiRelated._send_async', filter=task_method)
    def _send(self, fail_silently=False):
        """With this decorator, celery will support calling class
        methods as tasks

        """
        result = super(EmailMultiRelated, self).send()
        metric(self.sended_metric)
        return result

    def send(self, fail_silently=False, async=False):
        metric(self.waiting_metric)
        return super(AsyncEmailMultiRelatedMetric, self).send(
            fail_silently=fail_silently, async=async)

