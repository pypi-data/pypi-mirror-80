"Django Loves Sandstorm"
from setuptools import find_packages
from setuptools import setup

with open("README.rst", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="djangolovessandstorm",
    version="0.0.4",
    description="Django-Sandstorm integration",
    long_description=long_description,
    author="Troy J. Farrell",
    author_email="troy@entheossoft.com",
    url="http://www.tjf.us/en/code/python/djangolovessandstorm",
    license="BSD-3-Clause",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django :: 2.2",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
    ],
    packages=find_packages(),
)
