# Sonnen Coding Challenge

## __Sonnen The Supermarket Receipt Refactoring Kata__

## Prerequisites 

### Software Installation

* [Python 3.9+](https://www.python.org/) Python.
* [Poetry](https://python-poetry.org/) for Python package and environment management.

## System Dependencies

- Make sure your system is up-to-date.

```bash
$ sudo apt-get install libffi-dev
$ sudo apt-get install libpq-dev python-dev libssl-dev
```

## Python Dependencies

- Installing Python Packages

```bash
$ poetry shell
$ poetry install
```

## Testing

```bash
$ poetry run pytest
```

## Type checking

```bash
$ poetry run mypy .
```

## HTML Receipt

There is an [example](/example_receipt.py) on how to render a HTML Receipt

```bash
$ poetry run python example_receipt.py
```
