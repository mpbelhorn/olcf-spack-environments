'''
OLCF Custom Spack Utilities.
============================

Custom utilities for the OLCF to manage common spack processes. This script must
be setup as a [custom extension](https://spack.readthedocs.io/en/latest/extensions.html) and invoked
as a spack subcommand.

show-env: Display the long-form concretized specs in a Spack environment lock
          file. An environment name is required if a spack environment is not
          already active.

          ```
          spack [-E env_name] olcf show-env
          ```
'''


import sys
import argparse
import llnl.util.tty as tty
import spack
import spack.environment as ev
import spack.cmd

description = 'Custom utilities used by the OLCF'
section = "olcf"
level = "long"

#: List of subcommands of `spack env`
subcommands = [
    ['show-env', 'show']
]

subcommand_functions = {}

def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='olcf_command')

    for name in subcommands:
        if isinstance(name, (list, tuple)):
            name, aliases = name[0], name[1:]
        else:
            aliases = []

        # add commands to subcommands dict
        function_name = 'olcf_%s' % name.replace('-', '_')
        function = globals()[function_name]
        for alias in [name] + aliases:
            subcommand_functions[alias] = function

        # make a subparser and run the command's setup function on it
        setup_parser_cmd_name = 'olcf_%s_setup_parser' % name.replace('-', '_')
        setup_parser_cmd = globals()[setup_parser_cmd_name]

        subsubparser = sp.add_parser(
            name, aliases=aliases, help=setup_parser_cmd.__doc__)
        setup_parser_cmd(subsubparser)


def display_specs(concretized_specs):
    """Displays the list of specs returned by `Environment.concretize()`.

    Args:
        concretized_specs (list): list of specs returned by
            `Environment.concretize()`
    """
    def _tree_to_display(spec):
        format_ = '{namespace}.{name}{@version}'
        format_ += '{%compiler.name}{@compiler.version}{compiler_flags}'
        format_ += '{variants}{arch=architecture}'
        return spec.tree(
            format=format_,
            recurse_dependencies=True,
            status_fn=spack.spec.Spec.install_status,
            show_types=True,
            hashlen=7,
            hashes=True)

    for user_spec, concrete_spec in concretized_specs:
        tty.msg('Concretized {0}'.format(user_spec))
        sys.stdout.write(_tree_to_display(concrete_spec))
        print('')


def olcf_show_env_setup_parser(subparser):
    """Show concretized specs in an environment"""


def olcf(parser, args):
    """Look for a function called olcf_<name> and call it."""
    action = subcommand_functions[args.olcf_command]
    action(args)


def olcf_show_env(args):
    '''Shows the concretized specs in an environment.'''
    env = ev.get_env(args, 'olcf show-env', required=True)
    if not env:
        raise ev.SpackEnvironmentError('No environment found')

    concretized_specs = list(env.concretized_specs())
    display_specs(concretized_specs)
