Introduction
============

This package integrates the low-level `plone.uuid`_ into Plone-the-
application. In particular, it:

* Ensures that all CMF content is given a UUID when created, by marking
  the ``DynamicType`` class with ``plone.uuid.interfaces.IAttributeUUID``.
* Registers a ``portal_catalog`` indexer called ``uuid`` that allows an
  object's UUID to be indexed.
* Registers a ``FieldIndex`` and a catalog metadata column containing the
  UUID.
* Registers a utility view, ``@@redirect-to-uuid``. You can use this with
  a URL like::
  
    http://example.org/some/path/@@redirect-to-uuid/b2dc6f7a-9d17-11df-8788-58b035f3cfa0
  
  This will then redirect to the object identified by that URL.
  
    *Hint:* You can use the ``@@uuid`` view from `plone.uuid`_ to render a
    UUID. In TAL, you can do something like::
    
        <a tal:attributes="href string:${portal_url}/@@redirect-to-uuid/${obj/@@uuid}">Click here</a>
* Provides several utility methods in the ``plone.app.uuid.utils`` module:
  
  ``uuidToPhysicalPath(uuid)``
      Returns the physical path (relative to the ZODB root) as a string of the
      object with the given UUID, or None if it cannot be found.
  
  ``uuidToURL(uuid)``
      Returns the absolute URL of the object with the given UUID, or None if it
      cannot be found.
  
  ``uuidToObject(uuid)``
      Returns the content object associated with the given UUID, or None if it
      cannot be found.

Please see the `plone.uuid`_ package for more details about how UUIDs are
generated and can be accessed.

.. _plone.uuid: http://pypi.python.org/pypi/plone.uuid
