# -*- coding: utf-8 -*-
from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName
from Products.ZCatalog.query import IndexQuery
from zope.component.hooks import getSite
from zope.globalrequest import getRequest


def _catalog():
    """Get and store portal_catalog on request.

    This avoids looking up the site and the portal_catalog
    each time one of the below functions is called.
    """
    request = getRequest()
    try:
        return request._catalog
    except AttributeError:
        site = getSite()
        if site is None:
            request._catalog = None
            return
        catalog = request._catalog = getToolByName(site, 'portal_catalog', None)
        return catalog


def uuidToPhysicalPath(uuid):
    """Given a UUID, attempt to return the absolute path of the underlying
    object. Will return None if the UUID can't be found.

    This version is four times faster than the original.
    Downside: it no longer automatically checks if the user is allowed
    to see the object at the path.  This is now the responsibility
    of the caller.  See the updated code in uuidToObject.
    """
    catalog = _catalog()
    if catalog is None:
        return
    index = catalog.Indexes["UID"]
    try:
        # This uses a private attribute, so be careful.
        rid = index._index.get(uuid)
    except AttributeError:
        # Fall back to IndexQuery.
        query = IndexQuery({"UID": uuid}, "UID")
        result = index.query_index(query)
        if not result:
            return
        rid = result[0]
    if not rid:
        return
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
    # Go to the parent of the item without restrictions.
    split_path = path.split("/")
    parent_path = split_path[:-1]
    parent = site.unrestrictedTraverse(parent_path)
    # Do check restrictions for the final object.
    final_path = split_path[-1]
    try:
        return parent.restrictedTraverse(final_path)
    except Unauthorized:
        return


def uuidToCatalogBrain(uuid):
    """Given a UUID, attempt to return a catalog brain.
    """
    catalog = _catalog()
    if catalog is None:
        return
    result = catalog.unrestrictedSearchResults(UID=uuid)
    if len(result) != 1:
        return None

    return result[0]
