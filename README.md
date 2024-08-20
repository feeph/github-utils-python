# github-utils-python

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-purple.json)](https://github.com/copier-org/copier)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Coverage Status](https://coveralls.io/repos/github/feeph/github-utils-python/badge.svg)](https://coveralls.io/github/feeph/github-utils-python)
[![pdm-managed](https://img.shields.io/endpoint?url=https%3A%2F%2Fcdn.jsdelivr.net%2Fgh%2Fpdm-project%2F.github%2Fbadge.json)](https://pdm-project.org)
[![tox](https://img.shields.io/badge/tox-ab79d2)](https://tox.wiki/)

various GitHub related utilities

## Purpose

This respository contains multiple tools, each tool is documented individually.

- [`update_github-secrets`](docs/update_github-secrets.md)

## Installation

It is recommended to use [pipx](https://pipx.pypa.io/stable/) to install
this package. Installation instructions for pipx can be found at
https://pipx.pypa.io/stable/installation/

This package is in development and has not been released on PyPI!
It must be installed from TestPyPI.

```
# install from TestPyPI
pipx install --index-url=https://test.pypi.org/simple/ feeph.github_utils
```

## GitHub Personal Access Token

The utilities in this repository require a Personal Access Token in order
to be allowed to talk to the GitHub API. The easiest way to acquire this
token is to install the [GitHub Command Line utilities](https://cli.github.com)
and use `gh auth login`.

## Bugs & Features

Please submit bugs and request features on the [issue tracker](https://github.com/feeph/github-utils-python/issues).

Contributions are always welcome.

## How to contribute

Please refer to the [Contribution guide](docs/CONTRIBUTING.md).
