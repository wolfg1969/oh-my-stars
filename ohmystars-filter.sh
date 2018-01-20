#!/bin/bash

py_version=`python -c "from __future__ import print_function;import sys; print('{}.{}'.format(*sys.version_info[:2]))"`

export PATH=$PATH:$HOME/.local/bin:$HOME/Library/Python/${py_version}/bin:/usr/local/bin
export PYTHONIOENCODING=UTF-8

read args <<< "{query}"

if [ "${alfred_version:0:1}" = "2" ]; then
	mystars $args -a
else
	mystars $args -3
fi

