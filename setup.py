# -*- coding: utf-8 -*-

version = '1.1.3'

from setuptools import setup, find_packages

long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(name='cpskin.agenda',
      version=version,
      description='Agenda package for cpskin',
      long_description=long_description,
      classifiers=[
          "Environment :: Web Environment",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Framework :: Plone",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
      ],
      keywords='',
      author='IMIO',
      author_email='support@imio.be',
      url='https://github.com/imio/',
      license='gpl',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'z3c.unconfigure',
          'Plone',
          'plone.api',
          'plone.app.contenttypes',
          'plone.app.event',
          'plone.behavior',
          'collective.contact.core',
          'eea.facetednavigation',
          'cpskin.locales',
          'cpskin.core',
      ],
      extras_require={
          'test': [
              'plone.app.robotframework',
          ]
      },
      entry_points={},
)
