from setuptools import setup, find_packages
import os

version = open('version.txt').read().strip()

setup(name='david.profileview',
      version=version,
      description="BrowserView profiler",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='browserview profiler',
      author='David Batranu',
      author_email='dbatranu@gmail.com',
      url='http://github.com/david-batranu/david.profileview',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['david'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.api'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
