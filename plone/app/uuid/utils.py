# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.ZCatalog.query import IndexQuery
from zope.component.hooks import getSite


def uuidToPhysicalPath(uuid):
    """Given a UUID, attempt to return the absolute path of the underlying
    object. Will return None if the UUID can't be found.

    This version is four times faster than the original.
    """
    site = getSite()
    if site is None:
        return None
    catalog = getToolByName(site, 'portal_catalog', None)
    if catalog is None:
        return None
    index = catalog.Indexes["UID"]
    # This works even faster, but uses a private attribute:
    # rid = index._index.get(uuid)
    # if not rid:
    #     return
    query = IndexQuery({"UID": uuid}, "UID")
    result = index.query_index(query)
    if not result:
        return
    rid = result[0]
    path = catalog.getpath(rid)
    return path


def uuidToURL(uuid):
    """Given a UUID, attempt to return the absolute URL of the underlying
    object. Will return None if the UUID can't be found.
    """

    brain = uuidToCatalogBrain(uuid)
    if brain is None:
        return None

    return brain.getURL()


def uuidToObject(uuid):
    """Given a UUID, attempt to return a content object. Will return
    None if the UUID can't be found.
    """
    path = uuidToPhysicalPath(uuid)
    if not path:
        return
    site = getSite()
    if site is None:
        return
    return site.restrictedTraverse(path)


def uuidToCatalogBrain(uuid):
    """Given a UUID, attempt to return a catalog brain.
    """

    site = getSite()
    if site is None:
        return None

    catalog = getToolByName(site, 'portal_catalog', None)
    if catalog is None:
        return None

    result = catalog.unrestrictedSearchResults(UID=uuid)
    if len(result) != 1:
        return None

    return result[0]
