import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


# readme
with open('README.md', 'rb') as f:
    long_desc = f.read().decode('utf-8')

# read requirements
with open('requirements.txt') as fd:
    req = fd.read().strip().split('\n')

setup(
    name='vat',
    version='1.0',
    description='A python package for dealing with VAT',
    long_description=long_desc,
    author='Alastair Houghton',
    author_email='alastair@alastairs-place.net',
    url='http://bitbucket.org/al45tair/vat',
    license='MIT License',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Office/Business :: Financial',
    ],
    tests_require=['pytest'],
    install_requires=req,
    provides=['vat']
)
