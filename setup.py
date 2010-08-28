from setuptools import setup, find_packages
import os

version = '1.0a1'

setup(name='plone.app.uuid',
      version=version,
      description="Plone integration for the basic plone.uuid package",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone uuid',
      author='Martin Aspeli',
      author_email='optilude@gmail.com',
      url='http://plone.org',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.uuid',
          'plone.indexer',
          'Plone',
      ],
      extras_require = {
        'test': ['plone.app.testing',]
      },
      entry_points="""
      """,
      )
