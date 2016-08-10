from setuptools import setup, find_packages

version = '1.1.2.dev0'

setup(
    name='plone.app.uuid',
    version=version,
    description="Plone integration for the basic plone.uuid package",
    long_description=(open("README.rst").read() + "\n" +
                      open("CHANGES.rst").read()),
    # Get more strings from
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2.6',
        "Programming Language :: Python :: 2.7",
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
        'zope.publisher',
        'zope.interface',
    ],
    extras_require={
        'test': [
            'plone.dexterity',
            'plone.app.testing',
            'Products.Archetypes >= 1.7'
        ]
    },
    entry_points="""
    """,
    )
