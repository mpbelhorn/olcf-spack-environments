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


class P3dfft(AutotoolsPackage):
    '''
    Parallel Three-Dimensional Fast Fourier Transforms, dubbed P3DFFT, is a
    library for large-scale computer simulations on parallel platforms. 3D FFT
    is an important algorithm for simulations in a wide range of fields,
    including studies of turbulence, climatology, astrophysics and material
    science.
    '''

    homepage = "http://www.p3dfft.net"
    url      = "https://github.com/sdsc/p3dfft/releases/download/v2.7.5/p3dfft-2.7.5.tar.gz"

    version('2.7.5', 'e2a54e0eb364506f06053317cf625fd5')

    variant('essl', default=False,
            description="Enables support for ESSL")
    variant('fftw', default=True,
            description="Enables support for FFTW")
    variant('openmp', default=True,
            description="Enables openmp support")
    variant('openmpi',
            default=True, description="Enables openmpi support")
    variant('oned', default=False,
            description="Enables 1D decomposition as the default")
    variant('estimate', default=False,
            description="Disables run-time tuning to select the fastest algorithm for computing FFTs")
    variant('patient', default=False,
            description="Enables search-once-for-the-fastest-algorithm")
    variant('dimsc', default=False,
            description="Cartesian processor grid coords according to C convention.")
    variant('useeven', default=False,
            description="Uses MPI_AllToAll instead of MPI_AllToAllv. Recommended for Cray XTs")
    variant('stride1', default=False,
            description="Enables stride-1 data structures on output. Recommended")
    variant('nblx', default=False,
            description="Defines loop blocking factor NBL_X")
    variant('nbly1', default=False,
            description="To define loop blocking factor NBL_Y1")
    variant('nbly2', default=False,
            description="To define loop blocking factor NBL_Y2")
    variant('nblz', default=False,
            description="To define loop blocking factor NBL_Z")
    variant('single', default=False,
            description="Enables single precision")

    depends_on('mpi')
    depends_on('fftw', when='+fftw')
    depends_on('essl', when='+essl')
    depends_on('autoconf@2.65:', type='build')

    parallel = False

    def configure_args(self):
        args = []

        if not self.spec.satisfies('+fftw') and not self.spec.satisfies('+essl'):
          raise RuntimeError("+fftw or +essl is required to build!")
        
        if self.spec.satisfies("%gcc"):
          args.append("--enable-gnu")
        elif self.spec.satisfies("%pgi"):
          args.append("--enable-pgi")
        elif self.spec.satisfies("%intel"):
          args.append("--enable-intel")
        elif self.spec.satisfies("%cce"):
          args.append("--enable-cray")
        elif self.spec.satisfies("%xl"):
          args.append("--enable-ibm")

        if self.spec.satisfies('+fftw'):
          args.append("--enable-fftw")
          args.append("--with-fftw=%s" % self.spec['fftw'].prefix)
        elif self.spec.satisfies('+essl'):
          args.append("--enable-essl")
        
        if self.spec.satisfies('+openmp'):
          args.append("--enable-openmp")

        if self.spec.satisfies('^openmpi'):
          args.append("--enable-openmpi")

        if self.spec.satisfies('+oned'):
          args.append("--enable-oned")

        if self.spec.satisfies('+estimate') and self.spec.satisfies('+fftw'):
          args.append('--enable-estimate')
        elif self.spec.satisfies('+estimate') and not self.spec.satisfies('+fftw'):
          raise RuntimeError("+estimate variant requires +fftw")

        if self.spec.satisfies('+patient') and self.spec.satisfies('+fftw'):
          args.append('--enable-patient')
        elif self.spec.satisfies('+patient') and not self.spec.satisfies('+fftw'):
          raise RuntimeError("+patient variant requires +fftw")

        if self.spec.satisfies('+dimsc'):
          args.append('--enable-dimsc')

        if self.spec.satisfies('+useeven'):
          args.append('--enable-useeven')

        if self.spec.satisfies('+stride1'):
          args.append('--enable-stride1')

        if self.spec.satisfies('+nblx'):
          args.append('--enable-nblx32')

        if self.spec.satisfies('+nbly1'):
          args.append('--enable-nbly1=32')

        if self.spec.satisfies('+nbly2'):
          args.append('--enable-nbly2=32')

        if self.spec.satisfies('+nblz'):
          args.append('--enable-nblz=32')

        if self.spec.satisfies('+single'):
          args.append('--enable-single')

        return args
