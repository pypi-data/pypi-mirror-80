#!/usr/bin/env python

from os.path import abspath, dirname, join
from setuptools import setup, find_packages

ROOT = dirname(abspath(__file__))

version_file = join(ROOT, 'perfecto', 'version.py')
exec (compile(open(version_file).read(), version_file, 'exec'))

setup(name='perfecto_py37',
      version=VERSION,
      description='Perfecto smart reporting lib',
#       long_description=open(join(ROOT, 'README.rst')).read(),
      author='Perfecto PS',
      author_email='Professional Services <professionalservices@perfectomobile.com>',
      url='https://gitlab.com/perfectops/perfecto-python37',
      license='http://www.apache.org/licenses/LICENSE-2.0',
      keywords='Perfecto smart reporting python',
      platforms='any',
      classifiers=[
          "Development Status :: 3 - Alpha",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Software Development :: Testing",
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7'
      ],
      install_requires=[
      ],
      packages=find_packages(exclude=["demo", "docs", "tests", ]),
      include_package_data=True,
      )
