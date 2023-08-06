.. include:: global.rst.inc
.. highlight:: none
.. _why:

Why?
============

https://news.ycombinator.com/item?id=18789162

::

    Cool. One more "new" build system...

Yes, I know, we already have a lot of them. I decided to create this project
because I couldn’t find a build tool for Linux which is quick and easy to use,
flexible, ready to use, with declarative configuration, without the need to learn one more
special language and suitable for my needs.
I know about lots of build systems and I have tried some of them.
Eventually, I concluded that I had to try to make my own build tool.
Actually I began this project in `2013 <https://bitbucket.org/pustotnik/zenmake.old/src/master/>`_
year but I had no time to develop it at that time.
I would do it mostly for myself, but I would be glad if my tool was useful
for others.

The main purpose of ZenMake is to be as simple to use as possible
but remain flexible. It uses declarative configuration files and should provide
good performance.

Below I describe what is wrong with some of existing popular build systems in my
opinion. I considered only opensource cross-platform build systems that can
build C/C++ projects on GNU/Linux.
Remember it's only my opinion and it doesn't mean that other build systems are bad.
And it's not complete technical comparation.

**CMake**

It's one of the most popular cross-platform build systems nowadays as I know.
But I have never liked its internal language - for me it's not very convenient.
And CMake is too complicated.
As far as I know, a lot of people think
the same but they choose to use it because it's popular and with good support
for many platforms.

**Make**

It's a very old but still relevant build system. However, it has too many
disadvantages and it has been mostly replaced by more recent build systems in many projects.
But it is used as a backend in some other build systems,
for example, by CMake.

**Waf**

Waf is a great build system and has a lot of capabilities. I like it
and have some experience with it but for me it's a meta build system. You
can build your projects only by Waf but it has a long learning curve and
is not easy to use.

**ninja**

Well, I don't know a lot about this system. I know that it is used as
a backend in Meson and CMake. But "it is designed to have its input files generated
by a higher-level build system" and "Ninja build files are not meant to be written by hand".
So this build system is not for direct using.

**Meson**

It's really not a bad build system which uses ninja as a backend to build by default.
I have tried to use it but didn't like some of its features:

-  It tries to be smart when it's not necessary.
-  The tool uses an internal language which is like Python but not Python.
   You can read more about it here:
   https://mesonbuild.com/FAQ.html#why-is-meson-not-just-a-python-module-so-i-could-code-my-build-setup-in-python.
   But such reasons not to use the 'real' language are not convincing for me.
   I am not saying that all reasons are silly and I realize it is not possible
   to make a perfect build system as each of them has its advantages and
   disadvantages but at least the 'real' language gives you more freedom to do
   what you need.
-  It doesn't support target files with a wildcard:
   https://mesonbuild.com/FAQ.html#why-cant-i-specify-target-files-with-a-wildcard
-  They claim that Meson is 'as user friendly as possible' but I think
   it could be more user friendly in some areas.

The opinion that 'wildcard for target files is a bad thing' also exists in
CMake. For example, authors of Meson wrote that wildcards slow things down.
I don't agree with the position of developers of Meson and
CMake that specifying target files with a wildcard is a bad thing.
I agree that for big projects with a lot of files it can be slow in
some cases. But for all others it should be fast enough. Why didn't they
make it as an option? I don't know. An alternative with an external command
in Meson doesn't work very well, and authors of Meson should know about it.
There is no such a problem with wildcards in Waf.

**SCons**

Waf was created as alternative to this build system because:

::

   Thomas Nagy decided that SCons's fundamental issues (most notably the poor
   scalability) were too complex ...

It was taken from https://en.wikipedia.org/wiki/Waf. So in some things it's
similar to Waf and, as well as for Waf, it has a long learning curve.

**Premake/GENie**

I haven't tried to use it because I forgot about its existence. But it's not
a build system. It's a generator for some other build systems and IDE which is
another way to build projects. I don't know whether it is useful but the
project has status beta/alpha. I have checked some modules and it looks like
something is working but something is not. And it looks like it's quite complex
inside. However, the description of the project looks good.
Perhaps, I had to try to use it.

I found some info about problems with premake:
https://medium.com/@julienjorge/an-overview-of-build-systems-mostly-for-c-projects-ac9931494444.
And it doesn't look good to me.

**Bazel**

Well, I don't know a lot about this build system but I read some documentation and
tried some examples. I guess it's a normal choice
for big projects or for projects done internally in companies but is
definitely too big for small projects. And it has some other problems:
https://medium.com/windmill-engineering/bazel-is-the-worst-build-system-except-for-all-the-others-b369396a9e26
