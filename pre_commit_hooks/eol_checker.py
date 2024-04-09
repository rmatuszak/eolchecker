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
    cmd = ["git","ls-files","--eol",','.join(files)]
    eols = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="UTF-8")
    return list(eols.stdout.split('\n'))

def parse_eols(files: str, expected_eol: str) -> None:
    files_to_fix= []
    eols = _get_eols_from_files(files)
    pattern=re.compile("i\/(lf|crlf|mixed|none)")
    for e in eols:
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
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    print(f"Checking files: {args.filenames}")

    ftf = parse_eols(args.filenames, args.eol)

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