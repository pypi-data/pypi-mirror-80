##############################################################################
##              CDM Analytics Proprietary Analytics Toolset                 ##
##                    Copyright 2020 - CDM Analytics                        ##
##                           INTERNAL USE ONLY                              ##
##############################################################################
import setuptools
## Obtain Description from README.md
with open("README.md", "r") as fh:
    long_description = fh.read()
## Package Metadata
setuptools.setup(
    name="cdmanalytics",
    version="0.0.2",
    license="Proprietary",
    author="CDM Analytics",
    author_email="sales@canaryinthedatamine.com",
    description="CDM Analytics - Big Data Toolset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://cdmanalytics.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)