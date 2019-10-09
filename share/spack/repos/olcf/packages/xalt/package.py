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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install xalt
#
# You can edit this file again by typing:
#
#     spack edit xalt
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Xalt(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/Fahey-McLay/xalt"
    url      = "https://github.com/Fahey-McLay/xalt/archive/0.7.5.tar.gz"

    version('0.7.5', '753898837f255d741939e39ea2ae5255')

    variant('alps', default=False)
    variant('openmpi', default=False)

    # FIXME: Add dependencies if required.
    # depends_on('foo')
    patch('xalt-olcf.patch-0.7.5',when='@0.7.5')

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        configure('--with-transmission=broker','--prefix={0}'.format(prefix))

        # FIXME: Add logic to build and install here.
        env={'MAKEFLAGS': ''}
        make('echo',env=env)
        make('install',env=env)

        # Copy the xalt_syshohst.py file into place
        cp=which("cp")
        cp(self.package_dir+"/xalt_syshost.py",prefix+"/site/xalt_syshost.py")

        ## In bin/, delete ibrun*, ld.gold, mpirun.lsf and srun.
        ## Keep ld and xalt_helper_functions.sh
        ## Keep ( aprun || (mpirun && mpiexec) ) as appropriate for the system
        to_rm=['mpirun','mpiexec','aprun','ibrun','ibrun.symm','ld.gold','mpirun.lsf','srun']
        if "+alps" in spec:
          to_rm.remove('aprun')
        elif "+openmpi" in spec:
          to_rm.remove('mpirun')
          to_rm.remove('mpiexec')

	rm=which("rm")
        for rmfile in to_rm:
          rm(prefix+"/bin/"+rmfile)
