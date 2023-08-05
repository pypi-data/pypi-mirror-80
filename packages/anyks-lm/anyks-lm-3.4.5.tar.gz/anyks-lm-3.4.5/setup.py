#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import os
import pybind11
import setuptools
from distutils.core import setup, Extension

with open("README.md", "r") as fh:
    description = fh.read()

root_dir = './alm_pkg'

include_files = [
    '%s/alm/include/idw.hpp' % root_dir,
    '%s/alm/include/env.hpp' % root_dir,
    '%s/alm/include/alm.hpp' % root_dir,
    '%s/alm/include/nwt.hpp' % root_dir,
    '%s/alm/include/word.hpp' % root_dir,
    '%s/alm/include/fsys.hpp' % root_dir,
    '%s/alm/include/aspl.hpp' % root_dir,
    '%s/alm/include/ablm.hpp' % root_dir,
    '%s/alm/include/arpa.hpp' % root_dir,
    '%s/alm/include/python.hpp' % root_dir,
    '%s/alm/include/toolkit.hpp' % root_dir,
    '%s/alm/include/alphabet.hpp' % root_dir,
    '%s/alm/include/progress.hpp' % root_dir,
    '%s/alm/include/tokenizer.hpp' % root_dir,
    '%s/alm/include/collector.hpp' % root_dir,
    '%s/alm/include/threadpool.hpp' % root_dir,
    '%s/alm/include/levenshtein.hpp' % root_dir
]

include_cityhash = [
    '%s/alm/contrib/include/cityhash/city.h' % root_dir,
    '%s/alm/contrib/include/cityhash/config.h' % root_dir,
    '%s/alm/contrib/include/cityhash/citycrc.h' % root_dir
]

include_bigint = [
    '%s/alm/contrib/include/bigint/BigInteger.hh' % root_dir,
    '%s/alm/contrib/include/bigint/BigUnsigned.hh' % root_dir,
    '%s/alm/contrib/include/bigint/NumberlikeArray.hh' % root_dir,
    '%s/alm/contrib/include/bigint/BigIntegerUtils.hh' % root_dir,
    '%s/alm/contrib/include/bigint/BigIntegerLibrary.hh' % root_dir,
    '%s/alm/contrib/include/bigint/BigUnsignedInABase.hh' % root_dir,
    '%s/alm/contrib/include/bigint/BigIntegerAlgorithms.hh' % root_dir
]

src_files = [
    '%s/alm/src/idw.cpp' % root_dir,
    '%s/alm/src/nwt.cpp' % root_dir,
    '%s/alm/src/arpa.cpp' % root_dir,
    '%s/alm/src/python.cpp' % root_dir,
    '%s/alm/src/progress.cpp' % root_dir,
    '%s/alm/src/alphabet.cpp' % root_dir,
    '%s/alm/src/collector.cpp' % root_dir,
    '%s/alm/src/alm.cpp' % root_dir,
    '%s/alm/src/alm1.cpp' % root_dir,
    '%s/alm/src/alm2.cpp' % root_dir,
    '%s/alm/src/tokenizer.cpp' % root_dir,
    '%s/alm/src/toolkit.cpp' % root_dir,
    '%s/alm/src/levenshtein.cpp' % root_dir,
    '%s/alm/src/ablm.cpp' % root_dir,
    '%s/alm/contrib/src/cityhash/city.cc' % root_dir,
    '%s/alm/contrib/src/bigint/BigInteger.cc' % root_dir,
    '%s/alm/contrib/src/bigint/BigUnsigned.cc' % root_dir,
    '%s/alm/contrib/src/bigint/BigIntegerUtils.cc' % root_dir,
    '%s/alm/contrib/src/bigint/BigUnsignedInABase.cc' % root_dir,
    '%s/alm/contrib/src/bigint/BigIntegerAlgorithms.cc' % root_dir,
    '%s/palm.cxx' % root_dir
]

pakage_files = [
    ('include/alm', include_files),
    ('include/bigint', include_bigint),
    ('include/cityhash', include_cityhash),
    ('include/alm/app', ['%s/alm/app/alm.hpp' % root_dir]),
    ('include/nlohmann', ['%s/alm/contrib/include/nlohmann/json.hpp' % root_dir])
]

ext_modules = [
    Extension(
        'alm', src_files,
        include_dirs = [
            root_dir,
            '%s/alm' % root_dir,
            '%s/alm/include' % root_dir,
            '%s/alm/contrib/include' % root_dir,
            pybind11.get_include()
        ],
        language = 'c++',
        # library_dirs = [''],
        libraries = ['m', 'z', 'ssl', 'stdc++', 'crypto', 'pthread'],
        extra_compile_args = ['-std=c++11', '-O2', '-fno-permissive', '-Wno-pedantic', '-Wno-unknown-attributes', '-DNOPYTHON']
    )
]

setuptools.setup(
    name = "anyks-lm",
#    name = "test-alm",
    version = "3.4.5",
    author = "Yuriy Lobarev",
    author_email = "forman@anyks.com",
    description = "Smart language model",
    long_description = description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/anyks/alm",
    download_url = 'https://github.com/anyks/alm/archive/release.tar.gz',
    ext_modules = ext_modules,
    packages = setuptools.find_packages(),
    data_files = pakage_files,
    keywords = ['nlp', 'lm', 'alm', 'language-model'],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: POSIX :: BSD :: FreeBSD"
    ],
    requires = ['pybind11'],
    python_requires = '>=3.6',
    include_package_data = True
)
