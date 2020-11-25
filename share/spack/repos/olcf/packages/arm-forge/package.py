# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.pkg.builtin.arm_forge import ArmForge as ArmForgeBase


class ArmForge(ArmForgeBase):
    # To use remote clients, it is necessary to manually create a
    # `$PREFIX/allinearc` after installation that, at a minimum, sets the
    # ALLINEA_LICENSE_FILE environment variable, for example
    # 
    # ```
    # export ALLINEA_LICENSE_FILE=/sw/sources/ddt/licences/Titan.forge
    # ```
    #
    # among other things like tuning the loaded environment modules or tuning
    # runtime environment variables for MPI, etc. Each system will be different.
    version(
        "20.2-Redhat-8.0-x86_64",
        sha256="bed2e9429773504b5cc73b22fc25b9b39af1b665c3b67a2034a13f3b88cdd516",
        url="https://content.allinea.com/downloads/arm-forge-20.2-Redhat-8.0-x86_64.tar",
    )
    version(
        "20.2-Redhat-7.0-x86_64",
        sha256="26592a77c42f970f724f15b70cc5ce6af1078fd0ef9243a37c3215916cfa7cf4",
        url="https://content.allinea.com/downloads/arm-forge-20.2-Redhat-7.0-x86_64.tar",
    )
    version(
        "20.2-Suse-15.0-x86_64",
        sha256="a923c6f479e95511457b36e5ca4cbeb050f3da325d5e0f90e39c894c22db15df",
        url="https://content.allinea.com/downloads/arm-forge-20.2-Suse-15.0-x86_64.tar",
    )
    version(
        "20.2-Suse-12.0-x86_64",
        sha256="f78af9eb1c5150b3ff188a68a27be0d20c93173de887448923e4e65ea7aa2ef2",
        url="https://content.allinea.com/downloads/arm-forge-20.2-Suse-12.0-x86_64.tar",
    )
    version(
        "20.2-Ubuntu-18.04-x86_64",
        sha256="33e76d7a3f2423144765af7a46c117fd7b5d163bbab0b5a812526756f6d0722c",
        url="https://content.allinea.com/downloads/arm-forge-20.2-Ubuntu-18.04-x86_64.tar",
    )
    version(
        "20.2-Ubuntu-16.04-x86_64",
        sha256="6025af4720a83b432eac8ddb82a1028d34ffe618f758001606ae0c1f700c72ee",
        url="https://content.allinea.com/downloads/arm-forge-20.2-Ubuntu-16.04-x86_64.tar",
    )
    version(
        "20.2-Redhat-7.2-ppc64le",
        sha256="e13bc0c941629c9332660bced46e764d37d9a119b89a7e532975ac23d66662c5",
        url="https://content.allinea.com/downloads/arm-forge-20.2-Redhat-7.2-ppc64le.tar",
    )
    version(
        "20.2-Redhat-8.0-aarch64",
        sha256="fa465fa829d50137f59e90e9102716bf49df2674300b85fa4fc4046188f68a29",
        url="https://content.allinea.com/downloads/arm-forge-20.2-Redhat-8.0-aarch64.tar",
    )
    version(
        "20.2-Redhat-7.6-aarch64",
        sha256="0e8f9bff9a6bb6360c305e2069f6edd52323fe348559dfc3dcb90c0b052df115",
        url="https://content.allinea.com/downloads/arm-forge-20.2-Redhat-7.6-aarch64.tar",
    )
    version(
        "20.2-Suse-15.0-aarch64",
        sha256="6fc5634140d8e502d5d3e4f23d35046addd402fc0689fdfb977ce0f542ba8016",
        url="https://content.allinea.com/downloads/arm-forge-20.2-Suse-15.0-aarch64.tar",
    )
    version(
        "20.2-Suse-12.3-aarch64",
        sha256="481db75ce302c70ac5aa7fc12ec3af52057f41cb65127aad1f2605038f86406e",
        url="https://content.allinea.com/downloads/arm-forge-20.2-Suse-12.3-aarch64.tar",
    )
    version(
        "20.2-Ubuntu-18.04-aarch64",
        sha256="b3aa6ad95b2d51a48b019e9e9d3702bb96ca96da4da3f7abbe157498cd9b8902",
        url="https://content.allinea.com/downloads/arm-forge-20.2-Ubuntu-18.04-aarch64.tar",
    )
    version(
        "20.2-Ubuntu-16.04-aarch64",
        sha256="fbe03dde3eec0fc7cd53c68215f31bf8712f826d9edd6c7fd9449d50eb2a3812",
        url="https://content.allinea.com/downloads/arm-forge-20.2-Ubuntu-16.04-aarch64.tar",
    )
    version(
        "20.1-Redhat-8.0-x86_64",
        sha256="9c3731e35f29e997a646ad2fdffe9d35b4782ec0cf861158168e9e485c8382e1",
        url="https://content.allinea.com/downloads/arm-forge-20.1-Redhat-8.0-x86_64.tar",
    )
    version(
        "20.1-Redhat-7.0-x86_64",
        sha256="97d0b21a804659293f9ca5209053afa00e81a0a8c8b59eaff34bd4d258d3a7d1",
        url="https://content.allinea.com/downloads/arm-forge-20.1-Redhat-7.0-x86_64.tar",
    )
    version(
        "20.1-Suse-15.0-x86_64",
        sha256="4d9cda722bfb872111d622599060c9065480fa3a1aa0aaa134c1582a3483ede6",
        url="https://content.allinea.com/downloads/arm-forge-20.1-Suse-15.0-x86_64.tar",
    )
    version(
        "20.1-Suse-12.0-x86_64",
        sha256="16003dac11cd976ca0a921b16ffe9821208d753425462c2dddf5c183f6c5cb9f",
        url="https://content.allinea.com/downloads/arm-forge-20.1-Suse-12.0-x86_64.tar",
    )
    version(
        "20.1-Ubuntu-18.04-x86_64",
        sha256="0c4d302baa940ba33f0356e5c4d5bd705ca0e55f40200f002fa61fe62eb659f3",
        url="https://content.allinea.com/downloads/arm-forge-20.1-Ubuntu-18.04-x86_64.tar",
    )
    version(
        "20.1-Ubuntu-16.04-x86_64",
        sha256="790a78abfaaf32e2ccca33d6420a16c8f567de3533d2f4e439b0a5c6997d0962",
        url="https://content.allinea.com/downloads/arm-forge-20.1-Ubuntu-16.04-x86_64.tar",
    )
    version(
        "20.1-Redhat-7.2-ppc64le",
        sha256="e596877a46290f4c3f68274a81990c28e8ea8a1901cf10fbc1c959eeb8f1c1ca",
        url="https://content.allinea.com/downloads/arm-forge-20.1-Redhat-7.2-ppc64le.tar",
    )
    version(
        "20.1-Redhat-8.0-aarch64",
        sha256="0caf1b8b9afce5b1ae4204b6d6027fc7a8a3e535a64b59fce09dfa090e749ce6",
        url="https://content.allinea.com/downloads/arm-forge-20.1-Redhat-8.0-aarch64.tar",
    )
    version(
        "20.1-Redhat-7.6-aarch64",
        sha256="63570ee6c6f75d727db1897f68d1feb746a4f169d34b83a3bfdae878d601f9e6",
        url="https://content.allinea.com/downloads/arm-forge-20.1-Redhat-7.6-aarch64.tar",
    )
    version(
        "20.1-Suse-15.0-aarch64",
        sha256="ccbc02627a8291c5f19fd6d7e6a2aa13da6b08c405fbe3960c919d1caa2a6144",
        url="https://content.allinea.com/downloads/arm-forge-20.1-Suse-15.0-aarch64.tar",
    )
    version(
        "20.1-Suse-12.3-aarch64",
        sha256="684ba0d4e7656156ca90a474527b7f6545fd2eaeb38e16d63648c8fae82bdd20",
        url="https://content.allinea.com/downloads/arm-forge-20.1-Suse-12.3-aarch64.tar",
    )
    version(
        "20.1-Ubuntu-18.04-aarch64",
        sha256="684ba0d4e7656156ca90a474527b7f6545fd2eaeb38e16d63648c8fae82bdd20",
        url="https://content.allinea.com/downloads/arm-forge-20.1-Ubuntu-18.04-aarch64.tar",
    )
    version(
        "20.1-Ubuntu-16.04-aarch64",
        sha256="9f38ab2d04c0221c6dde4db50eec2264d416bd6656a655954c95a2f0b5f3d47d",
        url="https://content.allinea.com/downloads/arm-forge-20.1-Ubuntu-16.04-aarch64.tar",
    )

    def setup_run_environment(self, env):
        env.set('DDT_HOME', self.prefix)
