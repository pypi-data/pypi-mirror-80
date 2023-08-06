  
#!/usr/bin/env python3
import sys
from setuptools import find_packages, setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 5)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of Django REST Framework requires Python {}.{}, but you're trying
to install it on Python {}.{}.
This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:
    $ python -m pip install --upgrade pip setuptools
    $ python -m pip install djangorestframework
This will install the latest version of Django REST Framework which works on
your version of Python. If you can't upgrade your pip (or Python), request
an older version of Django REST Framework:
    $ python -m pip install "djangorestframework<3.10"
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='django-rest-swagger-master',
    version='1.0.5',
    url='https://github.com/crazy-coding/django-rest-swagger-master',
    license='BSD',
    description='Django Template with Template, Restframework and Swagger.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Dennis Cho',
    author_email='dennischo122@gmail.com',  # SEE NOTE BELOW (*)
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=["django>=2.2"],
    python_requires=">=3.5",
    zip_safe=False,
    classifiers=[
        # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
    ]
)