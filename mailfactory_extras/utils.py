# coding=utf-8

""" :synopsis: Utilities """


from mail_factory import factory


def registered_mails_names():
    return zip(factory.mail_map.keys(), factory.mail_map.keys())
