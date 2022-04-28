"""Setup.py for the Astronomer firebird Airflow provider package. Built from datadog provider package for now."""

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

"""Perform the package airflow-provider-firebird setup."""
setup(
    name='airflow-provider-firebird',
    version="0.0.1",
    description='A firebird provider package built by Leandro.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        "apache_airflow_provider": [
            "provider_info=firebird_provider.__init__:get_provider_info"
        ]
    },
    license='Apache License 2.0',
    packages=['firebird_provider', 'firebird_provider.hooks',
              'firebird_provider.sensors', 'firebird_provider.operators'],
    install_requires=['apache-airflow>=2.0'],
    setup_requires=['setuptools', 'wheel'],
    author='Leandro Jacomelli',
    author_email='leandro.jacomelli@gmail.com',
    url='https://github.com/lecomelli/',
    classifiers=[
        "Framework :: Apache Airflow",
        "Framework :: Apache Airflow :: Provider",
    ],
    python_requires='~=3.7',
)
