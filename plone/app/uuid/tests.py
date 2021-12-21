# -*- coding: utf-8 -*-
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.zope import Browser
from plone.app.uuid.testing import PLONE_APP_UUID_FUNCTIONAL_TESTING
from plone.app.uuid.testing import PLONE_APP_UUID_INTEGRATION_TESTING

import os
import time
import transaction
import unittest


class IntegrationTestCase(unittest.TestCase):
    layer = PLONE_APP_UUID_INTEGRATION_TESTING

    def test_assignment(self):
        from plone.uuid.interfaces import IUUID

        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])

        portal.invokeFactory('Document', 'd1')

        d1 = portal['d1']
        uuid = IUUID(d1)

        self.assertTrue(isinstance(uuid, str))

    def test_search(self):
        from plone.uuid.interfaces import IUUID

        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])

        portal.invokeFactory('Document', 'd1')
        portal.invokeFactory('Document', 'd2')

        d1 = portal['d1']
        uuid = IUUID(d1)

        catalog = portal['portal_catalog']
        results = catalog(UID=uuid)

        self.assertEqual(1, len(results))
        self.assertEqual(uuid, results[0].UID)
        self.assertEqual('/'.join(d1.getPhysicalPath()), results[0].getPath())

    def test_uuidToPhysicalPath(self):
        from plone.uuid.interfaces import IUUID
        from plone.app.uuid.utils import uuidToPhysicalPath

        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])

        portal.invokeFactory('Document', 'd1')
        portal.invokeFactory('Document', 'd2')

        d1 = portal['d1']
        uuid = IUUID(d1)

        self.assertEqual('/'.join(d1.getPhysicalPath()),
                         uuidToPhysicalPath(uuid))
        self.assertIsNone(uuidToPhysicalPath('unknown'))

    def test_speed(self):
        # I updated some of the utility functions to be a bit faster.
        # In this function you can check the speed.
        from Acquisition import aq_base
        from plone.uuid.interfaces import IUUID
        from plone.app.uuid.utils import uuidToPhysicalPath
        from plone.app.uuid.utils import uuidToURL
        from plone.app.uuid.utils import uuidToObject
        from plone.app.uuid.utils import uuidToCatalogBrain

        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])

        start = time.time()
        uuids = {}

        # Read env variable to see how many items to create.
        # If we have a variable, do some printing.
        total = os.getenv("PLONE_APP_UUID_TEST_SPEED_TOTAL")
        if total:
            report = True
            total = int(total)
            print("Creating {} documents...".format(total))
        else:
            report = False
            total = 40
        for i in range(total):
            doc_id = portal.invokeFactory('Document', 'd{}'.format(i))
            doc = portal[doc_id]
            uuids[IUUID(doc)] = {
                'path': '/'.join(doc.getPhysicalPath()),
                'url': doc.absolute_url(),
                'obj': aq_base(doc),
            }
        end = time.time()
        if report:
            print("Time taken to create {} items: {}".format(total, end - start))

        self.assertEqual(len(uuids), total)
        start = time.time()
        for uuid, info in uuids.items():
            self.assertEqual(info['path'], uuidToPhysicalPath(uuid))
        end = time.time()
        if report:
            print("Time taken for uuidToPhysicalPath: {}".format(end - start))

        start = time.time()
        for uuid, info in uuids.items():
            self.assertEqual(info['url'], uuidToURL(uuid))
        end = time.time()
        if report:
            print("Time taken for uuidToURL: {}".format(end - start))

        start = time.time()
        for uuid, info in uuids.items():
            self.assertEqual(info['obj'], aq_base(uuidToObject(uuid)))
        end = time.time()
        if report:
            print("Time taken for uuidToObject: {}".format(end - start))

        start = time.time()
        for uuid, info in uuids.items():
            self.assertEqual(info['path'], uuidToCatalogBrain(uuid).getPath())
        end = time.time()
        if report:
            print("Time taken for uuidToCatalogBrain: {}".format(end - start))

    def test_uuidToURL(self):
        from plone.uuid.interfaces import IUUID
        from plone.app.uuid.utils import uuidToURL

        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])

        portal.invokeFactory('Document', 'd1')
        portal.invokeFactory('Document', 'd2')

        d1 = portal['d1']
        uuid = IUUID(d1)

        self.assertEqual(d1.absolute_url(), uuidToURL(uuid))
        self.assertIsNone(uuidToURL('unknown'))

    def test_uuidToObject(self):
        from Acquisition import aq_base
        from plone.uuid.interfaces import IUUID
        from plone.app.uuid.utils import uuidToObject

        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])

        portal.invokeFactory('Document', 'd1')
        portal.invokeFactory('Document', 'd2')

        d1 = portal['d1']
        uuid = IUUID(d1)

        self.assertEqual(aq_base(d1), aq_base(uuidToObject(uuid)))
        self.assertIsNone(uuidToObject('unknown'))

    def test_uuidToCatalogBrain(self):
        from Acquisition import aq_base
        from plone.uuid.interfaces import IUUID
        from plone.app.uuid.utils import uuidToCatalogBrain

        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])

        portal.invokeFactory('Document', 'd1')
        portal.invokeFactory('Document', 'd2')

        d1 = portal['d1']
        uuid = IUUID(d1)

        self.assertEqual('/'.join(d1.getPhysicalPath()), uuidToCatalogBrain(uuid).getPath())
        self.assertIsNone(uuidToCatalogBrain('unknown'))

    def test_access_private_published(self):
        from Acquisition import aq_base
        from plone.uuid.interfaces import IUUID
        from plone.app.uuid.utils import uuidToPhysicalPath
        from plone.app.uuid.utils import uuidToURL
        from plone.app.uuid.utils import uuidToObject
        from plone.app.uuid.utils import uuidToCatalogBrain

        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        wftool = portal.portal_workflow
        wftool.setDefaultChain("simple_publication_workflow")

        # Create private folder.
        portal.invokeFactory('Folder', 'private')
        private = portal.private
        private_url = private.absolute_url()
        private_uuid = IUUID(private)
        private_path = '/'.join(private.getPhysicalPath())

        # Create public document in private folder.
        private.invokeFactory('Document', 'published')
        wftool.doActionFor(portal.private.published, 'publish')
        published = private.published
        published_url = published.absolute_url()
        published_uuid = IUUID(published)
        published_path = '/'.join(published.getPhysicalPath())

        # Check that the review states are what we expect.
        self.assertEqual(wftool.getInfoFor(private, 'review_state'), 'private')
        self.assertEqual(wftool.getInfoFor(published, 'review_state'), 'published')

        # The test user can obviously see the published item.
        self.assertEqual(published_path, uuidToPhysicalPath(published_uuid))
        self.assertEqual(published_url, uuidToURL(published_uuid))
        self.assertEqual(published_path, uuidToCatalogBrain(published_uuid).getPath())
        self.assertEqual(aq_base(published), aq_base(uuidToObject(published_uuid)))

        # The test user, which here has a Manager role, can see the private item.
        self.assertEqual(private_path, uuidToPhysicalPath(private_uuid))
        self.assertEqual(private_url, uuidToURL(private_uuid))
        self.assertEqual(private_path, uuidToCatalogBrain(private_uuid).getPath())
        self.assertEqual(aq_base(private), aq_base(uuidToObject(private_uuid)))

        # Anonymous can see the published item.
        logout()
        self.assertEqual(published_path, uuidToPhysicalPath(published_uuid))
        self.assertEqual(published_url, uuidToURL(published_uuid))
        self.assertEqual(published_path, uuidToCatalogBrain(published_uuid).getPath())
        self.assertEqual(aq_base(published), aq_base(uuidToObject(published_uuid)))

        # Anonymous cannot see the private item, except for the physical path.
        self.assertEqual(private_path, uuidToPhysicalPath(private_uuid))
        self.assertIsNone(uuidToURL(private_uuid))
        self.assertIsNone(uuidToCatalogBrain(private_uuid))
        self.assertIsNone(uuidToObject(private_uuid))


class FunctionalTestCase(unittest.TestCase):

    layer = PLONE_APP_UUID_FUNCTIONAL_TESTING

    def test_uuid_view(self):

        from plone.uuid.interfaces import IUUID

        portal = self.layer['portal']
        app = self.layer['app']

        setRoles(portal, TEST_USER_ID, ['Manager'])

        portal.invokeFactory('Document', 'd1')

        d1 = portal['d1']
        uuid = IUUID(d1)

        transaction.commit()

        browser = Browser(app)
        browser.addHeader(
            'Authorization',
            'Basic {0}:{1}'.format(TEST_USER_ID, TEST_USER_PASSWORD, )
        )

        browser.open('{0}/@@uuid'.format(d1.absolute_url()))
        self.assertEqual(uuid, browser.contents)

    def test_redirect_to_uuid_view(self):
        from plone.uuid.interfaces import IUUID

        portal = self.layer['portal']
        app = self.layer['app']

        setRoles(portal, TEST_USER_ID, ['Manager'])

        portal.invokeFactory('Document', 'd1')
        portal.invokeFactory('Document', 'd2')

        d1 = portal['d1']
        uuid = IUUID(d1)

        transaction.commit()

        browser = Browser(app)
        browser.addHeader(
            'Authorization',
            'Basic {0}:{1}'.format(TEST_USER_ID, TEST_USER_PASSWORD,)
        )

        url = '{0}/@@redirect-to-uuid/{1}'
        browser.open(url.format(portal.absolute_url(), uuid,))
        self.assertEqual(d1.absolute_url(), browser.url)

    def test_redirect_to_uuid_invalid_uuid(self):
        portal = self.layer['portal']
        app = self.layer['app']

        setRoles(portal, TEST_USER_ID, ['Manager'])

        transaction.commit()

        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader(
            'Authorization',
            'Basic {0}:{1}'.format(TEST_USER_ID, TEST_USER_PASSWORD, )
        )

        url = '{0}/@@redirect-to-uuid/gibberish'.format(portal.absolute_url())
        from zExceptions import NotFound
        with self.assertRaises(NotFound):
            browser.open(url)
