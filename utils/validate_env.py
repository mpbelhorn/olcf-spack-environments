#!/usr/bin/env spack-python

import pprint
import spack.store
import spack.config
import spack.caches
from spack.repo import Repo, RepoError
from spack.modules.common import root_path as module_root
from spack.util.path import canonicalize_path

printp = pprint.PrettyPrinter(indent=4).pprint

template_dirs = spack.config.get('config:template_dirs')
template_dirs = [canonicalize_path(x) for x in template_dirs]
repo_roots = spack.config.get('repos')
repos = []
for repo_root in repo_roots:
    try:
        repos.append(Repo(repo_root))
    except RepoError:
        continue
settings = {
    'install_root': spack.store.store.root,
    'template_dirs': template_dirs,
    'module_roots': {k: module_root(k) for k in ('tcl', 'lmod')},
    'misc_cache': spack.caches.misc_cache.root,
    'source_cache': spack.caches.fetch_cache.root,
    'mirrors': dict(spack.config.get('mirrors')),
    'repos': repos,
}

printp(settings)
