from setuptools import setup

setup(
    packages=['udn_cli'],
    install_requires=['urllib3==1.24', 'requests', 'boto3'],
    entry_points={
        'console_scripts': [
            'udn = udn_cli.main:main'
        ]}
)
