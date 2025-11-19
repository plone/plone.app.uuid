from setuptools import setup


version = "3.0.0a1.dev0"

long_description = "{}\n{}".format(
    open("README.rst").read(),
    open("CHANGES.rst").read(),
)

setup(
    name="plone.app.uuid",
    version=version,
    description="Plone integration for the basic plone.uuid package",
    long_description=long_description,
    # Get more strings from
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 6.2",
        "Framework :: Plone :: Core",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="plone uuid",
    author="Martin Aspeli",
    author_email="optilude@gmail.com",
    url="http://plone.org",
    license="GPL",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "Products.CMFCore",
        "Products.ZCatalog",
        "plone.uuid",
        "plone.indexer",
        "Zope",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.dexterity",
            "plone.testing",
        ]
    },
    entry_points="""
    """,
)
