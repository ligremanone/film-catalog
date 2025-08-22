# FastAPI Film Catalog

[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white&style=for-the-badge)](https://www.python.org/)
[![uv](https://img.shields.io/badge/dependencies-uv-8A2BE2?logo=lightning&logoColor=white&style=for-the-badge)](https://github.com/astral-sh/uv)
[![Black](https://img.shields.io/badge/code%20style-black-000000?logo=python&logoColor=white&style=for-the-badge)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/linter-ruff-red?logo=ruff&logoColor=white&style=for-the-badge)](https://github.com/astral-sh/ruff)
[![Mypy](https://img.shields.io/badge/type%20checker-mypy-2E5DFF?logo=python&logoColor=white&style=for-the-badge)](https://github.com/python/mypy)

[![codecov](https://codecov.io/gh/ligremanone/film-catalog/branch/main/graph/badge.svg)](https://codecov.io/gh/ligremanone/film-catalog)

## Development

### Setup

Right click `film-catalog` -> Mark Directory as -> Sources Root

### Install dependencies

Install all packages:

```shell
uv sync
```

### Configure pre-commit

Install pre-commit hook:

```shell
pre-commit install
```

### Run

Go to workdir:

```shell
cd film-catalog
```

Run dev server:

```shell
fastapi dev
```

## Snippets

```shell
python -c 'import secrets;print(secrets.token_urlsafe(16))'
```
