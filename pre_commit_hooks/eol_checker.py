# from __future__ import annotations
# from typing import Sequence

# import argparse
# import subprocess
# import re

# CRLF = b'\r\n'
# LF = b'\n'
# CR = b'\r'
# ACCEPTED_EOLS = {'cr': CR, 'crlf': CRLF, 'lf': LF}

# def _get_eols_from_files(files: list) -> list:
#     """
#     Internal method used to list and process line endings using git listing command.
#     :param files: files passed to git listing
#     """
#     cmd = ["git","ls-files","--eol",','.join(files)]
#     eols = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="UTF-8")
#     return list(eols.stdout.split('\n'))[:-1]

# def parse_eols(files: list, expected_eol: str) -> list:
#     """
#     Created for intepreting results from _get_eols_from_files.
#     Returns either an empty list or list of files, which not passed the check.
#     :param files: files passed to _get_eols_from_files
#     :param expected_eol: end of line expected in files for current case
#     """
#     files_to_fix= []
#     eols = _get_eols_from_files(files)
#     pattern=re.compile("i\/(lf|crlf|mixed|none)")
#     for e in eols:
#         result = pattern.match(e)
#         if result is not None and result.group().split('/')[1] != expected_eol:
#             files_to_fix.append(e.split('\t')[1])
#     return files_to_fix

# def main(argv: Sequence[str] | None = None) -> int:
#     parser = argparse.ArgumentParser()
#     parser.add_argument('filenames', nargs='*', help='Filenames to check')
#     parser.add_argument(
#         '-e', '--eol',
#         choices=('crlf', 'lf','cr'),
#         default='lf',
#         help='Specifies the line ending to expect in files. Default is LF.',
#     )

#     args = parser.parse_args(argv)
#     print(f"files: {args.filenames}")
#     ftf = parse_eols(args.filenames, args.eol)
#     print(f"Files to fix: {ftf}")
#     hook_ret=0
#     if len(ftf) > 0:
#         print("Not all files passed EOL check. Please investigate below:")
#         for f in ftf:
#             print(f)
#         hook_ret = 1
#     else:
#         print("All files passed checks!")

#     return hook_ret

# if __name__ == "__main__":
#     raise SystemExit(main())


from __future__ import annotations

import argparse
from typing import Sequence

def check_line_expected_eol(filename: str, expected_eol: bytes) -> int:
    ret_val = 0
    with open(filename, 'rb') as file_obj:
        for line in file_obj:
            if expected_eol == b'\r\n' and line.endswith(expected_eol):
                continue
            elif expected_eol == b'\n' and line.endswith(b'\r\n'):
                ret_val = 1
                break
            elif expected_eol == b'\n' and line.endswith(expected_eol):
                continue
            else:
                ret_val = 1
                break
        file_obj.close()
        return ret_val


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    parser.add_argument(
        '-e', '--eol',
        choices=('crlf', 'lf'),
        default='lf',
        help='Specifies the line ending to expect in files. Default is LF.',
    )
    args = parser.parse_args(argv)

    retv, issues = 0, False

    for filename in args.filenames:
        # Read as binary so we can read byte-by-byte
        with open(filename, 'rb+') as file_obj:
            retv = check_line_expected_eol(file_obj, args.eol)
            if retv:
                print(f'{filename}: Incorrect line endings. Please investigate.')
                issues = 1
    return issues

if __name__ == '__main__':
    raise SystemExit(main())


