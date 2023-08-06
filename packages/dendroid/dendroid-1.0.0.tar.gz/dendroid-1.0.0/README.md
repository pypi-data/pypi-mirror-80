dendroid
========

[![](https://travis-ci.com/lycantropos/dendroid.svg?branch=master)](https://travis-ci.com/lycantropos/dendroid "Travis CI")
[![](https://dev.azure.com/lycantropos/dendroid/_apis/build/status/lycantropos.dendroid?branchName=master)](https://dev.azure.com/lycantropos/dendroid/_build/latest?definitionId=14&branchName=master "Azure Pipelines")
[![](https://codecov.io/gh/lycantropos/dendroid/branch/master/graph/badge.svg)](https://codecov.io/gh/lycantropos/dendroid "Codecov")
[![](https://img.shields.io/github/license/lycantropos/dendroid.svg)](https://github.com/lycantropos/dendroid/blob/master/LICENSE "License")
[![](https://badge.fury.io/py/dendroid.svg)](https://badge.fury.io/py/dendroid "PyPI")

In what follows
- `python` is an alias for `python3.5` or any later
version (`python3.6` and so on),
- `pypy` is an alias for `pypy3.5` or any later
version (`pypy3.6` and so on).

Installation
------------

Install the latest `pip` & `setuptools` packages versions:
- with `CPython`
  ```bash
  python -m pip install --upgrade pip setuptools
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --upgrade pip setuptools
  ```

### User

Download and install the latest stable version from `PyPI` repository:
- with `CPython`
  ```bash
  python -m pip install --upgrade dendroid
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --upgrade dendroid
  ```

### Developer

Download the latest version from `GitHub` repository
```bash
git clone https://github.com/lycantropos/dendroid.git
cd dendroid
```

Install dependencies:
- with `CPython`
  ```bash
  python -m pip install --force-reinstall -r requirements.txt
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --force-reinstall -r requirements.txt
  ```

Install:
- with `CPython`
  ```bash
  python setup.py install
  ```
- with `PyPy`
  ```bash
  pypy setup.py install
  ```

Usage
-----

```python
>>> from dendroid import avl, red_black, splay
>>> from random import sample
>>> min_value, max_value = -100, 100
>>> size = (max_value - min_value) // 2
>>> values = sample(range(min_value, max_value), size)
>>> avl_set, red_black_set, splay_set = (avl.set_(*values),
...                                      red_black.set_(*values),
...                                      splay.set_(*values))
>>> len(avl_set) == len(red_black_set) == len(splay_set) == size
True
>>> max_value not in avl_set and max_value not in red_black_set and max_value not in splay_set
True
>>> list(avl_set) == list(red_black_set) == list(splay_set) == sorted(values)
True
>>> avl_set.add(max_value)
>>> red_black_set.add(max_value)
>>> splay_set.add(max_value)
>>> len(avl_set) == len(red_black_set) == len(splay_set) == size + 1
True
>>> max_value in avl_set and max_value in red_black_set and max_value in splay_set
True
>>> list(avl_set) == list(red_black_set) == list(splay_set) == sorted(values) + [max_value]
True
>>> prev_max_value = max(values)
>>> avl_set.prev(max_value) == red_black_set.prev(max_value) == splay_set.prev(max_value) == prev_max_value
True
>>> avl_set.next(prev_max_value) == red_black_set.next(prev_max_value) == splay_set.next(prev_max_value) == max_value
True
>>> avl_set.remove(max_value)
>>> red_black_set.remove(max_value)
>>> splay_set.remove(max_value)
>>> len(avl_set) == len(red_black_set) == len(splay_set) == len(values)
True
>>> max_value not in avl_set and max_value not in red_black_set and max_value not in splay_set
True
>>> list(avl_set) == list(red_black_set) == list(splay_set) == sorted(values)
True
>>> avl_set.max() == red_black_set.max() == splay_set.max() == max(values)
True
>>> avl_set.min() == red_black_set.min() == splay_set.min() == min(values)
True
>>> avl_set.max() == red_black_set.max() == splay_set.max() == max(values)
True
>>> avl_set.min() == red_black_set.min() == splay_set.min() == min(values)
True
>>> avl_set.add(max_value)
>>> red_black_set.add(max_value)
>>> splay_set.add(max_value)
>>> avl_set.popmax() == red_black_set.popmax() == splay_set.popmax() == max_value
True
>>> avl_set.add(min_value)
>>> red_black_set.add(min_value)
>>> splay_set.add(min_value)
>>> avl_set.popmin() == red_black_set.popmin() == splay_set.popmin() == min_value
True
>>> min_key, max_key = min_value, max_value
>>> keys = sample(range(min_key, max_key), size)
>>> items = list(zip(keys, values))
>>> avl_map, red_black_map, splay_map = (avl.map_(*items),
...                                      red_black.map_(*items),
...                                      splay.map_(*items))
>>> len(avl_map) == len(red_black_map) == len(splay_map) == size
True
>>> max_key not in avl_map and max_key not in red_black_map and max_key not in splay_map
True
>>> list(avl_map) == list(red_black_map) == list(splay_map) == sorted(keys)
True
>>> avl_map[max_key] = red_black_map[max_key] = splay_map[max_key] = max_value
>>> len(avl_map) == len(red_black_map) == len(splay_map) == size + 1
True
>>> max_key in avl_map and max_key in red_black_map and max_key in splay_map
True
>>> avl_map[max_key] == red_black_map[max_key] == splay_map[max_key] == max_value
True
>>> list(avl_map) == list(red_black_map) == list(splay_map) == sorted(keys) + [max_key]
True
>>> prev_max_key, prev_max_value = items[max(range(size), key=keys.__getitem__)]
>>> avl_map.prev(max_key) == red_black_map.prev(max_key) == splay_map.prev(max_key) == prev_max_value
True
>>> avl_map.next(prev_max_key) == red_black_map.next(prev_max_key) == splay_map.next(prev_max_key) == max_value
True
>>> del avl_map[max_key], red_black_map[max_key], splay_map[max_key]
>>> len(avl_map) == len(red_black_map) == len(splay_map) == size
True
>>> max_key not in avl_map and max_key not in red_black_map and max_key not in splay_map
True
>>> list(avl_map) == list(red_black_map) == list(splay_map) == sorted(keys)
True
>>> avl_map.max() == red_black_map.max() == splay_map.max() == values[max(range(size), key=keys.__getitem__)]
True
>>> avl_map.min() == red_black_map.min() == splay_map.min() == values[min(range(size), key=keys.__getitem__)]
True
>>> avl_map[max_key] = red_black_map[max_key] = splay_map[max_key] = max_value
>>> avl_map.popmax() == red_black_map.popmax() == splay_map.popmax() == max_value
True
>>> avl_map[min_key] = red_black_map[min_key] = splay_map[min_key] = min_value
>>> avl_map.popmin() == red_black_map.popmin() == splay_map.popmin() == min_value
True

```

Development
-----------

### Bumping version

#### Preparation

Install
[bump2version](https://github.com/c4urself/bump2version#installation).

#### Pre-release

Choose which version number category to bump following [semver
specification](http://semver.org/).

Test bumping version
```bash
bump2version --dry-run --verbose $CATEGORY
```

where `$CATEGORY` is the target version number category name, possible
values are `patch`/`minor`/`major`.

Bump version
```bash
bump2version --verbose $CATEGORY
```

This will set version to `major.minor.patch-alpha`. 

#### Release

Test bumping version
```bash
bump2version --dry-run --verbose release
```

Bump version
```bash
bump2version --verbose release
```

This will set version to `major.minor.patch`.

### Running tests

Install dependencies:
- with `CPython`
  ```bash
  python -m pip install --force-reinstall -r requirements-tests.txt
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --force-reinstall -r requirements-tests.txt
  ```

Plain
```bash
pytest
```

Inside `Docker` container:
- with `CPython`
  ```bash
  docker-compose --file docker-compose.cpython.yml up
  ```
- with `PyPy`
  ```bash
  docker-compose --file docker-compose.pypy.yml up
  ```

`Bash` script (e.g. can be used in `Git` hooks):
- with `CPython`
  ```bash
  ./run-tests.sh
  ```
  or
  ```bash
  ./run-tests.sh cpython
  ```

- with `PyPy`
  ```bash
  ./run-tests.sh pypy
  ```

`PowerShell` script (e.g. can be used in `Git` hooks):
- with `CPython`
  ```powershell
  .\run-tests.ps1
  ```
  or
  ```powershell
  .\run-tests.ps1 cpython
  ```
- with `PyPy`
  ```powershell
  .\run-tests.ps1 pypy
  ```
