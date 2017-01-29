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
    ''' connection class, used for connecting to ListShine API'''

    __metaclass__ = ABCMeta

    def __init__(self):
        if not settings.LISTSHINE_API_KEY:
            raise ListShineAPIKeyException
        headers = {'Authorization': 'Token %s' % settings.LISTSHINE_API_KEY}
        self.connection_post = partial(requests.post, headers=headers)
        self.connection_get = partial(requests.get, headers=headers)


class LSContact(LSConnection):
    ''' get information about single contact i.e. blah@blah.com'''

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
        response = self.connection_post(url=api_url, json=kwargs)
        logger.warn('posting to url %s', api_url)
        response.raise_for_status()
        return response

    def retrieve(self, email):
        ''' retrieve contacts from contactlist that match email'''
        api_url = self.URL_BASE + '/contactlist/{list_id}/'.format(list_id=self.list_id)
        jsonfilter = {'jsonfilter': json.dumps({'filters':
                                                [{'filter_type': 'equal',
                                                  'filter_field': 'contactlist_uuid',
                                                  'filter_value': self.list_id},
                                                 {'filter_type': 'equal',
                                                  'filter_field': 'email',
                                                  'filter_value': email}]})}
        response = self.connection_get(url=api_url, params=jsonfilter)
        logger.warn('getting from url %s', api_url)
        response.raise_for_status()
        return response

    def unsubscribe(self, email):
        ''' unsubscribe contact from contactlist '''
        api_url = self.URL_BASE + '/contactlist/{list_id}/contact/{id}/unsubscribe/'
        contacts = self.retrieve(email)
        for contact in contacts.json():
            api_url = api_url.format(list_id=self.list_id, id=contact['id'])
            response = self.connection_post(api_url)
            response.raise_for_status()
            logger.warn('posting to url %s', api_url)
            yield response


class LSContactList(LSConnection):
    ''' get information about contactlist '''

    URL_BASE = settings.LISTSHINE_API_BASE + 'contactlist'

    def __init__(self, list_id):
        '''
        connection: obtain with Connection class
        list_id: list id from listshine_subscriber class or website
        '''
        super(LSContactList, self).__init__()
        self.list_id = list_id

    def list(self):
        ''' list all contactlists '''
        return self.connection_get(url=self.URL_BASE)

    def retrieve(self):
        ''' details about each contactlist '''
        api_url = self.URL_BASE + '/{list_id}/'.format(list_id=self.list_id)
        return self.connection_get(url=api_url)

    # class LSSegment:
    #     def all_segments(self):
    #         pass

    #     def get_segment_by_id(self, segment_id):
    #         pass
