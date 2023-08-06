#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This file is part of crossroad.
# Copyright (C) 2013 Jehan <jehan at girinstud.io>
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
Setups a cross-compilation environment for Microsoft Windows operating systems (64-bit).
'''

# Require python 3.3 for shutil.which
import shutil
import subprocess
import glob
import os.path
import sys

install_datadir = os.path.join(os.path.abspath('@DATADIR@'), 'share')

name = 'w64'

short_description = 'Windows 64-bit'

if os.path.isfile('/etc/redhat-release'):
    mandatory_binaries = {
        'x86_64-w64-mingw32-gcc': 'mingw64-gcc',
        'x86_64-w64-mingw32-ld': 'mingw64-binutils'
        }

    languages = {
        'C' : {'x86_64-w64-mingw32-gcc': 'mingw64-gcc'},
        'C++': {'x86_64-w64-mingw32-c++': 'mingw64-gcc-c++'},
        'Ada': {'x86_64-w64-mingw32-gnat': 'mingw64-gcc-gnat?'},
        'OCaml': {'x86_64-w64-mingw32-ocamlc': 'mingw64-gcc-ocaml?'},
        'fortran': {'x86_64-w64-mingw32-gfortran': 'mingw64-gcc-gfortran'},
        'Objective C' : {'x86_64-w64-mingw32-gobjc': 'mingw64-gcc-objc'},
        'Objective C' : {'x86_64-w64-mingw32-gobjc++': 'mingw64-gcc-objc++'}
        }
else:
    mandatory_binaries = {
        'x86_64-w64-mingw32-gcc': 'gcc-mingw-w64-x86-64',
        'x86_64-w64-mingw32-ld': 'binutils-mingw-w64-x86-64'
        }

    languages = {
        'C' : {'x86_64-w64-mingw32-gcc': 'gcc-mingw-w64-x86-64'},
        'C++': {'x86_64-w64-mingw32-c++': 'g++-mingw-w64-x86-64'},
        'Ada': {'x86_64-w64-mingw32-gnat': 'gnat-mingw-w64-x86-64'},
        'OCaml': {'x86_64-w64-mingw32-ocamlc': 'mingw-ocaml'},
        'fortran': {'x86_64-w64-mingw32-gfortran': 'gfortran-mingw-w64-x86-64'},
        'Objective C' : {'x86_64-w64-mingw32-gobjc': 'gobjc-mingw-w64-x86-64'},
        'Objective C' : {'x86_64-w64-mingw32-gobjc++': 'gobjc++-mingw-w64-x86-64'}
        }

def is_available():
    '''
    Is it possible on this computer?
    '''
    for bin in mandatory_binaries:
        if shutil.which(bin) is None:
            return False
    return True

def requires():
    '''
    Output on standard output necessary packages and what is missing on
    the current installation.
    '''
    requirements = ''
    for bin in mandatory_binaries:
        requirements += '- {} [package "{}"]'.format(bin, mandatory_binaries[bin])
        if shutil.which(bin) is None:
            requirements += " (missing)\n"
        else:
            requirements += " (ok)\n"
    return requirements

def language_list():
    '''
    Return a couple of (installed, uninstalled) language list.
    '''
    uninstalled_languages = {}
    installed_languages = []
    for name in languages:
        for bin in languages[name]:
            if shutil.which(bin) is None:
                # List of packages to install.
                uninstalled_languages[name] = [languages[name][f] for f in languages[name]]
                # Removing duplicate packages.
                uninstalled_languages[name] = list(set(uninstalled_languages[name]))
                break
        else:
            installed_languages.append(name)
    return (installed_languages, uninstalled_languages)

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
    gcc_libs = subprocess.check_output(['x86_64-w64-mingw32-gcc', '-print-file-name='], universal_newlines=True)
    for dll in glob.glob(gcc_libs.strip() + '/*.dll'):
        try:
            os.symlink(dll, os.path.join(os.path.join(env_bin, os.path.basename(dll))))
        except OSError:
            # A failed symlink is not necessarily a no-go. Let's just output a warning.
            sys.stderr.write('Warning: crossroad failed to symlink {} in {}.\n'.format(dll, env_bin))
    return True

def crossroad_install(*packages:list, src:bool = False):
    '''
    Install the list of packages and all their dependencies.
    If --src is provided, it installs the source packages, and not the main packages.
    '''
    if len(packages) == 0:
        sys.stderr.write('Please provide at least one package name to install.\n')
        sys.exit(os.EX_USAGE)

    command = [os.path.join(install_datadir, 'crossroad/scripts/crossroad-mingw-install.py'),
               '-a', name, '--deps']
    if src:
        command += ['--src']
    command += list(packages)
    return subprocess.call(command, shell=False)

def crossroad_update():
    '''
    Update the repository information.
    '''
    command = [os.path.join(install_datadir, 'crossroad/scripts/crossroad-mingw-install.py'),
               '-a', name, '--update']
    return subprocess.call(command, shell=False)

def crossroad_list_files(*packages, src:bool = False):
    '''
    List files provided by packages.
    '''
    if len(packages) == 0:
        sys.stderr.write('Please provide at least one package name.\n')
        sys.exit(os.EX_USAGE)

    command = [os.path.join(install_datadir, 'crossroad/scripts/crossroad-mingw-install.py'),
               '-a', name, '--list-files']
    if src:
        command += ['--src']
    command += packages
    return subprocess.call(command, shell=False)

def crossroad_info(*packages, src:bool = False):
    '''
    Display package details.
    '''
    if len(packages) == 0:
        sys.stderr.write('Please provide at least one package name.\n')
        sys.exit(os.EX_USAGE)

    command = [os.path.join(install_datadir, 'crossroad/scripts/crossroad-mingw-install.py'),
               '-a', name, '--info']
    if src:
        command += ['--src']
    command += list(packages)
    return subprocess.call(command, shell=False)

def crossroad_uninstall(*packages, src:bool = False):
    '''
    Uninstall packages.
    '''
    if len(packages) == 0:
        sys.stderr.write('Please provide at least one package name.\n')
        sys.exit(os.EX_USAGE)

    command = [os.path.join(install_datadir, 'crossroad/scripts/crossroad-mingw-install.py'),
               '-a', name, '--uninstall']
    if src:
        command += ['--src']
    command += list(packages)
    return subprocess.call(command, shell=False)

def crossroad_search(*keywords, src:bool = False, search_files:bool = False):
    '''
    Search keywords in package names.
    If --search-files is also set, also search in files.
    '''
    if len(keywords) == 0:
        sys.stderr.write('Please provide at least one package name.\n')
        sys.exit(os.EX_USAGE)

    command = [os.path.join(install_datadir, 'crossroad/scripts/crossroad-mingw-install.py'),
               '-a', name, '--search']
    if src:
        command += ['--src']
    if search_files:
        command += ['--list-files']
    command += list(keywords)
    return subprocess.call(command, shell=False)

def crossroad_mask(*packages, src:bool = False):
    '''
    Mask packages.
    '''
    if len(packages) == 0:
        sys.stderr.write('Please provide at least one package name.\n')
        sys.exit(os.EX_USAGE)

    command = [os.path.join(install_datadir, 'crossroad/scripts/crossroad-mingw-install.py'),
               '-a', name, '--mask']
    if src:
        command += ['--src']
    command += list(packages)
    return subprocess.call(command, shell=False)

def crossroad_unmask(*packages, src:bool = False):
    '''
    Unmask packages.
    '''
    if len(packages) == 0:
        sys.stderr.write('Please provide at least one package name.\n')
        sys.exit(os.EX_USAGE)

    command = [os.path.join(install_datadir, 'crossroad/scripts/crossroad-mingw-install.py'),
               '-a', name, '--unmask']
    if src:
        command += ['--src']
    command += list(packages)
    return subprocess.call(command, shell=False)

def crossroad_source(set:str = None):
    '''
    List or set repository sources.
    '''
    if set is None:
      command = [os.path.join(install_datadir, 'crossroad/scripts/crossroad-mingw-install.py'),
                 '-a', name, '--list-sources']
      return subprocess.call(command, shell=False)
    else:
      command = [os.path.join(install_datadir, 'crossroad/scripts/crossroad-mingw-install.py'),
                 '-a', name, '--set-source', set]
      return subprocess.call(command, shell=False)
