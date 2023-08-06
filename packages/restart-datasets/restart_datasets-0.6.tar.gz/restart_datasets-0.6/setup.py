import io
import os
import re

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(path, encoding="utf-8"):
    path = os.path.join(here, path)
    with io.open(path, encoding=encoding) as fp:
        return fp.read()


def version(path):
    """Obtain the packge version from a python file e.g. pkg/__init__.py
    See <https://packaging.python.org/en/latest/single_source_version.html>.
    """
    version_file = read(path)
    version_match = re.search(
        r"""^__version__ = ['"]([^'"]*)['"]""", version_file, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="restart_datasets",
    version=version("restart_datasets/__init__.py"),
    description="Python package for offline access to restart datasets",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Restart Partners",
    author_email="info@restart.us",
    maintainer="Lucas Hahn",
    maintainer_email="lucas@restart.us",
    url="http://github.com/restartus/restart_datasets",
    install_requires=["pandas"],
    python_requires=">=3.8",
    tests_require=["pytest"],
    packages=find_packages(exclude=["tools"]),
    package_data={
        "restart_datasets": [
            "datasets.json",
            "dataset_info.json",
            "local_datasets.json",
            os.path.join("_data", "*.json"),
            os.path.join("_data", "*.csv"),
            os.path.join("_data", "*.tsv"),
            os.path.join("_data", "*.xlsx"),
            os.path.join("_data", "*.xls")
        ]
    },
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.8",
    ],
)
