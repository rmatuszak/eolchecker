from __future__ import annotations

import argparse
import os
import sys
from typing import Sequence

ACCEPTED_EOLS = ["lf","crlf","cr"]

def check_eol(filename: str, expected_eol: str) -> int:
    with open(filename, 'rb') as f:
        contents = f.read()

    not_expected=0
    lines_to_fix=[]
    if expected_eol in ACCEPTED_EOLS:
        for idx,line in enumerate(contents.splitlines(True)):
            if not line.endswith(expected_eol):
                not_expected += 1
                lines_to_fix.append(f"{filename} {idx}: {line}")
    else:
        raise "Error! Presented EOL is not in the list of available to parse EOLs! Exiting."

    if not_expected > 0:
        print(f"{filename} didn't pass check! Lines to fix:")
        print(lines_to_fix)
        return True
    else:
        print("All checks passed!")
        return False,

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
        res = check_eol(filename, args.eol)
        if res:
            hook_ret = -1
    return hook_ret

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))