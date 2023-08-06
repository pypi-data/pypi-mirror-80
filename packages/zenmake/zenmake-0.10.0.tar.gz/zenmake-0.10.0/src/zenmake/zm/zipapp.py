# coding=utf-8
#

"""
 Copyright (c) 2019, Alexander Magola. All rights reserved.
 license: BSD 3-Clause License, see LICENSE for more details.
"""

import sys
import os
import io
import shutil
import tempfile
import atexit

from zm.constants import PLATFORM, APPNAME
from zm.pyutils import stringtype
from zm import log, error, cmd
from zm import ZENMAKE_DIR
from zm.pypkg import ZipPkg

ZIPAPP_NAME = APPNAME + '.pyz'
if PLATFORM == 'windows':
    SHEBANG_ENC = 'utf-8'
else:
    SHEBANG_ENC = sys.getfilesystemencoding()

IGNORE_EXTS = frozenset(('.pyc', '.PYC', '.pyo', '.PYO' ))
IGNORE_FILE_PATHS = (
    {
        'dir' : os.path.join('waf', 'waflib', 'Tools'),
        'files' : frozenset(('lua.py', 'waf_unit_test.py'))
    },
    {
        'dir' : os.path.join('waf', 'waflib', 'extras'),
        'dont-ignore' : frozenset((
            'erlang.py', 'c_bgxlc.py', 'c_emscripten.py', 'c_nec.py',
            'fc_bgxlf.py', 'fc_cray.py', 'fc_nag.py', 'fc_nec.py',
            'fc_nfort.py', 'fc_open64.py', 'fc_pgfortran.py', 'fc_solstudio.py',
            'fc_xlf.py', 'protoc.py', 'pyqt5.py',
        ))
    },
)

# copied from shutil.py
def _samefile(src, dst):
    # Macintosh, Unix.
    if hasattr(os.path, 'samefile'):
        try:
            return os.path.samefile(src, dst)
        except OSError:
            return False

    # All other platforms: check for same pathname.
    return (os.path.normcase(os.path.abspath(src)) ==
            os.path.normcase(os.path.abspath(dst)))

def make(destDir, verbose = 0):
    """
    Make an executable zip file of project
    """

    zipAppFileName = os.path.join(destDir, ZIPAPP_NAME)
    zipPkg = ZipPkg(__name__)
    if zipPkg.zipexists:
        src, dst = zipPkg.zippath, zipAppFileName
        if _samefile(src, dst):
            msg = "{!r} and {!r} are the same file".format(src, dst)
            raise error.ZenMakeError(msg)

        # We already have a zip file so just copy it into dest dir
        return shutil.copy(src, dst)

    tempDir = None

    def clearTmp():
        if tempDir and os.path.isdir(tempDir):
            shutil.rmtree(tempDir, ignore_errors = True)
    atexit.register(clearTmp)

    tempDir = tempfile.mkdtemp(prefix = APPNAME + '.')
    tempDest = os.path.join(tempDir, APPNAME)

    def copytreeIgnore(src, names):
        if not isinstance(src, stringtype):
            # Since python 3.8 the src is the os.DirEntry object
            src = src.name

        _names = []
        for item in IGNORE_FILE_PATHS:
            if not src.endswith(item['dir']):
                continue
            _names = set(names)
            files = item.get('files', frozenset())
            dontIgnore = item.get('dont-ignore', frozenset())

            _names = _names & files if files else _names
            _names = list(_names - dontIgnore)
            break

        _names += [x for x in names if os.path.splitext(x)[1] in IGNORE_EXTS]
        return _names

    shutil.copytree(ZENMAKE_DIR, tempDest, ignore = copytreeIgnore)

    logger = log if verbose >= 1 else None
    zipFullBaseName = os.path.join(tempDir, APPNAME)
    zipFile = shutil.make_archive(zipFullBaseName, 'zip', tempDest, logger = logger)

    interpreter = '/usr/bin/env python'
    interpreter = interpreter.encode(SHEBANG_ENC)
    # Python 'zipapp' exists only in python >= 3.5 but it's not a big problem
    with io.open(zipAppFileName, 'wb') as appFile:
        shebang = b'#!' + interpreter + b'\n'
        appFile.write(shebang)
        with io.open(zipFile, 'rb') as zipFile:
            shutil.copyfileobj(zipFile, appFile)

    os.chmod(zipAppFileName, 0o755)
    return zipAppFileName

class Command(cmd.Command):
    """
    Command for making an executable zip file of project.
    It's implementation of command 'zipapp'.
    """

    COLOR = 'GREEN'

    def _run(self, cliArgs):

        destDir = os.path.abspath(cliArgs.destdir)
        zipAppFileName = os.path.join(destDir, ZIPAPP_NAME)

        self._info('Making of the executable zip file %r' % zipAppFileName)

        if PLATFORM == 'windows':
            msg = "On Windows it may need to have special launcher installed"
            msg += " to run .pyz file or use it like this: python zenmake.pyz"
            msg += "\nBut when it was being tested on Windows 10 it worked fine as is."
            self._warn(msg)

        make(destDir, cliArgs.verbose)

        self._info("'zipapp' finished successfully")
        return 0
