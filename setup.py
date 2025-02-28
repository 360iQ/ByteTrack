#!/usr/bin/env python
# Copyright (c) Megvii, Inc. and its affiliates. All Rights Reserved
import os
os.system("pip install -r requirements.txt")
import setuptools
import torch
from torch.utils.cpp_extension import CppExtension

torch_ver = [int(x) for x in torch.__version__.split(".")[:2]]
assert torch_ver >= [1, 3], "Requires PyTorch >= 1.3"


with open("README.md", "r") as f:
    long_description = f.read()


def get_install_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        reqs = [x.strip() for x in f.read().splitlines()]
    reqs = [x for x in reqs if not x.startswith("#")]
    return reqs


def get_package_dir():
    pkg_dir = {
        "bytetrack.tracker": "tracker",
    }
    return pkg_dir

setuptools.setup(
    name="bytetrack",
    version="0.1.0",
    author="basedet team",
    url="https://github.com/360iQ/ByteTrack.git",
    packages=list(get_package_dir().keys()),
    python_requires=">=3.6",
    install_requires=get_install_requirements(),
    setup_requires=["wheel"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3", "Operating System :: OS Independent"],
    cmdclass={"build_ext": torch.utils.cpp_extension.BuildExtension},
)
