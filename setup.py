from setuptools import find_packages
from setuptools import setup

setup(
    name="pre-commit-hooks",
    description="Example pre-commit library used in PIDT",
    url="https://github.com/rmatuszak/eolchecker",
    author="Rafal Matuszak",
    author_email="rafal.matuszak@intel.com",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: PyPy"
    ],
    packages=find_packages("."),
    entry_points={
        "console_scripts": [
            "eol-checker = pre_commit_hooks.eol_checker:main"
        ],
    },
)
