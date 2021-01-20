# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob
import os
import tempfile
from spack.pkg.builtin.ncl import Ncl as NclBase

class Ncl(NclBase):
    version('6.3.0', sha256='d2cd8a1de1c498c1832f0765113ad58086d1d3b29bf5d2cc9b1ba60f1919951c')

    variant('mpi', default=True, description='Build with MPI-enabled dependencies.')

    depends_on('esmf~mpi~pnetcdf', type='run', when="~mpi")
    depends_on('esmf+mpi+pnetcdf', type='run', when="+mpi")
    depends_on('netcdf-c~mpi~parallel-netcdf', when="~mpi")
    depends_on('netcdf-c+mpi+parallel-netcdf', when="+mpi")
    depends_on('hdf5+szip~mpi', when="~mpi")
    depends_on('hdf5+szip+mpi', when="+mpi")

    depends_on('netcdf-c+hdf4', when='+hdf4')

    def prepare_install_config(self):
        # Remove the results of the previous configuration attempts.
        self.delete_files('./Makefile', './config/Site.local')

        # Generate an array of answers that will be passed to the interactive
        # configuration script.
        config_answers = [
            # Enter Return to continue
            '\n',
            # Build NCL?
            'y\n',
            # Parent installation directory :
            "'%s'\n" % self.spec.prefix,
            # System temp space directory   :
            "'%s'\n" % tempfile.gettempdir(),
            # Build NetCDF4 feature support (optional)?
            'y\n'
        ]

        if self.spec.satisfies('+hdf4'):
            config_answers.extend([
                # Build HDF4 support (optional) into NCL?
                'y\n',
                # Also build HDF4 support (optional) into raster library?
                'y\n',
                # Did you build HDF4 with szip support?
                'y\n' if self.spec.satisfies('^hdf+szip') else 'n\n'
            ])
        else:
            config_answers.extend([
                # Build HDF4 support (optional) into NCL?
                'n\n',
                # Also build HDF4 support (optional) into raster library?
                'n\n'
            ])

        config_answers.extend([
            # Build Triangle support (optional) into NCL
            'y\n' if '+triangle' in self.spec else 'n\n',
            # If you are using NetCDF V4.x, did you enable NetCDF-4 support?
            'y\n',
            # Did you build NetCDF with OPeNDAP support?
            'y\n',
            # Build GDAL support (optional) into NCL?
            'y\n' if '+gdal' in self.spec else 'n\n',
            # Build EEMD support (optional) into NCL?
            'n\n',
            # Build Udunits-2 support (optional) into NCL?
            'y\n' if '+uduints2' in self.spec else 'n\n',
            # Build Vis5d+ support (optional) into NCL?
            'n\n',
            # Build HDF-EOS2 support (optional) into NCL?
            'n\n',
            # Build HDF5 support (optional) into NCL?
            'y\n',
            # Build HDF-EOS5 support (optional) into NCL?
            'n\n',
            # Build GRIB2 support (optional) into NCL?
            'n\n',
            # Enter local library search path(s) :
            "%s\n" % ' '.join([
                self.spec[key].prefix.lib for key in ('fontconfig', 'pixman', 'bzip2')
                ]),
            # Enter local include search path(s) :
            # All other paths will be passed by the Spack wrapper.
            "'%s'\n" % join_path(self.spec['freetype'].prefix.include,
                                 'freetype2'),
            # Go back and make more changes or review?
            'n\n',
            # Save current configuration?
            'y\n'
        ])

        config_answers_filename = 'spack-config.in'
        config_script = Executable('./Configure')

        with open(config_answers_filename, 'w') as f:
            f.writelines(config_answers)

        with open(config_answers_filename, 'r') as f:
            config_script(input=f)

