import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

version = os.getenv('TRAVIS_TAG')
if not version:
    version = os.getenv('TRAVIS_COMMIT')

setup(
    name='django-ad-import',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    license='GPL',
    description='A django app to import information from Active Directory to a database',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/StorFollo-IKT/django-ad-import',
    author='Anders Birkenes',
    author_email='anders.birkenes@storfolloikt.no',
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ], install_requires=['django>=2,<4']
)
