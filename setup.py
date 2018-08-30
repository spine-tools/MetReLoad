#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

from metreload import __version__ as version

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = ['Click >=6.0', 
                'pandas >=0.23.4',
                'xarray >=0.10.0',
                'Click >=6.0',
                'lxml >=4.1.1',
                'logzero >=1.5.0',
                'cython >=0.28.5',
                'netcdf4 >= 1.3.1',
                'dask >=0.16.1',
                'pydap >3.2.2']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Spine Project",
    author_email='spine_info@vtt.fi',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: LGPLv3 License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    description="Python application for downloading meteorological reanalysis data",
    entry_points={
        'console_scripts': [
            'metreload=metreload.cli:cli',
        ],
    },
    install_requires=requirements,
    license="LGPLv3 License",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=['reanalysis', 'data', 'meteorology'],
    name='MetReLoad',
    packages=find_packages(include=['metreload']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Spine-project/MetReLoad',
    version=version,
    zip_safe=False,
)
