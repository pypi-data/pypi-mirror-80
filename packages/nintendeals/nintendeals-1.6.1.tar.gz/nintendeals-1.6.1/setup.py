from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, "readme.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="nintendeals",
    version="1.6.1",
    url="https://github.com/fedecalendino/nintendeals",
    license="MIT",
    description="Scraping tools for Nintendo games and prices on NA, EU and JP.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Fede Calendino",
    author_email="fede@calendino.com",
    packages=[
        "nintendeals",
        "nintendeals.api",
        "nintendeals.classes",
        "nintendeals.classes.platforms",
        "nintendeals.noa",
        "nintendeals.noa.external",
        "nintendeals.noe",
        "nintendeals.noj",
    ],
    install_requires=[
        "algoliasearch",
        "beautifulsoup4",
        "pycountry",
        "python-dateutil",
        "requests",
        "xmltodict",
    ],
    keywords=[
        "nintendo",
        "eshop",
        "deals",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
