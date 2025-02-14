#!/bin/bash

git clone https://github.com/scylladb/scylla vulnerable_scylla

cd vulnerable_scylla

git checkout f4b1ad43d4e701538e60c5640032117c353577e2

# Initialize and update submodules
git submodule update --init --force --recursive

# Now patch Scylla with the vuln, and prepare cqlsh to run the exploit
cp ../cfop_mods/configure.py configure.py
cp ../cfop_mods/cqlsh.py tools/cqlsh/bin/cqlsh.py
cp ../cfop_mods/cooking_recipe.cmake seastar/cooking_recipe.cmake
cp ../cfop_mods/circular_buffer_fixed_capacity.hh seastar/include/seastar/core/circular_buffer_fixed_capacity.hh
cp ../cfop_mods/reactor.cc seastar/src/core/reactor.cc
cp ../cfop_mods/util.cc cql3/util.cc

# Build
./tools/toolchain/dbuild ./configure.py --mode=release
./tools/toolchain/dbuild ninja