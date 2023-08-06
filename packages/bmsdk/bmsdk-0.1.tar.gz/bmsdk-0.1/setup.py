#-------------------------------------------------------------------------
# Copyright (c) Boreus GmbH 
# All rights reserved.
#-------------------------------------------------------------------------

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bmsdk",
    version="0.1",
    author="Boreus GmbH",
    author_email="python@bigmodo.de",
    description="This package name is reserved by Boreus GmbH",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.boreus.de",
    packages=[],
)
