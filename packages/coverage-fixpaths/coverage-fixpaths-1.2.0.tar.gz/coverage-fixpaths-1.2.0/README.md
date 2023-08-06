# coverage-fixpaths

A small CLI tool that automatically fixes paths in Cobertura coverage and JUnit test reports.

## Usage

```
$ coverage-fixpaths --source /path/to/source/files --type coverage coverage.xml
$ coverage-fixpaths --source /path/to/source/files --type junit report.xml
```

This tries to match the filenames in `coverage.xml` to the actual files in `/path/to/source/files`.
Any common prefix in the coverage report is replaced with a subdirectory of `/path/to/source/files`
that best matches the file structure in `coverage.xml`. Files that do not exist in the source directory
are removed from the coverage report.

The option `--source` defaults to `.` (i.e. the current working directory).


## Installation

```
pip install coverage-fixpaths
```
or
```
conda install -c conda-forge coverage-fixpaths
```
