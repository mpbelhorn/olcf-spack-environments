# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Dftbplus(CMakePackage):
    """DFTB+ is an implementation of the
    Density Functional based Tight Binding (DFTB) method,
    containing many extensions to the original method."""

    homepage = "https://www.dftbplus.org"
    url      = "https://github.com/dftbplus/dftbplus/archive/19.1.tar.gz"

    version('20.2.1', sha256='6b1827a45b20d1757119a75abcb851cd4362e7abc58601094d029ed5922d6da7')
    version('19.1', sha256='4d07f5c6102f06999d8cfdb1d17f5b59f9f2b804697f14b3bc562e3ea094b8a8')

    resource(name='slakos',
             url='https://github.com/dftbplus/testparams/archive/dftbplus-18.2.tar.gz',
             sha256='bd191b3d240c1a81a8754a365e53a78b581fc92eb074dd5beb8b56a669a8d3d1',
             destination='external/slakos',
             when='@18.2:')

    variant('mpi', default=True,
            description="Build an MPI-paralelised version of the code.")

    variant('gpu', default=False,
            description="Use the MAGMA library "
            "for GPU accelerated computation")

    variant('elsi', default=False,
            description="Use the ELSI library for large scale systems. "
            "Only has any effect if you build with '+mpi'")

    variant('sockets', default=False,
            description="Whether the socket library "
            "(external control) should be linked")

    variant('arpack', default=False,
            description="Use ARPACK for excited state DFTB functionality")

    variant('transport', default=False,
            description="Whether transport via libNEGF should be included. "
            "Only affects parallel build. "
            "(serial version is built without libNEGF/transport)")

    variant('dftd3', default=False,
            description="Use DftD3 dispersion library "
            "(if you need this dispersion model)")

    depends_on('lapack')
    depends_on('blas')
    depends_on('scalapack', when="+mpi")
    depends_on('mpi', when="+mpi")
    depends_on('elsi', when="+elsi")
    depends_on('magma', when="+gpu")
    depends_on('arpack-ng', when="+arpack")
    depends_on('dftd3-lib@0.9.2', when="+dftd3")

    def cmake_args(self):
        spec = self.spec
        args = []

        if '+gpu' in spec:
            args.extend([
                '-DMAGMADIR={0}'.format(spec['magma'].prefix),
                '-DWITH_GPU=1',
                ])

        if '+mpi' in spec:
            args.extend([
                '-DSCALAPACKDIR={0}'.format(spec['scalapack'].prefix),
                '-DLIB_LAPACK={0}'.format(spec['blas'].libs.ld_flags),
                '-DWITH_MPI=1',
                ])

            if '+elsi' in self.spec:
                args.extend([
                    '-DWITH_ELSI=1',
                    '-DWITH_PEXSI={0}'.format(
                        '1' if '+enable_pexsi' in spec['elsi'] else '0'),
                    '-DELSIINCDIR={0}'.format(spec['elsi'].prefix.include),
                    '-DELSIDIR={0}'.format(spec['elsi'].prefix),
                    ])

        else:
            args.append('-DLIB_LAPACK+={0}'.format(spec['blas'].libs.ld_flags))

        if '+sockets' in self.spec:
            args.append('-DWITH_SOCKETS=1')

        if '+transport' in self.spec:
            args.append('-DWITH_TRANSPORT=1')

        if '+arpack' in self.spec:
            args.extend([
                '-DARPACK_LIBS={0}'.format(spec['arpack-ng'].libs.ld_flags),
                '-DWITH_ARPACK=1',
                ])

        if '+dftd3' in self.spec:
            args.extend([
                '-DCOMPILE_DFTD3=0',
                '-DDFTD3_INCS=-I{0}'.format(spec['dftd3-lib'].prefix.include),
                '-DDFTD3_LIBS=-L{0} -ldftd3'.format(spec['dftd3-lib'].prefix),
                '-DWITH_DFTD3=1',
                ])

        return args
