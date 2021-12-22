Speed up ``uuidToPhysicalPath`` and ``uuidToObject``.
Do this by using an IndexQuery to only query the UID index.
Note: of the four functions in ``utils.py``, only ``uuidToObject`` checks the security.
For the other functions, it is up to the caller to do this, if needed.
We may change this in the future, but for now the behavior should be the same as in previous versions.
[maurits]
