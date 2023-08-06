#!/usr/bin/env python3
# encoding: utf-8

from distutils.core import setup, Extension

cpp_module = Extension('PyCPU_CPP', sources = [])

setup(name='PyCPU_CPP',
      version='0.0.42',
      description='CPP Bindings for PyCPU',
      ext_modules=[cpp_module])
