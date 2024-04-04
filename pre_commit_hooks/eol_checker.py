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
                lines_to_fix.append(f"{filename} {idx}: {line}")
    else:
        raise "Error! Presented EOL is not in the list of available to parse EOLs! Exiting."

    if not_expected > 0:
        print(f"{filename} didn't pass check! Lines to fix:")
        # print(lines_to_fix)
        return True, lines_to_fix
    else:
        # print("All checks passed!")
        return False, lines_to_fix

def main(argv: Sequence[str] | None = None) -> int:
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
    for filename in args.filenames:
        res, lines = check_eol(filename, args.eol)
        if res:
            hook_ret = -1
            print(f"Not all files passed the check! Please refer to below lines in {filename}:")
            for line in lines:
                print(line)
        else:
            print("All files passed!")
    return hook_ret

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))