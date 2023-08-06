#!/usr/bin/env python3
# encoding: utf-8

from distutils.core import setup, Extension

names = ['PyCPU_RETRO70Z_ID0000.cpp']

names.append('includes\\sqlite\\sqlite3.c')

cpu_module = Extension('PyCPU_RETRO70Z_ID0000_CPP', sources = names)

setup(name='PyCPU_RETRO70Z_ID0000_CPP',
      version='0.0.11',
      description='CPP Module for PyCPU_RETRO70Z_ID0000_CPP',
      ext_modules=[cpu_module])
