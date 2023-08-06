#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
from fopy import __version__

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['numpy>=1.14.0', 'sympy>= 1.5.0', 'pandas>=1.0.0', 'Click>=7.0', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Abdulaziz Alqasem",
    author_email='Aziz_Alqasem@hotmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A Python package that makes working with math formulas convienant, powerfull and fast. ",
    entry_points={
        'console_scripts': [
            'fopy=fopy.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='fopy',
    name='fopy',
    packages=find_packages(include=['fopy', 'fopy.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/AzizAlqasem/fopy',
    version=__version__,
    zip_safe=False,
)
