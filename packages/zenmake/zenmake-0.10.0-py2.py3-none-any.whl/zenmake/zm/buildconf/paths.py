# coding=utf-8
#

"""
 Copyright (c) 2019, Alexander Magola. All rights reserved.
 license: BSD 3-Clause License, see LICENSE for more details.
"""

import os

from zm.pyutils import PY2
from zm.error import ZenMakeConfValueError
from zm.constants import WAF_CACHE_DIRNAME, WAF_CACHE_NAMESUFFIX, \
                         ZENMAKE_BUILDMETA_FILENAME, BUILDOUTNAME

joinpath = os.path.join

class ConfPaths(object):
    """
    Class to calculate different paths depending on buildconf
    """

    # pylint: disable=too-many-instance-attributes

    __slots__ = (
        'buildconffile', 'buildconfdir', 'buildroot', 'realbuildroot',
        'rootdir', 'startdir', 'buildout', 'wscripttop', 'wscriptout',
        'wafcachedir', 'wafcachefile', 'zmcachedir', 'zmmetafile',
    )

    def __init__(self, bconf):
        """
        bconf - object of buildconf.Config
        """

        #pylint: disable=protected-access
        buildconf = bconf._conf
        #pylint: enable=protected-access

        # See buildconf.Config
        self.buildconffile = bconf.path
        self.buildconfdir  = bconf.confdir
        self.rootdir       = bconf.rootdir
        self.startdir      = buildconf.startdir
        self.buildroot     = buildconf.buildroot
        self.realbuildroot = buildconf.realbuildroot

        # other attributes
        self.buildout = joinpath(self.buildroot, BUILDOUTNAME)

        #self.wscripttop    = self.buildconfdir
        self.wscripttop    = self.startdir

        self.wscriptout    = self.buildout
        self.wafcachedir   = joinpath(self.buildout, WAF_CACHE_DIRNAME)
        self.wafcachefile  = joinpath(self.wafcachedir, WAF_CACHE_NAMESUFFIX)
        self.zmcachedir    = self.wafcachedir
        self.zmmetafile    = joinpath(self.buildroot, ZENMAKE_BUILDMETA_FILENAME)

        self._checkBuildRoot('buildroot', 'startdir')
        self._checkBuildRoot('buildroot', 'buildconfdir')

        if self.realbuildroot != self.buildroot:
            self._checkBuildRoot('realbuildroot', 'startdir')
            self._checkBuildRoot('realbuildroot', 'buildconfdir')

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        for name in self.__slots__:
            if getattr(self, name, None) != getattr(other, name, None):
                return False
        return True

    if PY2: # python 3 has it by default and it's more performant
        def __ne__(self, other):
            return not self == other

    def _checkBuildRoot(self, buildrootName, checkingName):
        buildrootVal = getattr(self, buildrootName)
        checkingVal = getattr(self, checkingName)

        if checkingName == 'buildconfdir':
            checkingName = 'directory with buildconf file'
        else:
            checkingName = "%r" % checkingName

        if buildrootVal == checkingVal:
            msg = "Parameter %r cannot be the same as the %s" % (buildrootName, checkingName)
            raise ZenMakeConfValueError(msg, confpath = self.buildconffile)

        if checkingVal.startswith(buildrootVal):
            msg = "Parameter %r cannot be parent directory of the %s" % \
                   (buildrootName, checkingName)
            raise ZenMakeConfValueError(msg, confpath = self.buildconffile)
