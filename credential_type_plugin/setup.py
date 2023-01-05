#!/usr/bin/env python

from setuptools import setup

requirements = ['pysafeguard']  # add Python dependencies here
# e.g., requirements = ["PyYAML"]

setup(
    name='spp-custom-credential-plugin',
    version='0.1',
    author='One Identity, Llc.',
    author_email='brad.nicholes@oneidentity.com',
    description='',
    long_description='',
    license='Gnu Public License 3.0',
    keywords='ansible, One Identity',
    url='http://oneidentity.com',
    packages=['spp_custom_credential_plugin'],
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
