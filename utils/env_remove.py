#!/usr/bin/env spack-python

import sys
import pprint
import itertools
import spack.store
import spack.config
import spack.environment
from spack.spec_list import SpecListError

printp = pprint.PrettyPrinter(indent=4).pprint

query_spec = ' '.join(sys.argv[1:])

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
        spec.dag_hash(): spec for spec in env_spec_list
        if query_filter(spec, query_spec)}

uninstall_list = [
        spec for dag_hash, spec in env_specs_by_hash.items()
        if dag_hash in installed_specs_by_hash]
from spack.cmd.uninstall import do_uninstall, confirm_removal, _remove_from_env

remove_list = list()
specs = set(uninstall_list).union(set(remove_list))
confirm_removal(specs)
if env:
    # Remove all the specs that are supposed to be uninstalled or just
    # removed.
    with env.write_transaction():
        for spec in itertools.chain(remove_list, uninstall_list):
            try:
                _remove_from_env(spec, env)
            except SpecListError:
                pass
        env.write()

# Uninstall everything on the list
do_uninstall(env, uninstall_list, force=True)

