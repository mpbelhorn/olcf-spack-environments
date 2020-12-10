#!/usr/bin/env python3

import pprint


def parse_file(path):
    specs = list()
    with open(path, 'r') as f:
        specs = f.readlines()
    return specs

NEW_SPECS = '/sw/sources/facspack/sw-manifest.summit.20201202.no-comp.log'
#NEW_SPECS = '/sw/sources/facspack/sw-manifest.summit.20201116.no-comp.log'
OLD_SPECS = '/sw/sources/facspack/sw-manifest.summit-rhel7.20201116.no-comp.log'

def main():
    new_specs = parse_file(NEW_SPECS)
    old_specs = parse_file(OLD_SPECS)

    packages = dict()
    changelog = dict()

    for spec in new_specs:
        name, version = spec.split('@')
        version = version.strip()
        changes = packages.setdefault(name, dict())
        new_versions = changes.setdefault('new', set())
        new_versions.add(version)

    for spec in old_specs:
        name, version = spec.split('@')
        version = version.strip()
        changes = packages.setdefault(name, dict())
        old_versions = changes.setdefault('old', set())
        old_versions.add(version)
    
    for name, pkg in packages.items():
        new = pkg.get('new')
        old = pkg.get('old')

        changes = changelog.setdefault(name, dict())
        if new and not old:
            changes['added'] = set(new)
        elif old and not new:
            changes['removed'] = set(old)
        else:
            changes['added'] = new.difference(old)
            changes['persisted'] = new.intersection(old)
            changes['removed'] = old.difference(new)

    for name in sorted(changelog.keys()):
        pkg = changelog[name]
        added = pkg.get('added', set())
        removed = pkg.get('removed')
        persisted = pkg.get('persisted', set())
        installed = added.union(persisted)
        if not installed:
            print("- {0}".format(name))
            if installed:
                print("    installed: {0}".format(', '.join(sorted(installed))))
            if added:
                print("    added:     {0}".format(', '.join(sorted(added))))
            if removed:
                print("    removed:   {0}".format(', '.join(sorted(removed))))
    # pp = pprint.PrettyPrinter(indent=4).pprint
    # pp(changelog)


if __name__ == '__main__':
    main()
