from AccessControl import Unauthorized
from Products.CMFCore.indexing import processQueue
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
            if request is not None:
                request._catalog = None
            return
        catalog = getToolByName(site, "portal_catalog", None)
        if request is not None:
            request._catalog = catalog
        return catalog


def uuidToPhysicalPath(uuid):
    """Given a UUID, attempt to return the absolute path of the underlying
    object. Will return None if the UUID can't be found.

    This version is four times faster than the original.

    Note: the user may not be authorized to view the object at this path.
    It is up to the caller to check this, if needed.
    """
    catalog = _catalog()
    if catalog is None:
        return
    index = catalog.Indexes["UID"]

    # Process the catalog queue in case we have pending relevant operations
    processQueue()
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

    Note: the user may not be authorized to view the object at the url.
    It is up to the caller to check this, if needed.
    """

    brain = uuidToCatalogBrain(uuid)
    if brain is None:
        return None

    return brain.getURL()


def uuidToObject(uuid, unrestricted=False):
    """Given a UUID, attempt to return a content object. Will return
    None if the UUID can't be found.

    Note: the user may not be authorized to view the object.
    It is up to the caller to check this, if needed.

    If the author is authorised to view the object, unrestricted flag should be set to True
    """
    path = uuidToPhysicalPath(uuid)
    if not path:
        return
    site = getSite()
    if site is None:
        return
    # Go to the parent of the item without restrictions.
    parent_path, final_path = path.rpartition("/")[::2]
    parent = site.unrestrictedTraverse(parent_path)
    # Do check restrictions for the final object.
    # Check if the object has restrictions
    if unrestricted:
        return parent.unrestrictedTraverse(final_path)
    return parent.restrictedTraverse(final_path)


def uuidToCatalogBrain(uuid):
    """Given a UUID, attempt to return a catalog brain.

    Note: the user may not be authorized to view the object for this brain.
    It is up to the caller to check this, if needed.
    """
    catalog = _catalog()
    if catalog is None:
        return
    result = catalog.unrestrictedSearchResults(UID=uuid)
    if len(result) != 1:
        return None

    return result[0]
