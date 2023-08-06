#!/usr/bin/python3
import json, os, re, argparse, pathlib
from collections import defaultdict

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', help='Source text file to parse.')
    parser.add_argument('-g', '--groups', help='Groups definitions json file.')
    parser.add_argument('-b', '--base', help='Base directory of source wiki (to trim paths to).')
    parser.add_argument('-d', '--delimiters', help='Default is, "{:,|,:}", pass comma-separated delimiters.')
    args = parser.parse_args()

    CWD = pathlib.Path(os.getcwd())
    SOURCE = pathlib.Path(args.source)     # e.g., 'page.txt'
    GROUPS = pathlib.Path(args.groups)     # e.g., 'groups.json'
    BASE = pathlib.Path(args.base or CWD)  # e.g., '~/.wiki'
    DELIMITERS = args.delimiters or '{:,|,:}'
    delims = DELIMITERS.split(',')

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

    for k, g in groups.items(): groups[k] = frozenset(g)

    pattern = '(%s)' % '|'.join([
        '|' in delim and re.escape(delim) or delim
        for delim in delims])

    stack = []
    cur = stack
    for tok in re.compile(pattern).split(open(SOURCE, 'r').read()):
        if tok == delims[0]:   new = []; cur += [new]; stack += [cur]; cur = new
        elif tok == delims[-1]: cur = stack.pop()
        else:             cur += [tok]

    out = defaultdict(str)
    def process(stack, group):
        if len(stack) >= 2 and stack[1] == delims[1]:
            if stack[0][0] == '-':
                group = group - groups.get(stack[0][1:], set([stack[0][1:]]))
            else:
                group = group | groups.get(stack[0], set([stack[0]]))
            stack = stack[2:]
        for foo in stack:
            if type(foo) is list:
                process(foo, group)
            else:
                for who in group: out[who] += foo
    process(stack, frozenset())

    SPATH, SFILE = str(SOURCE.parent.expanduser()), SOURCE.name
    if SPATH.startswith(str(BASE)): SPATH = SPATH[len(str(BASE)):]
    if SPATH.startswith(BASE._flavour.sep): SPATH = SPATH[1:]

    for who, data in out.items():
        if who in indiv:
            path = os.path.join(indiv[who], SPATH)

            if data:
                if not os.path.exists(path):
                    os.makedirs(path)

                open(os.path.join(path, SFILE), 'w').write(data)


if __name__ == '__main__':
    main()
