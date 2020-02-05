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
import os
import argparse
import llnl.util.tty as tty
import llnl.util.filesystem as fs
import spack
import spack.spec
import spack.environment as ev
import spack.cmd

description = 'Custom utilities used by the OLCF'
section = "olcf"
level = "long"

#: List of subcommands of `spack env`
subcommands = [
    ['show-env', 'show'],
    'deploy',
]

subcommand_functions = {}


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


class OLCFEnv(ev.Environment):
    '''Derived environment class to wrap specific methods.'''

    def _install(self, spec, **install_args):
        display_specs([spec])
        spec.package.do_install(**install_args)

        # Make sure log directory exists
        log_path = self.log_path
        fs.mkdirp(log_path)

        with fs.working_dir(self.path):
            # Link the resulting log file into logs dir
            build_log_link = os.path.join(
                log_path, '%s-%s.log' % (spec.name, spec.dag_hash(7)))
            if os.path.lexists(build_log_link):
                os.remove(build_log_link)
            os.symlink(spec.package.build_log_path, build_log_link)


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


def olcf_show_env_setup_parser(subparser):
    """Show concretized specs in the environment"""

def olcf_deploy_setup_parser(subparser):
    """Install concretized specs in the environment"""

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

def olcf_deploy(args):
    '''Install concretized specs in the environment.'''
    if hasattr(args, 'package') or hasattr(args, 'specfiles'):
        tty.die("olcf deploy acts on an environment, not individual packages")
    env, env_arg = None, getattr(args, 'env', None)
    if env_arg:
        if ev.exists(env_arg):
            ev.validate_env_name(env_arg)
            env = OLCFEnv(ev.root(env_arg))
        elif ev.is_env_dir(env_arg):
            env = OLCFEnv(env_arg)
        else:
            raise SpackEnvironmentError('no environment in %s' % env_arg)
    if ev._active_environment:
        env = ev._active_environment
    else:
        tty.die(
            '`spack olcf deploy` requires an environment',
            'activate an environment first:',
            '    spack env activate ENV',
            'or use:',
            '    spack -e ENV %s ...' % cmd_name)
    if env:
        if not hasattr(args, 'only_concrete'):
            # Concretize new specs
            concretized_specs = env.concretize()
            display_specs(concretized_specs)
            env.write()
        tty.msg("Installing environment %s" % env.name)
        env.install_all(args)
        return
    else:
        raise ev.SpackEnvironmentError('No environment found')
