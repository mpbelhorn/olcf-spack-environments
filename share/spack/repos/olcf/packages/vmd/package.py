# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os

class Vmd(Package):
    """VMD is designed for modeling, visualization, and analysis of biological
    systems such as proteins, nucleic acids, lipid bilayer assemblies, etc. It may
    be used to view more general molecules, as VMD can read standard Protein Data
    Bank (PDB) files and display the contained structure. VMD can act
    as a graphical front end for an external MD program by displaying and animating
    a molecule undergoing simulation on a remote computer.
    """
    homepage = "https://www.ks.uiuc.edu/Research/vmd/"
    url      = "http://www.ks.uiuc.edu/Research/vmd/vmd-1.9.3/files/final/vmd-1.9.3.bin.LINUXAMD64-CUDA8-OptiX4-OSPRay111p1.opengl.tar.gz"

    version('1.9.3', '7f0cefa52e4ac3645018512fed70e474', url='http://www.ks.uiuc.edu/Research/vmd/vmd-1.9.3/files/final/vmd-1.9.3.bin.LINUXAMD64-CUDA8-OptiX4-OSPRay111p1.opengl.tar.gz')

    def install(self, spec, prefix):
      env = os.environ
      env["VMDINSTALLBINDIR"] = prefix.bin
      env["VMDINSTALLLIBRARYDIR"] = prefix.lib

      configure()

      with working_dir("src"):
        make("install", env=env)
