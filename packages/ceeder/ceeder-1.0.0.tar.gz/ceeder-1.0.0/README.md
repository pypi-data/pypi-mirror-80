# ceeder

<a href="https://github.com/qntfy/ceeder/actions"><img alt="Actions Status" src="https://github.com/qntfy/ceeder/workflows/Tests/badge.svg"></a>
[![Documentation](https://readthedocs.org/projects/ceeder/badge/?version=latest)](https://ceeder.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


`ceeder` is a library intended to make working with
[CDRs](https://github.com/WorldModelers/Document-Schema)
and CDR-based analytics simpler.

## Documentation

Documentation is available on
[readthedocs.io](https://ceeder.readthedocs.io/en/latest/).

## Install as a library

`ceeder` is available on [PyPI](https://pypi.org/project/ceeder/).

``` shell
python -m pip install ceeder
```

## Build

[poetry](https://python-poetry.org/) is required to use the project.

Clone the project, then run:

```shell
poetry build
```

## Testing

[tox](https://tox.readthedocs.io/en/latest/index.html) is used for testing the
project.

``` shell
python -m pip install --upgrade tox
tox
```

## Usage

See [the examples](./examples) directory for usage information
in your analytic.
