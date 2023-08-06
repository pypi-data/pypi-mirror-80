#!/usr/bin/python3
import json, re, os, argparse, pathlib

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', help='Source folder to traverse.')
    parser.add_argument('-g', '--groups', help='Groups definitions json file.')
    parser.add_argument('-b', '--base', help='Base directory of source wiki (to trim paths to).')
    parser.add_argument('-d', '--delimiters', help='Default is, "{:,|,:}", pass comma-separated delimiters.')
    args = parser.parse_args()

    CWD = pathlib.Path(os.getcwd())
    SOURCE = pathlib.Path(args.source)
    GROUPS = pathlib.Path(args.groups)
    BASE = pathlib.Path(args.base or CWD)
    DELIMITERS = args.delimiters or '{:,|,:}'

    for dir_name, subdir_list, file_list in os.walk(SOURCE):
        dir_path = dir_name.split('/')[1:]

        for fname in file_list:
            path = os.path.join(dir_name, fname)
            os.system('notesplit -s "%s" -g "%s" -b "%s" -d "%s"' % (path, str(GROUPS), str(BASE), DELIMITERS))

if __name__ == '__main__':
    main()
