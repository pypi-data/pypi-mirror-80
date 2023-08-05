#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Haeckel K",
    author_email='haeckelk.github@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Aid writing boilerplate SQL items from create tables, inserts and updates.",
    entry_points={
        'console_scripts': [
            'devtools_shorthand_sql=devtools_shorthand_sql.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    # long_description=readme + '\n\n' + history,
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='devtools_shorthand_sql',
    name='devtools_shorthand_sql',
    packages=find_packages(include=['devtools_shorthand_sql', 'devtools_shorthand_sql.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/HaeckelK/devtools_shorthand_sql',
    version='0.4.0',
    zip_safe=False,
)
