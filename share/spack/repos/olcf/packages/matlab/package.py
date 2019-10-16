# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import subprocess


class Matlab(Package):
    """MATLAB (MATrix LABoratory) is a multi-paradigm numerical computing
    environment and fourth-generation programming language. A proprietary
    programming language developed by MathWorks, MATLAB allows matrix
    manipulations, plotting of functions and data, implementation of
    algorithms, creation of user interfaces, and interfacing with programs
    written in other languages, including C, C++, C#, Java, Fortran and Python.

    Note: MATLAB is licensed software. You will need to create an account on
    the MathWorks homepage and download MATLAB yourself. Spack will search your
    current directory for the download file. Alternatively, add this file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://www.mathworks.com/products/matlab.html"
    version('R2018b', sha256='8cfcddd3878d3a69371c4e838773bcabf12aaf0362cc2e1ae7e8820845635cac')
    version('R2017a', '5d9c60136b8d1133e82489aa0ee1d5f7')
    version('R2016b', 'b0e0b688894282139fa787b5a86a5cf7')

    variant(
        'mode',
        default='interactive',
        values=('interactive', 'silent', 'automated'),
        description='Installation mode (interactive, silent, or automated)'
    )

    ## Keyfile must have lines formated as:
    ## ```
    ## {SPACK PACKAGE VERSION}: {INSTALL_KEY}
    ## ```
    variant(
        'keyfile',
        default='/sw/sources/matlab/install_keys',
        values=lambda x: True,  # Anything goes as a keyfile
        description='The file in which to find the installation key.'
    )

    # Licensing
    license_required = True
    license_comment  = '#'
    license_files    = ['licenses/license.dat']
    license_vars     = ['MLM_LICENSE_FILE', 'LM_LICENSE_FILE']
    license_url      = 'https://www.mathworks.com/help/install/index.html'

    extendable = True

    def url_for_version(self, version):
        return "file://{0}/matlab_{1}_glnxa64_dvd.tar.gz".format('/sw/sources/matlab', version)

    def configure(self, spec, prefix):
        key = None
        with open(spec.variants['keyfile'].value, 'r') as keyfile:
           content = keyfile.readlines()
           for line in content:
               if line.startswith(str(spec.version)):
                   key = line.split(':')[1].strip()
                   break
        if key is None:
            raise InstallError("Install key not found in given keyfile."
                               " See package for details.")

        config = {
            'destinationFolder':   prefix,
            'mode':                spec.variants['mode'].value,
            'fileInstallationKey': key,
            'licensePath':         self.global_license_file,
            'agreeToLicense':      'yes',
        }

        # Store values requested by the installer in a file
        with open('spack_installer_input.txt', 'w') as input_file:
            for option, value in config.items():
                input_file.write('{0}={1}\n'.format(option, value))

    def install(self, spec, prefix):
        chmod = which('chmod')
        chmod.add_default_arg('+x')
        chmod('install')
        chmod('bin/glnxa64/install_unix')
        chmod('bin/glnxa64/usResourceCompiler')
        with working_dir('sys/java/jre/glnxa64/jre/bin/'):
            for f in os.listdir('.'):
                chmod(f)

        self.configure(spec, prefix)

        # Run silent installation script
        # Full path required
        input_file = join_path(
            self.stage.source_path, 'spack_installer_input.txt')
        subprocess.call(['./install', '-inputFile', input_file])
