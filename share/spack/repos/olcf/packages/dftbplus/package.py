# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkg.builtin.dftbplus import Dftbplus as DftbplusBase

class Dftbplus(DftbplusBase):
    version('20.2.1', sha256='6b1827a45b20d1757119a75abcb851cd4362e7abc58601094d029ed5922d6da7')

