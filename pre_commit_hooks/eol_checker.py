from __future__ import annotations

import argparse
import os
import sys
from typing import Sequence

CRLF = b'\r\n'
LF = b'\n'
CR = b'\r'
ACCEPTED_EOLS = {'cr': CR, 'crlf': CRLF, 'lf': LF}

def check_eol(filename: str, expected_eol: str) -> bool:
    with open(filename, 'rb') as f:
        contents = f.read()

    not_expected=0
    lines_to_fix=[]
    if expected_eol in ACCEPTED_EOLS.keys():
        for idx,line in enumerate(contents.splitlines(True)):
            if not line.endswith(ACCEPTED_EOLS[expected_eol]):
                not_expected += 1
                lines_to_fix.append(f"{idx}: {line}")
    else:
        raise "Error! Presented EOL is not in the list of available to parse EOLs! Exiting."

    if not_expected > 0:
        return True, lines_to_fix
    else:
        return False, lines_to_fix

def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-e', '--eol',
        choices=('crlf', 'lf','cr'),
        default='lf',
        help='Specifies the line ending to expect in files. Default is LF.',
    )
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    hook_ret = 0
    files_to_check = {}
    for filename in args.filenames:
        res, lines = check_eol(filename, args.eol)
        if res:
            files_to_check.update({filename:lines})
            hook_ret = -1

    # all results printing should happen here, after main for loop
    if hook_ret != 0:
        print("Not all files passed check.")
        for f,l in files_to_check.items():
            print(f"File {f}: ")
            for e in l:
                print(e)
    else:
        print("All files passed!")
    return hook_ret

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))