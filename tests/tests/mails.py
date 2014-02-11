# coding=utf-8

from django.test import TestCase
from django.core import mail
from django.conf import settings

from mail_factory.exceptions import MissingMailContextParamException

from mailfactory_extras.backends.celery import (
    CeleryMail, AsyncEmailMultiRelated)


class CeleryMailTest(TestCase):

    def __init__(self, *args, **kwargs):
        super(CeleryMailTest, self).__init__(*args, **kwargs)
        self.mail_class = CeleryMail

    def test_init(self):
        class TestMail(self.mail_class):
            params = ['foo']

        with self.assertRaises(MissingMailContextParamException):
            TestMail()
        with self.assertRaises(MissingMailContextParamException):
            TestMail({})
        with self.assertRaises(MissingMailContextParamException):
            TestMail({'bar': 'bar'})
        self.assertTrue(TestMail({'foo': 'bar'}))

    def test_get_language(self):
        class TestMail(self.mail_class):
            params = []

        translation.activate('en')
        self.assertEqual(TestMail().get_language(), 'en')
        translation.activate('fr')
        self.assertEqual(TestMail().get_language(), 'fr')

    def test_get_params(self):
        class TestMail(self.mail_class):
            params = []

        self.assertEqual(TestMail().get_params(), [])

        class TestMail2(self.mail_class):
            params = ['foo']

        self.assertEqual(TestMail2({'foo': 'bar'}).get_params(), ['foo'])

    def test_get_context_data(self):
        class TestMail(self.mail_class):
            params = []

        self.assertEqual(TestMail().get_context_data(), {})
        self.assertEqual(TestMail().get_context_data(foo='bar'),
                         {'foo': 'bar'})

    def test_get_attachments(self):
        class TestMail(self.mail_class):
            params = []

        self.assertEqual(TestMail().get_attachments(None), [])
        self.assertEqual(TestMail().get_attachments('foo'), 'foo')

    def test_get_template_part(self):
        class TestMail(self.mail_class):
            params = []
            template_name = 'test'

        test_mail = TestMail()
        test_mail.lang = 'foo'
        self.assertEqual(test_mail.get_template_part('stuff'),
                         ['mails/test/foo/stuff', 'mails/test/stuff'])
        self.assertEqual(test_mail.get_template_part('stuff', 'bar'),
                         ['mails/test/bar/stuff', 'mails/test/stuff'])

    def test_render_part(self):
        class TestMail(self.mail_class):
            params = []
            template_name = 'test'

        test_mail = TestMail()
        with self.assertRaises(TemplateDoesNotExist):
            test_mail._render_part('stuff')

        # active language before stays the same
        cur_lang = translation.get_language()
        test_mail._render_part('subject.txt')
        self.assertEqual(cur_lang, translation.get_language())

        # without a proper language, fallback
        test_mail.lang = 'not a lang'
        self.assertEqual(test_mail._render_part('subject.txt'),
                         '[TestCase] Mail test subject')
        # with a proper language, use it
        test_mail.lang = 'fr'
        self.assertEqual(test_mail._render_part('body.txt'), 'Français')
        # use provided language
        test_mail.lang = 'not a lang'
        self.assertEqual(test_mail._render_part('subject.txt', 'en'),
                         '[TestCase] Mail test subject')
        self.assertEqual(test_mail._render_part('body.txt', 'fr'), 'Français')
        # if provided language doesn't exist, fallback
        self.assertEqual(test_mail._render_part('subject.txt', 'not a lang'),
                         '[TestCase] Mail test subject')

    def test_create_email_msg(self):
        class TestMail(self.mail_class):
            params = []
            template_name = 'test'

        test_mail = TestMail()
        # check is using the custom message class
        self.assertIsInstance(
            test_mail.create_email_msg([]), CeleryEmailMultiRelated)

        # no "from email" given => use settings.DEFAULT_FROM_EMAIL
        self.assertEqual(test_mail.create_email_msg([]).from_email,
                         settings.DEFAULT_FROM_EMAIL)
        msg = test_mail.create_email_msg([], from_email='foo')
        self.assertEqual(msg.from_email, 'foo')
        # templates with html
        msg = test_mail.create_email_msg([], lang='fr')
        self.assertEqual(len(msg.alternatives), 1)
        msg = test_mail.create_email_msg([], lang='en')
        self.assertEqual(len(msg.alternatives), 1)
        # templates without html
        test_mail.template_name = 'test_no_html'
        msg = test_mail.create_email_msg([], lang='fr')
        self.assertEqual(len(msg.alternatives), 0)
        msg = test_mail.create_email_msg([], lang='en')
        self.assertEqual(len(msg.alternatives), 0)
        #template without txt
        test_mail.template_name = 'test_no_txt'
        self.assertEqual(test_mail.create_email_msg(
            emails=['receiver@mail.com', ],
            from_email="receiver@mail.com", lang='fr').body,
            '# Français\n\n')
        #template without html and without txt
        test_mail.template_name = 'test_no_html_no_txt'

        with self.assertRaises(TemplateDoesNotExist):
            test_mail.create_email_msg(
                emails=['receiver@mail.com', ],
                from_email="receiver@mail.com", lang='fr')

    def test_create_email_msg_attachments(self):
        class TestMail(self.mail_class):
            params = []
            template_name = 'test'

        test_mail = TestMail()
        attachments = [
            (finders.find('admin/img/nav-bg.gif'), 'nav-bg.gif', 'image/png'),
            (finders.find('admin/css/base.css'), 'base.css', 'plain/text')]
        msg = test_mail.create_email_msg([], attachments=attachments)
        self.assertEqual(len(msg.attachments), 1) # base.css
        self.assertEqual(len(msg.related_attachments), 1) # nav-bg.gif

    def test_send(self):
        class TestMail(self.mail_class):
            params = []
            template_name = 'test'

        before = len(mail.outbox)

        task = TestMail().send(['foo@bar.com'])
        self.assertTrue(task.successful())
        self.assertEqual(task.get(), None)
        self.assertEqual(len(mail.outbox), before + 1)
        self.assertEqual(mail.outbox[-1].to, ['foo@bar.com'])

