#!/usr/bin/python
#
# (C) 2018 Riad S. Wahby <rsw@cs.stanford.edu> and the FaCT authors
#
# Python FFI interface to FaCT code

from __future__ import print_function
import cffi
import os
import subprocess

# python3 compatibility
try:
    basestring
except NameError:
    basestring = str

# adapted from cffi/recompiler.py
def _modname_to_file(outputdir, modname):
    parts = modname.split('.')
    try:
        os.makedirs(os.path.join(outputdir, *parts[:-1]))
    except OSError:
        pass
    return os.path.join(outputdir, *parts)

# wrapper around CFFI for FaCT code
class CTFFI(cffi.FFI):
    _assigned_fact_source = None

    def __init__(self, factpath="fact.byte"):
        super(CTFFI, self).__init__()
        self._ffi_compile = super(CTFFI, self).compile
        self._fact_exec = factpath

    def set_fact_source(self, module_name, source_string):
        if self._assigned_fact_source is not None:
            raise ValueError("set_fact_source() cannot be called multiple times in one CTFFI object")

        if not isinstance(module_name, basestring):
            raise TypeError("'module_name' must be a string")

        if os.sep in module_name or (os.altsep and os.altsep in module_name):
            raise ValueError("'module_name' must not contain '/'; use package.module instead")

        self._assigned_fact_source = (str(module_name), source_string)

    def compile(self, tmpdir='.', verbose=0, target=None, debug=None):
        (module_name, fact_source) = self._assigned_fact_source

        # step 1: create FaCT source file
        basefilename = _modname_to_file(tmpdir, module_name) + '_fact_module'
        factfilename = basefilename + '.fact'
        factheadername = basefilename + '.h'
        factobjectname = basefilename + '.o'

        with open(factfilename, 'w') as factfile:
            factfile.write(fact_source)

        # step 2: invoke FaCT compiler
        if subprocess.call([self._fact_exec, factfilename, '-opt', 'O2', '-generate-header']) != 0:
            raise RuntimeError("fact invocation returned non-zero status")

        # step 3: read in the resulting header file
        with open(factheadername, 'r') as factheader:
            headercontents = ''.join( x for x in factheader.readlines() if x[0] != '#' )

        ### Verbose mode: print header
        if verbose:
            print(headercontents)

        # step 4: call into CFFI
        self.set_source(module_name, headercontents, extra_objects=[factobjectname])
        self.cdef(headercontents)

        # step 5: compile the CFFI object
        self._ffi_compile(tmpdir=tmpdir, verbose=verbose, target=target, debug=debug)
