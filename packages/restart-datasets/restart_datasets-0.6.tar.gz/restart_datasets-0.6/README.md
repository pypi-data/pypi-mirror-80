# Restart Datasets

A Python package for offline access to data needed to run [restart](https://github.com/restartus/restart)

## Installation
``vega_datasets`` is compatible with Python 3.8 or newer. Install with:

```
$ pip install restart_datasets
```

## Usage

The main object in this library is ``data``:

```python
>>> from restart_datasets import data
```

To access the BLS data for, say, the state of California:

```python
df = data.California()
```

This will return a dataframe containing employment statistics for the state of
California.

## Available Datasets

To list all the available datsets, use ``list_datasets``:

```python
datasets = data.list_datasets()
```

## Dataset Information

If you want more information about any dataset, you can use the ``description`` property:

```python
data.California.description
```
