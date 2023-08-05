import plone.api
from plone.app.textfield.value import RichTextValue

from plone.namedfile.file import NamedBlobFile
from . import base


class TestTrashCan(base.IntegrationTestCase):

    def test_document(self):
        page = plone.api.content.create(id='page1', type='Document', title='My page', container=self.portal)
        page.text = RichTextValue('some text')
        plone.api.content.delete(page)
        self.assertEqual(len(self.can.objectIds()), 1)

    def test_file(self):
        _file = plone.api.content.create(id='file1', type='File', title='My file', container=self.portal)
        plone.api.content.delete(_file)
        self.assertEqual(len(self.can.objectIds()), 1)

    def test_file_limit(self):
        _file = plone.api.content.create(id='file1', type='File', title='My file', container=self.portal)
        _file.file = NamedBlobFile()
        _file.file.data = 'hello, world'
        _file.file.__dict__['size'] = 1e10  # fake it
        plone.api.content.delete(_file)
        self.assertEqual(len(self.can.objectIds()), 0)


def test_suite():
    import unittest
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
