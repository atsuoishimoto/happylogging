import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="happylogging",
    version="0.0.2",
    author="Atsuo Ishimoto",
    description="Utility functions to help using standard logging module.",
    license="MIT",
    keywords="logging",
    url="https://github.com/atsuoishimoto/happylogging",
    long_description=read('README.rst'),
    classifiers=[
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=['happylogging'],
)
