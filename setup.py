""" wgadmin
"""

from setuptools import setup, find_packages

setup(
    name='wgadmin',
    version='1.0',
    url='https://github.com/sinner-/wgadmin',
    author='Sina Sadeghi',
    description='WireGuard Admin',
    packages=find_packages(),
    install_requires=[
        'Flask-RESTful>=0.3.6',
    ],
    entry_points={
        'console_scripts': [
            'wg-api = wgadmin.cmd.api:main',
        ]},
)
