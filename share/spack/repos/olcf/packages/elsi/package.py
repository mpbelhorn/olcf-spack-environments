# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkg.builtin.elsi import Elsi as ElsiBase

class Elsi(ElsiBase):
    url = "https://gitlab.com/elsi_project/elsi_interface/-/archive/v2.6.4/elsi_interface-v2.6.4.tar.gz"

    version('2.6.4', sha256='4ab38c9ea8a1ab278f0cc1b1373f8008a5e8091f0c1a87ae0e826f803a9d20d0')
    version('2.2.1', sha256='4690907789a4f18985c16e7a7263d5d17d4751d386c88289a0127882abe17969')
