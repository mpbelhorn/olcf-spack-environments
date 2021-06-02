# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkg.builtin.raja import Raja as RajaBase


class Raja(RajaBase):
    version('0.2.3', tag="v0.2.3", submodules="True")
    version('0.2.2', tag="v0.2.2", submodules="True")
    version('0.1.0', tag="v0.1.0", submodules="True")
    conflicts('%gcc@:4.999', when='@0.5:')

