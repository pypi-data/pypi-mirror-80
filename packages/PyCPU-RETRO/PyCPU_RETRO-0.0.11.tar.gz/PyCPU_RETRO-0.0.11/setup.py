#!/usr/bin/env python3
# encoding: utf-8

from distutils.core import setup, Extension

names = []

cpu_module = Extension('PyCPU_RETRO', sources = names)

setup(name='PyCPU_RETRO',
      version='0.0.11',
      description='Dispatcher for the RETROFORTH CPU Type',
      ext_modules=[cpu_module])
