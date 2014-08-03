# coding=utf-8

""" :synopsis: Utilities """


from mail_factory import factory


def registered_mails_names():
    for k, v in factory._registry.items():
        yield k, v.__name__
    return
