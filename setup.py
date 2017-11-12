#!/usr/bin/env python

from setuptools import setup


setup(
    name="htmlgen",
    version="0.99.2",
    description="HTML 5 Generator",
    long_description=open("README.rst").read(),
    author="Sebastian Rittau",
    author_email="srittau@rittau.biz",
    url="https://github.com/srittau/python-htmlgen",
    packages=["htmlgen", "test_htmlgen"],
    package_data={"htmlgen": ["*.pyi"]},
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    tests_require=["asserts >= 0.8.0, < 0.9", "typing"],
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
)
