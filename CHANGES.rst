Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

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
