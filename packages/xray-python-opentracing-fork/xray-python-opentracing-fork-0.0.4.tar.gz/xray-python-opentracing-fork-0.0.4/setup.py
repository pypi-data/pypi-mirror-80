#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="xray-python-opentracing-fork",
    version="0.0.4",
    description="AWS X-Ray Python OpenTracing Implementation",
    long_description="",
    author="Jeremy Apthorp <nornagon@nornagon.net>",
    maintainer="KOCAK Mikail <hello@vanille.bid>",
    license="",
    install_requires=["basictracer>=3.1,<4.0", "opentracing>=2.3.0"],
    tests_require=["pytest"],
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords=[
        "opentracing",
        "aws",
        "xray",
        "awsxray",
        "traceguide",
        "tracing",
        "microservices",
        "distributed",
    ],
    packages=find_packages(exclude=["docs*", "tests*", "sample*"]),
)
