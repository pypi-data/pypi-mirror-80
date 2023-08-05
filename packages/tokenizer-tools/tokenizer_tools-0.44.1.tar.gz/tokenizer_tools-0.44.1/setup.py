#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

# without tensorflow by default
install_requires = [
    "Click>=6.0",
    "scikit-learn",
    "scipy",
    "pandas",
    "fuzzywuzzy",
    "plotly",
    "mistletoe",
    "tqdm"
]


setup_requirements = ["pytest-runner"]

test_requirements = ["pytest", "pytest-helpers-namespace"]

setup(
    author="Xiaoquan Kong",
    author_email="u1mail2me@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Tools for tokenizer develope and evaluation",
    entry_points={"console_scripts": ["tokenizer_tools=tokenizer_tools.cli:main"]},
    install_requires=install_requires,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="tokenizer_tools",
    name="tokenizer_tools",
    packages=find_packages(include=["tokenizer_tools", "tokenizer_tools.*"]),
    setup_requires=setup_requirements,
    extra_require={"tensorflow": "tensorflow>1.15,<2.0"},
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/howlandersonn/tokenizer_tools",
    version="0.44.1",
    zip_safe=False,
)
