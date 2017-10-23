#!/usr/bin/env python

from setuptools import setup

setup(name='tap-reviewscouk',
      version='0.0.1',
      description='Singer.io tap for extracting data from reviews.co.uk',
      author='Onedox',
      url='https://github.com/onedox/tap-reviewscouk',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_reviewscouk'],
      install_requires=[
          'requests>=2.13.0',
          'singer-python>=1.4.2',
      ],
      entry_points='''
          [console_scripts]
          tap-reviewscouk=tap_reviewscouk:main
      ''',
      packages=['tap_reviewscouk'],
      package_data = {
          'tap_reviewscouk/schemas': [
              "merchant_reviews.json",
          ],
      },
      include_package_data=True,
)
