.. include:: global.rst.inc
.. _introduction:

Introduction
============

What is it?
-----------

ZenMake is a build system based on the meta build system/framework Waf_.
The main purpose of ZenMake is to be as simple to use as possible
but remain flexible.

Some reasons to create this project can be found :ref:`here<why>`.

It uses declarative configuration files with ability to use the real 
programming language (python).

Main features
-------------
    - Easy to use and flexible build config as python (.py) or as yaml file.
      Details are :ref:`here<buildconf>`.
    - Distribution as zip application or as system package (pip).
      See :ref:`Installation<installation>`.
    - Automatic build order and dependencies.
    - Automatic reconfiguring: no need to run command 'configure'.
    - Compiler autodetection.
    - Building and running functional/unit tests including an ability to
      build and run tests only on changes. Details are :ref:`here<buildtests>`.
    - Running custom scripts during a build phase.
    - Build configs in sub directories.
    - Building external dependencies.
    - Supported platforms: GNU/Linux, MacOS, MS Windows. Some other
      platforms like OpenBSD/FreeBSD should work as well but it
      hasn't been tested.
    - Supported languages:

      - C: gcc, clang, msvc, icc, xlc, suncc, irixcc
      - C++: g++, clang++, msvc, icpc, xlc++, sunc++
      - D: dmd, ldc2, gdc (MS Windows is not supported yet)
      - Fortran: gfortran, ifort
      - Assembler: gas (GNU Assembler), nasm/yasm (experimental)

Plans to do
------------

There is no clear roadmap for this project. I add features that I think are
needed to include.

Project links
-------------

.. include:: projectlinks.rst
