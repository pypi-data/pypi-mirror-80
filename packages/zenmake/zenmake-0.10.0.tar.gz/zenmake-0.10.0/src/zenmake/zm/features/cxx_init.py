# coding=utf-8
#

"""
 Copyright (c) 2020, Alexander Magola. All rights reserved.
 license: BSD 3-Clause License, see LICENSE for more details.
"""

from zm.constants import TASK_TARGET_KINDS, TASK_FEATURE_ALIASES
from zm.buildconf.schemeutils import addSelectToParams

VALIDATION_TASKSCHEME_SPEC = {
    'cxxflags' :  { 'type': ('str', 'list-of-strs') },
}
addSelectToParams(VALIDATION_TASKSCHEME_SPEC)

TASK_FEATURES_SETUP = {
    'cxx' : {
        'target-kinds' : TASK_TARGET_KINDS,
        'aliases' : TASK_FEATURE_ALIASES,
        'file-extensions' : ('.cpp', '.CPP', '.cxx', '.CXX', '.c++', '.C++', '.cc', '.CC'),
    },
}

TOOLCHAIN_VARS = {
    # 'sysenv-var' - environment variable to set compiler
    # 'cfgenv-var' - WAF ConfigSet variable to get/set compiler
    # 'sysenv-flagvars' - env flag variables that have effect from system environment
    # 'cfgenv-flagvars' - WAF ConfigSet variables that are used on 'configure' step
    # and translated from buildconf vars
    'cxx' : {
        'sysenv-var'      : 'CXX',
        'cfgenv-var'      : 'CXX',
        'sysenv-flagvars' : ('CXXFLAGS', 'CPPFLAGS', 'LDFLAGS', 'LINKFLAGS'),
        'cfgenv-flagvars' : ('CXXFLAGS', 'CPPFLAGS', 'LDFLAGS', 'LINKFLAGS', 'DEFINES'),
    },
}
