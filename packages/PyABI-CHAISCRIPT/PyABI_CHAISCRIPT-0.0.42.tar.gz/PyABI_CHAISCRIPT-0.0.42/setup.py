#!/usr/bin/env python3
# encoding: utf-8

from distutils.core import setup, Extension

names = ['PyABI_CHIASCRIPT.cpp']

names.append('sqlite3.c')

abi_module = Extension('PyABI_CHIASCRIPT_pyd', sources = names)

setup(name='PyABI_CHIASCRIPT_pyd',
      version='0.0.42',
      description='PyABI_CHIASCRIPT Implements the ChiaScript C++ Engine',
      ext_modules=[abi_module])
