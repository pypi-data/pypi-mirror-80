#!/usr/bin/python3
import setuptools
import physicslib

setuptools.setup(
    name="physicslib",
    version=physicslib.__version__,
    packages=setuptools.find_packages(),
    author="NamorNiradnug",
    author_email="roma937a@mail.ru",
    description="Physics objects and constants.",
    license="MIT",
)
