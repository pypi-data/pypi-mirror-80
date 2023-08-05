import setuptools
from pathlib import Path

setuptools.setup(name="harvey_logger",
                 version="1.41",
                 long_description=Path("README.md").read_text(),
                 packages=setuptools.find_packages(),
                 license="MIT")
