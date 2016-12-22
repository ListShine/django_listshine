import json
import logging
from abc import ABCMeta
from functools import partial

import requests

from django.conf import settings


logger = logging.getLogger(__name__)


class ListShineException(Exception):
    pass


class ListShineAPIKeyException(ListShineException):
    def __str__(self):
        return 'LISTSHINE_API_KEY not defined'


class LSConnection(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        if not settings.LISTSHINE_API_KEY:
            raise ListShineAPIKeyException
        headers = {'Authorization': 'Token %s' % settings.LISTSHINE_API_KEY}
        self.connection_post = partial(requests.post, headers=headers)
        self.connection_get = partial(requests.get, headers=headers)


class LSContact(LSConnection):
    URL_BASE = settings.LISTSHINE_API_BASE + 'escontact'

    def __init__(self, list_id):
        '''
        connection: obtain with Connection class
        list_id: list id from listshine_subscriber class or website
        '''
        super(LSContact, self).__init__()
        self.list_id = list_id

    def subscribe(self, email, **kwargs):
        ''' subscribe email to contactlist '''
        api_url = self.URL_BASE + '/contactlist/subscribe/{list_id}/'.format(list_id=self.list_id)
        kwargs.update({'email': email})
        result = self.connection_post(url=api_url, json=kwargs)
        logger.warn('posting to url %s', api_url)
        result.raise_for_status()
        return result

    def unsubscribe(self, email):
        ''' unsubscribe contact from contactlist '''
        api_url = self.URL_BASE + '/contactlist/{list_id}/contact/{id}/unsubscribe/'
        contacts = self.retrieve(email)
        for contact in contacts:
            api_url = api_url.format(list_id=self.list_id, id=contact.id)
            result = self.connection_post(api_url)
            result.raise_for_status()
            logger.warn('posting to url %s', api_url)
            yield result

    def retrieve(self, email):
        ''' retrieve contacts from contactlist that match email'''
        api_url = self.URL_BASE + '/contactlist/{list_id}/'.format(list_id=self.list_id)
        jsonfilter = {'jsonfilter': json.dumps({'email__equal': email})}
        result = self.connection_get(url=api_url, params=jsonfilter)
        logger.warn('getting from url %s', api_url)
        result.raise_for_status()
        for contact in result.json():
            if contact['list_id'] == self.list_id:
                yield contact

# class LSSubscriber:
#     URL_BASE = LISTSHINE_API_BASE + '/subscriber/contactlist'

#     def __init__(self):
#         pass

#     def all_contactlists(self):
#         data = requests.get(URL_BASE)
#         for contactlist in data:
#             yield contactlist

#     def get_list_by_id(self, contactlist_id):
#         data = requests.get(URL_BASE)
#         return data

# class LSSegment:
#     def all_segments(self):
#         pass

#     def get_segment_by_id(self, segment_id):
#         pass
