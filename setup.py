#!/usr/bin/env python

from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='django-socialfeed',
    version='0.1',
    description='',
    long_description=read('README.rst'),
    author='Fabian Germann',
    author_email='fg@feinheit.ch',
    url='http://github.com/fabiangermann/',
    packages=find_packages(),
    package_data={
        '': ['*.html', '*.txt'],
        'socialfeed': [
            'locale/*/*/*.*',
            'templates/*.*',
            'templates/*/*.*',
            'templates/*/*/*.*',
            'templates/*/*/*/*.*',
        ],
    },
    install_requires=[
        'Django>=1.7.0',
        'pytz>=2014.7',
        'django-jsonfield==0.9.13',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)
