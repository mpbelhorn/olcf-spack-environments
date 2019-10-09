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


class Wgrib2(Package):
    """WGRIB is a program to manipulate, inventory and decode GRIB files"""

    homepage = "http://www.cpc.ncep.noaa.gov/products/wesley/wgrib.html"
    url      = "http://www.ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/wgrib2.tgz"

    version('2.0.6c', 'a6c5a71b9a5b3837b0c9d82ae965b274')

    def url_for_version(self, version):
        """ This is just a link to the latest. Actual urls confuse spack
            such that it is unable to detect the compression type """
        return "http://www.ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/wgrib2.tgz"

    def install(self, spec, prefix):
        # Nonstandard build system, needs -j 1 or it chokes
        gmake.jobs = 1
        gmake()

        # Compensate for missing 'install' target in Makefile
        for d in ['bin', 'include', 'lib', 'share', 'man/man1']:
            dest = os.path.join(prefix, d)
            mkdirp(dest)
            for f in os.listdir(d):
                src = os.path.join(d, f)
                if os.path.isfile(src):
                    install(src, dest)
        
        # Don't forget the most important part, which is located in an
        # entirely different directory from all the other executables.
        install('wgrib2/wgrib2', prefix.bin)
