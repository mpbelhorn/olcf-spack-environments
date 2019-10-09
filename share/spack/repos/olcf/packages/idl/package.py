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
import sys
from spack import *


class Idl(Package):
    homepage = "http://www.harrisgeospatial.com/ProductsandTechnology/Software/IDL.aspx"
    url      = "file:///sw/sources/idl/idl-8.2.3.tar.gz"

    version('8.2.3', '84d77e9fe6d370d68616a6ea9ebddf00', expand=False)

    def setup_environment(self,spack_env,run_env):
      run_env.set('EXELIS_DIR','%s/%s/binary' % (self.prefix,str(self.version)))
      run_env.set('IDL_DIR', '%s/%s/binary/idl82' % (self.prefix, str(self.version)))
      run_env.prepend_path('PATH', '%s/%s/binary/idl82/bin' % (self.prefix, str(self.version)))
      run_env.prepend_path('LD_LIBRARY_PATH', '%s/%s/binary/idl82/lib' % (self.prefix, str(self.version)))


    def install(self, spec, prefix):
      tar = which('tar')
      tar('xvf', self.stage.archive_file, '-C', prefix)
      return 0
