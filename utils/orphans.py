#!/usr/bin/env spack-python

import sys
import itertools
import spack.store
import spack.config
import spack.environment


query_spec = ''

def query_filter(spec, query_spec=None):
    if query_spec:
        return spec.satisfies(query_spec)
    return True

def installed_at(spec, prefix):
    return spec.concrete and spec.prefix.startswith(prefix)


env = spack.environment._active_environment
if not env:
    sys.exit(1)
env_install_prefix = spack.store.store.root

db_args = {'installed': True}
if query_spec:
    db_args['query_spec'] = query_spec

installed_specs = spack.store.db.query_local(**db_args)
installed_specs_by_hash = {
        spec.build_hash(): spec for spec in installed_specs
        if installed_at(spec, env_install_prefix)}


env_spec_list = list()
for spec_hash in env.concretized_order:
    spec = env.specs_by_hash[spec_hash]
    specs = (spec.traverse(deptype=('link', 'build', 'run')))
    env_spec_list.extend(specs)

env_specs_by_hash = {
        spec.dag_hash(): spec.name for spec in env_spec_list
        if query_filter(spec, query_spec)}
orphaned_specs = {
        hash: spec for hash, spec in installed_specs_by_hash.items()
        if hash not in env_specs_by_hash.keys()}

from spack.cmd.uninstall import do_uninstall, confirm_removal, _remove_from_env

remove_list = list()
uninstall_list = orphaned_specs.values()
specs = set(uninstall_list).union(set(remove_list))
confirm_removal(specs)
if env:
    # Remove all the specs that are supposed to be uninstalled or just
    # removed.
    with env.write_transaction():
        for spec in itertools.chain(remove_list, uninstall_list):
            _remove_from_env(spec, env)
        env.write()

# Uninstall everything on the list
do_uninstall(env, uninstall_list, force=False)
