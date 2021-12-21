Speed up ``uuidToPhysicalPath`` and ``uuidToObject``.
Do this by using an IndexQuery to only query the UID index.
Note: none of the functions check security.
It is up to the caller to do this, if needed.
[maurits]
