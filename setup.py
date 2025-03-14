from setuptools import setup, find_packages

setup(
    name="dns-rules-converter",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ipaddress>=1.0.23",
        "requests>=2.31.0",
    ],
    entry_points={
        'console_scripts': [
            'dns-converter=dns_rules_converter.main:main',
        ],
    },
) 