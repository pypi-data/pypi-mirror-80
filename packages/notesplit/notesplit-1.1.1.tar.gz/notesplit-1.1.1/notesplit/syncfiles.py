#!/usr/bin/python3
import json, re, os, argparse, pathlib, xattr, fnmatch, shutil

def main(ignore_dot_files=False, listen_gitignore=False):
    """ Copies files with user.groups, user.individuals into folders, based on groups.json"""

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', help='Source folder to traverse.')
    parser.add_argument('-g', '--groups', help='Groups definitions json file.')
    parser.add_argument('-b', '--base', help='Base directory of source wiki (to trim paths to).')
    args = parser.parse_args()

    CWD = pathlib.Path(os.getcwd())
    SOURCE = pathlib.Path(args.source)
    GROUPS = pathlib.Path(args.groups)
    BASE = pathlib.Path(args.base or CWD)

    for i, p in enumerate([SOURCE, GROUPS, BASE]):
        if p.expanduser() == p and not str(p).startswith(p._flavour.sep):
            p = pathlib.Path(os.path.join(CWD, p))
            if i == 0: SOURCE = p
            if i == 1: GROUPS = p
            if i == 2: BASE = p

    group_defs = json.load(open(GROUPS, 'r'))

    indiv  = {k: os.path.abspath(os.path.expanduser(os.path.expandvars(group_defs['individuals'][k])))
              for k in group_defs['individuals']}

    groups = group_defs['groups']

    if os.path.isfile(SOURCE):
        IS_FILE = True
    else:
        IS_FILE = False


    for dir_name, subdir_list, file_list in os.walk(
            not IS_FILE and SOURCE or SOURCE.parent.expanduser()):

        if IS_FILE:
            dir_name = str(SOURCE.parent.expanduser())
            file_list = [SOURCE.name]

        dir_path = dir_name.split('/')[1:]

        if ignore_dot_files:
            if any([name.startswith('.') for name in dir_path]):
                continue

        for fname in file_list:

            path = os.path.join(dir_name, fname)

            if ignore_dot_files:
                if fname.startswith('.'):
                    continue


            if listen_gitignore:
                if os.path.exists('.gitignore'):
                    patterns = [line[:-1] for line in
                                open('.gitignore').readlines()
                                if not line.startswith('#') and line[:-1]]
                    any_matched = False

                    for pattern in patterns:
                        result = re.search(fnmatch.translate(pattern), path)

                        if result:
                            any_matched = True

                    if any_matched:
                        continue

            with open(path, 'r') as f:
                attrs = xattr.listxattr(f)
                if 'user.to' in attrs:
                    value = xattr.getxattr(f=f, attr='user.to')
                    share_to = str(value, 'utf-8').split(',')
                else:
                    share_to = []

                # Do set math to figure out groups and set subtractions. #

                inds = [it for it in share_to if it in indiv]
                grps = list(set(share_to) - set(inds))

                indivs_add = set([it for it in inds if not it.startswith('-')])
                indivs_rem = set([it[1:] for it in inds if it.startswith('-')])
                groups_add = set([it for it in grps if not it.startswith('-')])
                groups_rem = set([it[1:] for it in grps if it.startswith('-')])

                for grp in groups_add:
                    members = groups[grp]
                    indivs_add = indivs_add.union(members)

                for grp in groups_rem:
                    members = groups[grp]
                    indivs_rem = indivs_rem.union(members)

                friends = list(indivs_add - indivs_rem)

                for who in friends:
                    SOURCE = pathlib.Path(path)

                    SPATH, SFILE = str(SOURCE.parent.expanduser()), SOURCE.name
                    if SPATH.startswith(str(BASE)): SPATH = SPATH[len(str(BASE)):]
                    if SPATH.startswith(BASE._flavour.sep): SPATH = SPATH[1:]

                    DPATH = os.path.join(indiv[who], SPATH)
                    DESTINATION = os.path.join(DPATH, SFILE)

                    print(f'COPY: @{who}', SOURCE, '->', DESTINATION)
                    if not os.path.exists(DPATH):
                        os.makedirs(DPATH)

                    shutil.copyfile(SOURCE, DESTINATION)
            if IS_FILE:
                break

if __name__ == '__main__':
    main()
