#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This file is part of crossroad.
# Copyright (C) 2017 Jehan <jehan at girinstud.io>
#
# crossroad is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# crossroad is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with crossroad.  If not, see <http://www.gnu.org/licenses/>.

'''
Setups a compilation environment for native builds.
'''


# pkg-config: /usr/bin/i686-redhat-linux-gnu-pkg-config
# Or: i686-pc-linux-gnu-pkg-config ???

# Am I 32 or 64-bit for native: https://www.fastwebhost.in/blog/how-to-find-if-linux-is-running-on-32-bit-or-64-bit/
# gcc just use -m32/-m64: https://www.cyberciti.biz/tips/compile-32bit-application-using-gcc-64-bit-linux.html
# -mtune=i686 works too? https://www.linuxquestions.org/questions/programming-9/%5Bcross-compiling%5Dx86_64-system-compile-target-i686-872066/

# Require python 3.3 for shutil.which
import shutil
import subprocess
import glob
import os.path
import sys

install_datadir = os.path.join(os.path.abspath('@DATADIR@'), 'share')

name = 'native'
short_description = 'Native platform ({})'.format(subprocess.getoutput('uname -mo'))

def is_available():
    return True

def prepare(prefix):
    '''
    Prepare the environment.
    Note that copying these libs is unnecessary for building, since the
    system can find these at build time. But when moving the prefix to a
    Windows machine, if ever we linked against these dll and they are
    absent, the executable won't run.
    '''
    try:
        env_bin = os.path.join(prefix, 'bin')
        os.makedirs(env_bin, exist_ok = True)
    except PermissionError:
        sys.stderr.write('"{}" cannot be created. Please verify your permissions. Aborting.\n'.format(env_path))
        return False
    return True
