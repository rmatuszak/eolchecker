# eolchecker - hook for pre-commit tool

Repository contains code for hook, which can be used in ``pre-commit`` tool.

It checks end of lines in files, that are passed to the main method of the hook. To be parsed properly, files must be in staged phase, to be taken under ``pre-commit`` analyze.

Below hook uses ``git ls-files`` to get the list of line endings and then process them and compares to expected end of line (provided by the user).
Check passes, when all file match expected line ending. If not, it returns a list of files to fix and fails the check.

