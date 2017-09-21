# -*- coding: utf-8 -*-
from plone.app.uuid.utils import uuidToURL
from plone.app.uuid.utils import uuidToObject
from zope.interface import implementer
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces import NotFound
from zope.location.interfaces import LocationError
from zope.traversing.interfaces import ITraversable
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName


@implementer(IPublishTraverse)
class RedirectToUUIDView(BrowserView):
    """A browser view that will cause a redirect to a given UUID,
    given via sub-path traversal.
    """

    uuid = None

    def publishTraverse(self, request, name):
        self.uuid = name
        return self

    def __call__(self):
        if self.uuid is None:
            raise KeyError(
                'No UUID given in sub-path. Use .../@@redirect-to-uuid/<uuid>'
            )

        url = uuidToURL(self.uuid)
        if url is None:
            raise NotFound(self, self.uuid)

        self.request.response.redirect(url)
        return u''


@implementer(ITraversable)
class UUIDTraverser(object):
    "a traversal namespace adapter for traversing to content by its uuid"


    def __init__(self, context, request):
        self.context = context
        self.request = request

    def traverse(self, uuid, remaining):
        "return object with a given uuid, raising NotFound if no such uuid is found"

        catalog = getToolByName(self.context, 'portal_catalog', None)
        if catalog is None:
            raise LocationError(uuid)

        result = catalog.unrestrictedSearchResults(UID=uuid)
        if len(result) != 1:
            raise LocationError(uuid)

        brain = result[0]

        # Fix the request so things behave the same as after normal traversal
        # by replacing the uuid traversal path with normal path
        # TODO: is there a cleaner way? How to fix request["PARENTS"]?
        uuid_path = "/++uuid++" + uuid
        brain_path = brain.getPath()
        site_path = '/'.join(self.context.getPhysicalPath())
        obj_path = brain_path[len(site_path):]
        for rvar in ("ACTUAL_URL" ,"URL", "PATH_INFO", "PATH_TRANSLATED"):
           self.request[rvar] = self.request[rvar].replace(uuid_path, obj_path)

        obj = brain._unrestrictedGetObject()
        return aq_inner(obj)
