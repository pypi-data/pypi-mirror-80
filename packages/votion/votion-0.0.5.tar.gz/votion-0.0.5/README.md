# votion

[![Build Status](https://travis-ci.org/weastur/votion.svg?branch=master)](https://travis-ci.org/weastur/votion)
[![codecov](https://codecov.io/gh/weastur/votion/branch/master/graph/badge.svg)](https://codecov.io/gh/weastur/votion)
[![Documentation Status](https://readthedocs.org/projects/votion/badge/?version=latest)](https://votion.readthedocs.io/en/latest/?badge=latest)
[![PyPi version](https://img.shields.io/pypi/v/votion.svg)](https://pypi.org/project/votion/)
[![Python versions](https://img.shields.io/pypi/pyversions/votion)](https://pypi.org/project/votion/)
[![black-formatter](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/) [![Join the chat at https://gitter.im/votion-build-tool/community](https://badges.gitter.im/votion-build-tool/community.svg)](https://gitter.im/votion-build-tool/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

---

Docker image build tool

## Features

## Documentation

For full documentation please go [here](https://votion.readthedocs.io/en/latest/).

## Instalation

```bash
pip install votion
```

## Development

For development first you need [poetry](https://github.com/python-poetry/poetry) and python 3.7+

```bash
git clone git@github.com:weastur/votion.git
cd votion
poetry install
```

This will install dependencies and all needed packages for development, like pytest, wemake-python-styleguide, mypy, black.

Highly recommend to install [overcommit](https://github.com/sds/overcommit).

```bash
overcommit -i
```

After, all commits will be checked on set of rules when you create them. Additionally
on CI executed flake8, mypy, black, and unit tests. You can easily integrate same checks into your editor.
This checks aren't executed with hooks, because otherwise you'll be able to commit only inside virtualenv.

## Bugs/Requests

## Changelog

## Roadmap

## License

Distributed under the terms of the [MIT](https://github.com/weastur/votion/blob/master/LICENSE) license, pytest is free and open source software.
