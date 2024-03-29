from setuptools import setup

setup(
    name='UDN-CLI',
    packages=['udn_cli'],
    install_requires=[
        'urllib3==1.25.4',
        'requests',
        'boto3'
    ],
    entry_points={
        'console_scripts': [
            'udn = udn_cli.main:main'
        ]},
    version='0.2.1'
)
