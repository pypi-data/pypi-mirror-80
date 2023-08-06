#!/usr/bin/env python

from setuptools import setup

version = '2.0.3'
repo_url = 'https://github.com/agerasev/test_cmd_x'
download_url = repo_url + '/tarball/' + version

setup(name='test_cmd_x',
      version=version,
      description='Tool for black-box testing command-line programs, with extensions',
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      url=repo_url,
      download_url=download_url,
      author='Alexey Gerasev',
      author_email='nthend.iipa@gmail.com',
      keywords='command line terminal functional black box testing arguments stdin stdout stderr',
      license='Apache',
      py_modules=['test_cmd_x'],
      entry_points = {
        'console_scripts': ['test_cmd_x=test_cmd_x:main'],
      },
      classifiers=[
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: Apache Software License',
        'Environment :: Console'
      ])
