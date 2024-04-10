from __future__ import annotations
from typing import Sequence

import argparse
import subprocess
import re

CRLF = b'\r\n'
LF = b'\n'
CR = b'\r'
ACCEPTED_EOLS = {'cr': CR, 'crlf': CRLF, 'lf': LF}

def _get_eols_from_files(files: str) -> str:
    """
    Internal method used to list and process line endings using git listing command.
    :param files: files passed to git listing
    """
    cmd = ["git","ls-files","--eol",','.join(files)]
    eols = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="UTF-8")
    return list(eols.stdout.split('\n'))

def _filter_extensions(eols: list, skip_extensions: list) -> list:
    """
    Filtering eols from _get_eols_from_files. Rmemoved from list all files with unwanted extension.
    :param eols: eols passed from _get_eols_from_files
    :param skip_extensions: extensions to be exluded from list
    """
    filtered=[]
    for e in eols:
        extension=e.split('\t')[1].split('.')
        if len(extension) > 1 and extension[1] in skip_extensions:
            continue
        else:
            filtered.append(e)
    return filtered


def parse_eols(files: str, expected_eol: str, skip_extensions: str) -> None:
    """
    Created for intepreting results from _get_eols_from_files.
    Returns either an empty list or list of files, which not passed the check.
    :param files: files passed to _get_eols_from_files
    :param expected_eol: end of line expected in files for current case
    """
    files_to_fix= []
    eols = _get_eols_from_files(files)
    filtered_eols = _filter_extensions(eols, skip_extensions)
    pattern=re.compile("i\/(lf|crlf|mixed|none)")
    for e in filtered_eols:
        result = pattern.match(e)
        if result is not None and result.group().split('/')[1] != expected_eol:
            files_to_fix.append(e.split('\t')[1])
    return files_to_fix

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-e', '--eol',
        choices=('crlf', 'lf','cr'),
        default='lf',
        help='Specifies the line ending to expect in files. Default is LF.',
    )
    parser.add_argument("-se","--skip_extensions", nargs='*', help="File extensions to exlude during the check, separated with comma")
    parser.add_argument('filenames', nargs='*', default=[], help='Filenames to check')
    args = parser.parse_args(argv)
    ftf = parse_eols(args.filenames, args.eol, args.skip_extensions)
    hook_ret=0
    if len(ftf) > 0:
        print("Not all files passed EOL check. Please investigate below:")
        for f in ftf:
            print(f)
        hook_ret = 1
    else:
        print("All files passed checks!")

    return hook_ret

if __name__ == "__main__":
    raise SystemExit(main())