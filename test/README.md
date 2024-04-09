# eolchecker - manual tests or eolcherker hook (pre-commit)

## test_eols.py

Containt following method for manual testing - generating files with diffetent line endings.

1. ```generate_mixed_eol_file``` - generates a ten-line file with mixed line endings, named ```mixed_eols```
2. ```generate_exact_eols``` - generates a ten-line file with specified line ending. Arguments: eol - requested end of line.
3. ```view_eol_file``` - views content of file, generate by above methods. Arguments: filename - file to read from.

## Usage

Command:

```python test_eols.py```
