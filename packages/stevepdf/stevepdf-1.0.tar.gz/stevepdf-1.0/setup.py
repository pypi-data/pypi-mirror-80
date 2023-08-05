import setuptools
from pathlib import Path

setuptools.setup(
    name="stevepdf",
    version=1.0,
    long_descripyion=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])

)
