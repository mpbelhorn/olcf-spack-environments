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


class BbftpClient(AutotoolsPackage):
    """BBFTP is a software designed to quickly transfer files accross a wide
       area network."""

    homepage = "https://github.com/ucla/bbftp-client"
    url      = "http://software.in2p3.fr/bbftp/dist/bbftp-client-3.2.1.tar.gz"

    version('3.2.1', '8aacf78dddc6ccaf66931038d7d4b6cda')

    variant('openssl', default=True, description='Enable encryption support')

    depends_on('openssl', when='+openssl')

    def build_directory(self):
        return 'bbftpc'

    def configure_args(self):
        spec = self.spec

        options = []

        if spec.satisfies('+openssl'):
            options.append('--with-ssl={0}'.format(spec['openssl'].prefix))
        else:
            options.append('--without-ssl')

        return options
