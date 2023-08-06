import setuptools
import re

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="credit_card_checker",
    version="0.0.3",
    author="Jianfang Bladen-Hovell",
    author_email="bladenhovell@gmail.com",
    description="Use the Luhn algorithm to check if credit card numbers are valid",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/credit_card_checker",
    packages=setuptools.find_packages(),
    py_modules=['credit_card_checker'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
