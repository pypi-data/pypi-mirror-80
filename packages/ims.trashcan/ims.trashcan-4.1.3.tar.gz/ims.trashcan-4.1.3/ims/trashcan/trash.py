import plone.api
from DateTime import DateTime
from OFS.ObjectManager import ObjectManager
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from ZODB.blob import Blob
from zope.interface.declarations import implementer

from .interfaces import ITrashedItem


@implementer(ITrashedItem)
class TrashedItem(ObjectManager):
    manage_main = PageTemplateFile('www/manage_trashedItem', globals())
    _created = ''

    def __init__(self, id, title='', data=None, path=''):
        self.id = id
        self.data = Blob(data)
        self.path = path
        self.Title = title
        self._created = DateTime()

    def manage_properties(self):
        return {
            'title': self.Title,
            'created': plone.api.portal.get_localized_time(self._created, long_format=True),
            'id': self.id,
            'path': self.path,
        }

    def created(self):
        return self._created

    def getId(self):
        """ needed for indexing """
        return self.id
