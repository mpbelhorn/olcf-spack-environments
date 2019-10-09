##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import os


class Wgrib(Package):
    """WGRIB is a program to manipulate, inventory and decode GRIB files"""

    homepage = "http://www.cpc.ncep.noaa.gov/products/wesley/wgrib.html"
    url      = "ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib/wgrib.tar"

    version('1.8.1.2c', '406a0b9178a437b8d766ca8f542f431e')

    def url_for_version(self, version):
        """ This is just a link to the latest. Actual urls confuse spack
            such that it is unable to detect the compression type """
        return "ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib/wgrib.tar"

    def install(self, spec, prefix):
        # Nonstandard build system, needs -j 1 or it chokes
        gmake.jobs = 1
        gmake()

        mkdirp(prefix.bin)
        install('./wgrib', prefix.bin)
