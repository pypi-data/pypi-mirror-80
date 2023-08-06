#!/usr/bin/env python3
from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='snxtray',
    version='0.0.1',
    scripts=['snxtray'],
    install_requires=['psutil==5.7.0', 'wxPython'],
    packages=find_packages(),
    url='https://gitlab.com/linalinn/snxtray',
    license='Mozilla Public License Version 2.0',
    author='LinaLinn',
    author_email='lina.cloud@outlook.de',
    description='Systray for snx',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    data_files=[('icon', ['icon/lockWithe.png', 'icon/lockGreen.png', 'icon/lockRed.png'])],
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3'

)