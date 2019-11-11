#!/usr/bin/env python

from setuptools import setup


setup(
    name="htmlgen",
    version="2.0.0",
    description="HTML 5 Generator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sebastian Rittau",
    author_email="srittau@rittau.biz",
    url="https://github.com/srittau/python-htmlgen",
    packages=["htmlgen", "test_htmlgen"],
    package_data={"htmlgen": ["*.pyi", "py.typed"]},
    python_requires=">=3.5",
    tests_require=["asserts >= 0.8.0, < 0.11"],
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
)
