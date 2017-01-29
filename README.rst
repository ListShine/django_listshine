====================
django-listshine 1.0
====================


This is app that deals with subscribe/unsubscribe in ListShine mailing list system.

Quick start guide:
------------------

1. install django-listshine
   pip install django-listshine
2. Add LISTSHINE_API_KEY to your settings.py file
3. Add listshine to INSTALLED_APPS
4. Find out CONTACT_LIST_UUID from listshine application

API
---

1. Subscribing users

    from django_listshine.listshine.contactlist import LSContact
    connection = LSContact(list_id=<CONTACT_LIST_UUID>)
    connection.subscribe(email='test@email', firstname='test')

2. Unsubscribing users

    from django_listshine.listshine.contactlist import LSContact
    connection = LSContact(list_id=<CONTACT_LIST_UUID>)
    connection.unsubscribe(email='test@email')


Merge Vars
----------

When you are subscribing contacts you can use merge vars.
Following merge vars are supported:
* firstname
* lastname
* company
* website
* phone
* address
* city
* country
* custom
* custom2
* custom3
* custom3

Example
--------

To subscribe contact test@test.com with firstname "name" and lastname "surname"

    connection.subscribe(email='test@test.com', firstname='name', lastname='surname')
