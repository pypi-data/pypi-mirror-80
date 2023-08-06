"""
CRAYopt - yet another black-box optimization toolkit.
"""

from setuptools import setup, find_packages
import os

here = os.path.dirname(__file__)

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
  long_description=f.read()

version = '0.3.0'

setup(
  name = 'crayopt',
  version=version,
  description="""Yet another black-box optimization toolkit.""",

  long_description=long_description,
  long_description_content_type="text/markdown",

  url='https://gitlab.com/craynn/crayopt',

  author='Maxim Borisyak and contributors.',
  author_email='maximus.been@gmail.com',

  maintainer='Maxim Borisyak',
  maintainer_email='maximus.been@gmail.com',

  license='MIT',

  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],

  packages=find_packages(exclude=['contrib', 'examples', 'docs', 'tests']),

  extras_require={
    'test': [
      'pytest >= 6.0.0',
    ],

    'visualization': [
      'matplotlib >= 3.3.1',
      'ffmpeg-python >= 0.2.0',
      'pillow >= 7.2.0'
    ]
  },

  install_requires=[
    'numpy >= 1.17.1',
    'craygraph >= %s' % (version, ),
    'craynn >= %s' % (version, ),

    'tensorflow >= 2.3.0',
  ],

  python_requires='>=3.7',
)