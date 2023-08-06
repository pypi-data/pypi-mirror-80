import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="yfoptions_dl",
    version="1.0.0",
    description="Download option chain data from Yahoo Finance",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jingzact/yfoptions_dl",
    author="Jay",
    author_email="pythoninoffice@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["yfoptions_dl"],
    include_package_data=True,
    install_requires=["pandas >= 1.0.0",
                      "requests > 2.23.0"
                      ],
)
