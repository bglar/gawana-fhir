"""Gawana FHIR SERVER.

An implementation of https://www.hl7.org/fhir/
"""
import os
import re
import ast
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('fhir_server/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='gawana-fhir-server',
    version=version,
    license='Gawana',
    url='https://github.com/savannahinformatics/gawana_fhir_server/',
    author='Brian Ogollah',
    author_email='brian.ogollah@savannahinformatics.com',
    description='FHIR Profiling and Slicing.',
    long_description=README,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'alembic>=0.8.5',
        'Flask>=0.11.1',
        'Flask-Migrate>=1.8.0',
        'Flask-Script>=2.0.5',
        'Flask-SQLAlchemy>=2.1',
        'Flask-API>=0.6.6.post1',
        'Flask-OAuthlib>=0.9.3',
        'Flask-Cache>=0.13.1',
        'SQLAlchemy-Utils>=0.32.1',
        'psycopg2>=2.7.5',
        'SQLAlchemy>=1.0.12',
        'redis>=2.10.5',
        'celery>=3.1.23',

        'markdown>=2.6.6',
        'Sphinx>=1.3.6',
        'sphinx-autobuild>=0.6.0',

        'requests>=2.10.0',
        'language-tags>=0.4.1',
        'phonenumbers>=7.4.0',
        'PyJWT>=1.4.0',
        'pycountry>=1.20',
        'xmltodict>=0.10.2',
        'jsonschema>=2.5.1',
        'bleach>=1.4.3',
    ],
    keywords='FHIR Profiling Slicing',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: Gawana License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Clinical Informatics :: Interoperability',
    ],
)
