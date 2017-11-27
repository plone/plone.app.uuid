# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '1.3.0.dev0'

long_description = '{0}\n{1}'.format(
    open('README.rst').read(),
    open('CHANGES.rst').read(),
)

setup(
    name='plone.app.uuid',
    version=version,
    description='Plone integration for the basic plone.uuid package',
    long_description=long_description,
    # Get more strings from
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 5.0',
        'Framework :: Plone :: 5.1',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='plone uuid',
    author='Martin Aspeli',
    author_email='optilude@gmail.com',
    url='http://plone.org',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['plone', 'plone.app', ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.uuid',
        'plone.indexer',
        'zope.publisher',
        'zope.interface',
    ],
    extras_require={
        'test': [
            'plone.dexterity',
            'plone.app.testing',
            'Products.Archetypes >= 1.7',
        ]
    },
    entry_points="""
    """,
)
