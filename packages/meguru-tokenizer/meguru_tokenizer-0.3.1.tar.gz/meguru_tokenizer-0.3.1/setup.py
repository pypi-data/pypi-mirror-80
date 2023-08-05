#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
import os

PACKAGE = "meguru_tokenizer"
here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, PACKAGE, "__version__.py")) as f:
    exec(f.read(), about)


with open("readme.md") as readme_file:
    readme = readme_file.read()

requirements = [
    "ginza>=4.0.0",
    "sentencepiece",
    "neologdn",
    "nltk",
    "spacy>=2.2.4",
    "sudachidict-full",
    "torch",
    "tensorflow>=2.2.0",
]

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="MokkeMeguru",
    author_email="meguru.mokke@gmail.com",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="simple tokenizer for tensorflow 2.x and PyTorch",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords=["tensorflow", "pytorch", "tokenizer", "nlp"],
    name="meguru_tokenizer",
    packages=find_packages(include=["meguru_tokenizer", "meguru_tokenizer.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/MokkeMeguru/meguru_tokenizer",
    version=about["__version__"],
    zip_safe=False,
)
