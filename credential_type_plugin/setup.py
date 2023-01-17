#!/usr/bin/env python

from setuptools import setup

requirements = ['pysafeguard']  # add Python dependencies here
# e.g., requirements = ["PyYAML"]

setup(
    name='safeguardcredentialtype',
    version='0.9.0',
    author='One Identity, Llc.',
    author_email='brad.nicholes@oneidentity.com',
    description='One Identity Safeguard Credential Type plugin for Ansible',
    long_description='',
    license='Apache 2.0',
    keywords='ansible, One Identity',
    url='http://oneidentity.com',
    packages=['safeguardcredentialtype'],
    include_package_data=True,
    zip_safe=False,
    setup_requires=[],
    install_requires=requirements,
    entry_points = {
        'awx.credential_plugins': [
            'spp_plugin = spp_custom_credential_plugin:spp_plugin',
        ]
    }
)
