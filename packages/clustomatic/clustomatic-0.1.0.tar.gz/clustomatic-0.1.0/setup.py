#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ["numpy", "pandas", "scikit-learn", "matplotlib"]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Ulysse Queritet-Diop",
    author_email='ulysse-q@evidenceb.com',
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
    description="clustomatic is a python package that displays a graph of clustered points with a dataframe in entry",
    entry_points={
        'console_scripts': [
            'clustomatic=clustomatic.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='clustomatic',
    name='clustomatic',
    packages=find_packages(include=['clustomatic', 'clustomatic.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ulysse-qd/clustomatic',
    version='0.1.0',
    zip_safe=False,
)
