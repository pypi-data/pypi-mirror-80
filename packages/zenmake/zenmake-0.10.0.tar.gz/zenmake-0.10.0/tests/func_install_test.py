# coding=utf-8
#

# pylint: disable = wildcard-import, unused-wildcard-import
# pylint: disable = missing-docstring, invalid-name, bad-continuation
# pylint: disable = unused-argument, no-member, attribute-defined-outside-init
# pylint: disable = too-many-lines, too-many-branches, too-many-statements

"""
 Copyright (c) 2020, Alexander Magola. All rights reserved.
 license: BSD 3-Clause License, see LICENSE for more details.
"""

import os
import posixpath

import pytest
from zm import cli, utils
from zm.pyutils import viewitems
from zm.autodict import AutoDict
from zm.constants import PLATFORM
from zm.features import TASK_TARGET_FEATURES

from tests.func_utils import *

FORINSTALL_PRJDIRS = [
    joinpath('cpp', '09-complex-unittest'),
    joinpath('subdirs', '2-complex'),
]

def getInstallFixtureParams():

    fixtures = []

    #### 1
    prefix = cli.DEFAULT_PREFIX
    bindir = joinpath(prefix, 'bin')
    libdir = joinpath(prefix, 'lib%s' % utils.libDirPostfix())

    params = AutoDict(prefix = prefix, bindir = bindir, libdir = libdir)
    params.installArgs = []

    fixtures.append(AutoDict(id = len(fixtures) + 1, **params))

    #### 2
    prefix = '/usr/my'
    bindir = posixpath.join(prefix, 'bin')
    libdir = posixpath.join(prefix, 'lib%s' % utils.libDirPostfix())

    params = AutoDict(prefix = prefix, bindir = bindir, libdir = libdir)
    params.installArgs = ['--prefix', params.prefix]

    fixtures.append(AutoDict(id = len(fixtures) + 1, **params))

    #### 3
    params = AutoDict(
        prefix = '/usr/my',
        bindir = '/bb',
        libdir = '/ll',
    )

    params.installArgs = [
        '--prefix', params.prefix,
        '--bindir', params.bindir,
        '--libdir', params.libdir
    ]

    fixtures.append(AutoDict(id = len(fixtures) + 1, **params))

    for item in fixtures:
        item['id'] = str(item['id'])
    return fixtures

INSTALL_FIXTURE_PARAMS = getInstallFixtureParams()

@pytest.mark.usefixtures("unsetEnviron")
class TestInstall(object):

    @pytest.fixture(params = getZmExecutables())
    def allZmExe(self, request):
        self.zmExe = zmExes[request.param]

    @pytest.fixture(params = FORINSTALL_PRJDIRS)
    def project(self, request, tmpdir):

        def teardown():
            printErrorOnFailed(self, request)

        request.addfinalizer(teardown)
        setupTest(self, request, tmpdir)

    def _checkInstallResults(self, cmdLine, check):

        env = ConfigSet()
        env.PREFIX = check.prefix
        env.BINDIR = check.bindir
        env.LIBDIR = check.libdir

        assert isdir(check.destdir)

        isWindows = PLATFORM == 'windows'

        targets = set()
        processConfManagerWithCLI(self, cmdLine)
        tasks = getBuildTasks(self.confManager)
        for taskName, taskParams in viewitems(tasks):

            handleTaskFeatures(self, taskParams)
            features = taskParams['features']

            if 'test' in taskParams['features']:
                # ignore tests
                continue

            if not [ x for x in features if x in TASK_TARGET_FEATURES ]:
                # check only with features from TASK_TARGET_FEATURES
                continue

            taskEnv = getTaskEnv(self, taskName)
            fpattern, targetKind = getTargetPattern(taskEnv, features)

            if targetKind == 'stlib':
                # static libs aren't installed
                continue

            isExe = targetKind == 'exe'
            target = taskParams.get('target', taskName)

            if 'install-path' not in taskParams:
                targetdir = check.bindir if isExe else check.libdir
            else:
                installPath = taskParams.get('install-path', '')
                if not installPath:
                    continue

                env = env.derive()
                env.update(taskParams.get('substvars', {}))
                installPath = os.path.normpath(utils.substVars(installPath, env))
                targetdir = installPath

            if check.destdir:
                targetdir = joinpath(check.destdir,
                                      os.path.splitdrive(targetdir)[1].lstrip(os.sep))

            targetpath = joinpath(targetdir, fpattern % target)
            targets.add(targetpath)

            if targetKind == 'exe':
                assert os.access(targetpath, os.X_OK)

            if targetKind == 'shlib':
                verNum = taskParams.get('ver-num', None)
                if verNum:
                    nums = verNum.split('.')
                    if targetpath.endswith('.dylib'):
                        fname = fpattern % (target + '.' + nums[0])
                        targets.add(joinpath(targetdir, fname))
                        fname = fpattern % (target + '.' + verNum)
                        targets.add(joinpath(targetdir, fname))
                    else:
                        targets.add(targetpath + '.' + nums[0])
                        targets.add(targetpath + '.' + verNum)

                    if taskEnv.DEST_BINFMT == 'pe':
                        fname = fpattern % (target + '-' + nums[0])
                        targets.add(joinpath(targetdir, fname))

                if isWindows:
                    targetpath = joinpath(targetdir, '%s.lib' % target)
                    assert isfile(targetpath)
                    targets.add(targetpath)

        for root, _, files in os.walk(check.destdir):
            for name in files:
                path = joinpath(root, name)
                assert path in targets

    @pytest.fixture(params = INSTALL_FIXTURE_PARAMS, ids = lambda x: x['id'])
    def installFextures(self, request, tmpdir):

        fixtures = request.param.copy()
        testdir = str(tmpdir.realpath())
        fixtures['destdir'] = joinpath(testdir, 'inst')

        return fixtures

    def test(self, allZmExe, project, installFextures):

        destdir = installFextures.destdir

        cmdLine = ['install', '--destdir', destdir]
        cmdLine.extend(installFextures.installArgs)
        exitcode, _, _ = runZm(self, cmdLine)
        assert exitcode == 0

        check = installFextures.copy()
        for name in ('prefix', 'bindir', 'libdir'):
            check[name] = check[name].replace('/', os.sep)

        self._checkInstallResults(cmdLine, check)

        cmdLine[0] = 'uninstall'
        exitcode, _, _ = runZm(self, cmdLine)
        assert exitcode == 0
        assert not os.path.exists(destdir)

#############################################################################
#############################################################################

FORINSTALLFILES_PRJDIRS = [
    joinpath('mixed', '01-cshlib-cxxprogram'),
]

@pytest.mark.usefixtures("unsetEnviron")
class TestInstallFiles(object):

    @pytest.fixture(params = getZmExecutables())
    def allZmExe(self, request):
        self.zmExe = zmExes[request.param]

    @pytest.fixture(params = FORINSTALLFILES_PRJDIRS)
    def project(self, request, tmpdir):

        def teardown():
            printErrorOnFailed(self, request)

        request.addfinalizer(teardown)
        setupTest(self, request, tmpdir)

    @pytest.fixture(params = INSTALL_FIXTURE_PARAMS, ids = lambda x: x['id'])
    def installFextures(self, request, tmpdir):

        fixtures = request.param.copy()
        testdir = str(tmpdir.realpath())
        fixtures['destdir'] = joinpath(testdir, 'inst')

        prefix = fixtures['prefix'].replace('/', os.sep)
        prefix2 = os.path.splitdrive(prefix)[1].lstrip(os.sep)
        prjName = self.outputPrjDirName

        if self.testDirPath == FORINSTALLFILES_PRJDIRS[0]:

            dir1 = '%s/share/%s/scripts' % (prefix2, prjName)
            dir2 = '%s/share/%s/scripts' % (prefix, prjName)
            files = [
                { 'path' : dir1 + '/my-script.py', 'chmod' : 0o755, },
                { 'path' : dir1 + '/test.py', 'chmod' : 0o755, },
                { 'path' : dir1 + '/asd/test2.py', 'chmod' : 0o755, },
                #{ 'path' : dir1 + '/my-script.link.py', 'chmod' : 0o755, },
                { 'path' : dir1 + '2/my-script.py', 'chmod' : 0o755, },
                { 'path' : dir1 + '2/test.py', 'chmod' : 0o755, },
                { 'path' : dir1 + '3/my-script.py', 'chmod' : 0o644, },
                { 'path' : dir1 + '3/test.py', 'chmod' : 0o644, },
                { 'path' : dir1 + '3/test2.py', 'chmod' : 0o644, },
                { 'path' : dir1 + '/mtest.py', 'chmod' : 0o750 },
            ]

            if PLATFORM == 'linux':
                files.extend([
                    { 'path' : dir1 + '/mtest-link.py', 'linkto' : dir2 + '/mtest.py' },
                ])

            if PLATFORM != 'windows':
                files.extend([
                    { 'path' : dir1 + '/my-script.link.py', 'chmod' : 0o755, },
                ])
                files.extend([
                    { 'path' : dir1 + '2/my-script.link.py', 'linkto' : './my-script.py' },
                ])
        else:
            # unknown project, forgot to add ?
            assert False

        for item in files:
            item['path'] = item['path'].replace('/', os.sep)

        fixtures['files'] = files
        return fixtures

    def test(self, allZmExe, project, installFextures):

        destdir = installFextures.destdir

        cmdLine = ['install', '--destdir', destdir]
        cmdLine.extend(installFextures.installArgs)
        exitcode, _, _ = runZm(self, cmdLine)
        assert exitcode == 0

        for item in installFextures['files']:
            filepath = joinpath(destdir, item['path'])
            if 'linkto' in item:
                linkto = item['linkto']
                assert islink(filepath)
                assert linkto == os.readlink(filepath)
            else:
                assert isfile(filepath)
                if PLATFORM != 'windows':
                    chmodExpected = oct(item.get('chmod', 0o644))[-3:]
                    chmodReal = oct(os.stat(filepath).st_mode)[-3:]
                    assert chmodReal == chmodExpected

        cmdLine[0] = 'uninstall'
        exitcode, _, _ = runZm(self, cmdLine)
        assert exitcode == 0
        assert not os.path.exists(destdir)
