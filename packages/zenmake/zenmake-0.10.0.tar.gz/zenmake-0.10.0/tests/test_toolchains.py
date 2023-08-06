# coding=utf-8
#

# _pylint: skip-file
# pylint: disable = missing-docstring, invalid-name, bad-continuation

"""
 Copyright (c) 2019, Alexander Magola. All rights reserved.
 license: BSD 3-Clause License, see LICENSE for more details.
"""

import itertools
import pytest
from zm.error import ZenMakeError
from zm import toolchains
# pylint: disable = unused-import
from zm.features import c, cxx, asm
# pylint: enable = unused-import

COMPILERS_MAP = {
    'c'   : {
        'windows': ['msvc', 'gcc', 'clang'],
        'darwin':  ['clang', 'gcc'],
        'linux':   ['gcc', 'clang', 'icc'],
        'default': ['clang', 'gcc'],
    },
    'cxx' : {
        'windows': ['msvc', 'g++', 'clang++'],
        'darwin':  ['clang++', 'g++'],
        'linux':   ['g++', 'clang++', 'icpc'],
        'default': ['clang++', 'g++'],
    },
    'asm' : {
        'default':['gas', 'nasm'],
    },
}

SUPPORTED_LANGS = COMPILERS_MAP.keys()

def testGetNames():

    for lang in SUPPORTED_LANGS:
        langCompiler = COMPILERS_MAP[lang]

        for _platform in ('linux', 'windows', 'darwin'):
            compilers = toolchains.getNames(lang, _platform)
            # to force covering of cache
            _compilers = toolchains.getNames(lang, _platform)
            assert _compilers == compilers

            expected = langCompiler.get(_platform, langCompiler['default'])
            assert set(compilers) == set(expected)

        compilers = toolchains.getNames(lang, 'all')
        # to force covering of cache
        _compilers = toolchains.getNames(lang, 'all')
        assert _compilers == compilers
        assert set(compilers) >= \
                        set(itertools.chain(*langCompiler.values()))

    with pytest.raises(ZenMakeError):
        toolchains.getNames('')
    with pytest.raises(ZenMakeError):
        toolchains.getNames('invalid lang')

def testGetAllNames():

    for platform in ('linux', 'windows', 'darwin', 'all'):
        expectedCompilers = []
        for lang in SUPPORTED_LANGS:
            expectedCompilers.extend(toolchains.getNames(lang, platform))
        expectedCompilers = list(set(expectedCompilers))
        assert sorted(toolchains.getAllNames(platform)) == \
                                        sorted(expectedCompilers)
