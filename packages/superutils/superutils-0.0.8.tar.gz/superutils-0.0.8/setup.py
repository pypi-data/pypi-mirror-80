#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com

import setuptools


with open("superutils/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
name="superutils",
        version="0.0.8",
        author="Frank YCJ",
        author_email="1320259466@qq.com",
        description="The super superutils makes the code simpler!",
        keywords='tool util code simpler box email json security',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/YouAreOnlyOne",
        # packages=setuptools.find_packages(),
        packages=["superutils"],
        install_requires=['Pillow>6.0'],
        python_requires=">=2.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
        license="Apache 2.0 license",
        Platform="OS All, Python 2.x",

        project_urls={
        "Bug Tracker": "https://github.com/YouAreOnlyOne/FastFrameJar/issues",
        "Documentation": "https://github.com/YouAreOnlyOne/FastFrameJar",
        "Source Code": "https://github.com/YouAreOnlyOne/FastFrameJar",
    },

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "superutils": ["README"],
        "superutils": ["README.md"],
        "": ["README.md"],
        "superutils": ["*.md"],
        # "superutils": ["*.docx"],
        "superutils": ["LICENSE"],
    },
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
