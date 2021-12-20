Speed up ``uuidToPhysicalPath`` and ``uuidToObject``.
Do this by using an IndexQuery to only query the UID index.
``uuidToPhysicalPath`` no longer checks security, ``uuidToObject`` still does.
[maurits]
