django-mail-factory-extras
==========================

Extra features for `django-mail-factory <https://github.com/novapost/django-mail-factory>`_.


New features:
-------------

  * SMS factory to handle SMS like mails, Twilio integration implemented.
  * Async email class to send email via celery.
  
  
SMS Factory:
------------

* Defining SMS templates:

  + Define your templates inside a folder ``templates/sms/<template_name>/body.html``.

  
* Registering a SMS message using Twilio backend (Twilio python client needed):

  .. code:: python
  
    from mailfactory_extras import smsfactory
    from mailfactory_extras.sms.twilio.sms import TwilioSMS
  
  
    class InvitationSMS(TwilioSMS):
        template_name = "invitation"
        params = ['user']
        
  
    smsfactory.register(InvitationSMS)


  + ``template_name`` defines the name of the template to use.
  + ``params`` is the dict with the context variables the template will receive.


* Sending SMS, just call ``send()`` from the smsfactory:


  .. code:: python
  
    from mailfactory_extras import smsfactory
    
    smsfactory.send('invitation', {'user': 'Foo'})


Async email class:
-------------------

Define your email class using ``CeleryMail``.


.. code:: python
  
    from mail_factory import factory
    from mailfactory_extras.backends.celery import CeleryMail
  
  
    class InvitationAsyncEmail(CeleryMail):
        template_name = "invitation"
        params = ['user']
        
  
    factory.register(InvitationAsyncEmail)
