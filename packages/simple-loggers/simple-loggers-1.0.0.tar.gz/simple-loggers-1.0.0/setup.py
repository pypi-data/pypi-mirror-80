# -*- encoding: utf8 -*-
import os
from setuptools import setup, find_packages


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
from simple_loggers import __version__, __author__, __author_email__


setup(
    name='simple-loggers',
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    description='A Simple Logger Package',
    long_description=open(os.path.join(BASE_DIR, 'README.md')).read(),
    long_description_content_type="text/markdown",
    url='https://github.com/suqingdong/simple-loggers',
    project_urls={
        'Tracker': 'https://github.com/suqingdong/simple-loggers/issues',
    },
    license='BSD License',
    install_requires=['coloredlogs'],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ]
)
