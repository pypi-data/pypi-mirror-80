import setuptools
from pathlib import Path

setuptools.setup(
    name="sadrapdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"]) # in the paranthises we exclude files: here we excluded data and tests.
)