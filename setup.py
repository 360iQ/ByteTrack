#!/usr/bin/env python
# Copyright (c) Megvii, Inc. and its affiliates. All Rights Reserved
import os
os.system("pip install -r requirements.txt")
import re
import setuptools
import glob
from os import path
import torch
from torch.utils.cpp_extension import CppExtension

torch_ver = [int(x) for x in torch.__version__.split(".")[:2]]
assert torch_ver >= [1, 3], "Requires PyTorch >= 1.3"


def get_extensions():
    this_dir = path.dirname(path.abspath(__file__))
    extensions_dir = path.join(this_dir, "yolox", "layers", "csrc")

    main_source = path.join(extensions_dir, "vision.cpp")
    sources = glob.glob(path.join(extensions_dir, "**", "*.cpp"))

    sources = [main_source] + sources
    extension = CppExtension

    extra_compile_args = {"cxx": ["-O3"]}
    define_macros = []

    include_dirs = [extensions_dir]

    ext_modules = [
        extension(
            "yolox._C",
            sources,
            include_dirs=include_dirs,
            define_macros=define_macros,
            extra_compile_args=extra_compile_args,
        )
    ]

    return ext_modules


with open("yolox/__init__.py", "r") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        f.read(), re.MULTILINE
    ).group(1)


with open("README.md", "r") as f:
    long_description = f.read()


def get_install_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        reqs = [x.strip() for x in f.read().splitlines()]
    reqs = [x for x in reqs if not x.startswith("#")]
    return reqs


setuptools.setup(
    name="bytetrack",
    version="0.1.0",
    author="basedet team",
    url="https://github.com/360iQ/ByteTrack.git",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=get_install_requirements(),
    setup_requires=["wheel"],  # avoid building error when pip is not updated
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,  # include files in MANIFEST.in
    ext_modules=get_extensions(),
    classifiers=["Programming Language :: Python :: 3", "Operating System :: OS Independent"],
    cmdclass={"build_ext": torch.utils.cpp_extension.BuildExtension},
    # packages=setuptools.find_namespace_packages(),
)
