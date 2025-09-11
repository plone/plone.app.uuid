Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

2.2.4 (2025-09-11)
------------------

Internal:


- Update configuration files.
  [plone devs] (6e36bcc4)
- Move distribution to src layout [gforcada] (#4217)


2.2.3 (2024-01-19)
------------------

Internal:


- Update configuration files.
  [plone devs] (7723aeaf)


2.2.2 (2023-03-22)
------------------

Internal:


- Update configuration files.
  [plone devs] (b2d5d4a5)


2.2.1 (2022-10-11)
------------------

Bug fixes:


- Process the catalog queue before looking up in the catalog
  [ale-rt] (#15)


2.2.0 (2022-08-30)
------------------

Bug fixes:


- Add optional security check for uuidToObject [anirudhhkashyap] (#13)


2.1.0 (2021-12-29)
------------------

New features:


- Speed up ``uuidToPhysicalPath`` and ``uuidToObject``.
  Do this by using an IndexQuery to only query the UID index.
  Note: of the four functions in ``utils.py``, only ``uuidToObject`` checks the security.
  For the other functions, it is up to the caller to do this, if needed.
  We may change this in the future, but for now the behavior should be the same as in previous versions.
  [maurits] (#11)


2.0.2 (2020-04-20)
------------------

Bug fixes:


- Minor packaging updates. (#1)


2.0.1 (2020-03-13)
------------------

Bug fixes:


- Fix use case where UID to object is failing.
  [rodfersou] (#8)
- Initialize towncrier.
  [gforcada] (#2548)


2.0.0 (2018-11-02)
------------------

Breaking changes:

- Fix test that fails since it raises zExceptions.NotFound instead of zope.publisher.interfaces.NotFound.
  (This makes the tests incompatible with Zope 2.13.)
  [pbauer]

Bug fixes:

- Fix deprecation warning on zope.site.hooks import.
  [pbauer]


1.2 (2017-07-03)
----------------

New features:

- Remove unittest2 dependency
  [kakshay21]


1.1.3 (2017-02-12)
------------------

Bug fixes:

- Fix test in Zope 4.
  [davisagli]


1.1.2 (2016-11-17)
------------------

Bug fixes:

- Update code to follow Plone styleguide.
  [gforcada]


1.1.1 (2016-08-10)
------------------

Fixes:

- Use zope.interface decorator.
  [gforcada]


1.1 (2014-02-19)
----------------

- Make the test setup independent from basic content types in the
  PLONE_FIXTURE.
  [timo]


1.0 - 2011-05-13
-----------------
- Release 1.0 Final.
  [esteele]

- Add MANIFEST.in.
  [WouterVH]


1.0b2 - 2011-01-03
------------------
- Use user id instead of user name to fix tests.
  [davisagli]


1.0b1 - 2010-11-27
------------------

- Initial release
