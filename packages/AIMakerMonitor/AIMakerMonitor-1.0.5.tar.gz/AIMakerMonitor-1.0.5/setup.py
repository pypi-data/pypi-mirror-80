# coding:utf-8

from setuptools import setup

version_file = open("AIMakerMonitor/VERSION", "r")
VERSION = version_file.readline()
version_file.close()

setup(
    name='AIMakerMonitor',
    version=VERSION,
    description='monitor the result from inference server',
    author='scott_su',
    author_email='scott_su@asus.com',
    packages=['AIMakerMonitor'],
    package_data={'AIMakerMonitor': ['VERSION']},
    install_requires=[
        'requests',
    ],
    license='MIT',
    zip_safe=False
)
