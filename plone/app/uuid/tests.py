from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()

class UUIDLayer(PloneSite):
    @classmethod
    def setUp(cls):
        from Products.Five import zcml
        from Products.Five import fiveconfigure
        
        import plone.app.uuid
        
        fiveconfigure.debug_mode = True
        zcml.load_config('configure.zcml', plone.app.uuid)
        fiveconfigure.debug_mode = False
    
    @classmethod
    def tearDown(cls):
        pass

class IntegrationTestCase(ptc.PloneTestCase):
    layer = UUIDLayer
    
    def afterSetUp(self):
        self.addProfile('plone.app.uuid:default')
    
    def test_catalog_setup(self):
        self.failUnless('uuid' in self.portal['portal_catalog'].schema())
        self.failUnless('uuid' in self.portal['portal_catalog'].indexes())
    
    def test_assignment(self):
        from plone.uuid.interfaces import IUUID
        
        self.folder.invokeFactory('Document', 'd1')
        
        d1 = self.folder['d1']
        uuid = IUUID(d1)
        
        self.assertTrue(isinstance(uuid, str))
    
    def test_search(self):
        from plone.uuid.interfaces import IUUID
        
        self.folder.invokeFactory('Document', 'd1')
        self.folder.invokeFactory('Document', 'd2')
        
        d1 = self.folder['d1']
        uuid = IUUID(d1)
        
        catalog = self.portal['portal_catalog']
        results = catalog(uuid=uuid)
        
        self.assertEqual(1, len(results))
        self.assertEqual(uuid, results[0].uuid)
        self.assertEqual('/'.join(d1.getPhysicalPath()), results[0].getPath())
    
    def test_uuidToPhysicalPath(self):
        from plone.uuid.interfaces import IUUID
        from plone.app.uuid.utils import uuidToPhysicalPath
        
        self.folder.invokeFactory('Document', 'd1')
        self.folder.invokeFactory('Document', 'd2')
        
        d1 = self.folder['d1']
        uuid = IUUID(d1)
        
        self.assertEqual('/'.join(d1.getPhysicalPath()), uuidToPhysicalPath(uuid))
    
    def test_uuidToURL(self):
        from plone.uuid.interfaces import IUUID
        from plone.app.uuid.utils import uuidToURL
        
        self.folder.invokeFactory('Document', 'd1')
        self.folder.invokeFactory('Document', 'd2')
        
        d1 = self.folder['d1']
        uuid = IUUID(d1)
        
        self.assertEqual(d1.absolute_url(), uuidToURL(uuid))
    
    def test_uuidToObject(self):
        from Acquisition import aq_base
        from plone.uuid.interfaces import IUUID
        from plone.app.uuid.utils import uuidToObject
        
        self.folder.invokeFactory('Document', 'd1')
        self.folder.invokeFactory('Document', 'd2')
        
        d1 = self.folder['d1']
        uuid = IUUID(d1)
        
        self.assertEqual(aq_base(d1), aq_base(uuidToObject(uuid)))

class FunctionalTestCase(ptc.FunctionalTestCase):
    layer = UUIDLayer
    
    def afterSetUp(self):
        self.addProfile('plone.app.uuid:default')
    
    def test_uuid_view(self):
        from plone.uuid.interfaces import IUUID
        
        self.folder.invokeFactory('Document', 'd1')
        
        d1 = self.folder['d1']
        uuid = IUUID(d1)
        
        import transaction
        transaction.commit()
        
        from Products.Five.testbrowser import Browser
        browser = Browser()
        browser.addHeader('Authorization', 'Basic %s:%s' % (ptc.default_user, ptc.default_password,))
        
        browser.open("%s/@@uuid" % d1.absolute_url())
        self.assertEqual(uuid, browser.contents)
        
    def test_redirect_to_uuid_view(self):
        from plone.uuid.interfaces import IUUID
        
        self.folder.invokeFactory('Document', 'd1')
        self.folder.invokeFactory('Document', 'd2')
        
        d1 = self.folder['d1']
        uuid = IUUID(d1)
        
        import transaction
        transaction.commit()
        
        from Products.Five.testbrowser import Browser
        browser = Browser()
        browser.addHeader('Authorization', 'Basic %s:%s' % (ptc.default_user, ptc.default_password,))
        
        browser.open("%s/@@redirect-to-uuid/%s" % (self.portal.absolute_url(), uuid,))
        self.assertEqual(d1.absolute_url(), browser.url)
