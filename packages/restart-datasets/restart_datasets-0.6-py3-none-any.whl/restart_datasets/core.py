from io import BytesIO
import os
import json
import pkgutil
import textwrap
from typing import Any, Dict, Iterable, List
from urllib.request import urlopen
import pandas as pd

# This is the tag in http://github.com/vega/vega-datasets from
# which the datasets in this repository are sourced.
SOURCE_TAG = "v1.29.0"


def _load_dataset_info() -> Dict[str, Dict[str, Any]]:
    """This loads dataset info from three package files:

    restart_datasets/datasets.json
    restart_datasets/dataset_info.json
    restart_datasets/local_datasets.json

    It returns a dictionary with dataset information.
    """

    def load_json(path: str) -> Dict[str, Any]:
        raw = pkgutil.get_data("restart_datasets", path)
        if raw is None:
            raise ValueError(
                "Cannot locate package path restart_datasets:{}".format(path)
            )
        return json.loads(raw.decode())

    info = load_json("datasets.json")
    descriptions = load_json("dataset_info.json")
    local_datasets = load_json("local_datasets.json")

    for name in info:
        info[name]["is_local"] = name in local_datasets
    for name in descriptions:
        info[name].update(descriptions[name])

    return info


class Dataset(object):
    """Class to load a particular dataset by name"""

    _instance_doc = """Loader for the {name} dataset.

    {data_description}

    {bundle_info}
    Dataset source: {url}

    Usage
    -----

        >>> from vega_datasets import data
        >>> {methodname} = data.{methodname}()
        >>> type({methodname})
        {return_type}

    Equivalently, you can use

        >>> {methodname} = data('{name}')

    To get the raw dataset rather than the dataframe, use

        >>> data_bytes = data.{methodname}.raw()
        >>> type(data_bytes)
        bytes

    To find the dataset url, use

        >>> data.{methodname}.url
        '{url}'
    {additional_docs}
    Attributes
    ----------
    filename : string
        The filename in which the dataset is stored
    url : string
        The full URL of the dataset at http://vega.github.io
    format : string
        The format of the dataset: usually one of {{'csv', 'tsv', 'json'}}
    pkg_filename : string
        The path to the local dataset within the vega_datasets package
    is_local : bool
        True if the dataset is available locally in the package
    filepath : string
        If is_local is True, the local file path to the dataset.

    {reference_info}
    """
    _additional_docs = ""
    _reference_info = """
    For information on this dataset, see https://github.com/vega/vega-datasets/
    """
    base_url = "https://cdn.jsdelivr.net/npm/vega-datasets@" + SOURCE_TAG + "/data/"
    _dataset_info = _load_dataset_info()
    _pd_read_kwds = {}  # type: Dict[str, Any]
    _return_type = pd.DataFrame

    @classmethod
    def init(cls, name: str) -> "Dataset":
        """Return an instance of this class or an appropriate subclass"""
        clsdict = {
            subcls.name: subcls
            for subcls in cls.__subclasses__()
            if hasattr(subcls, "name") or
            hasattr(subcls, "state")
        }
        return clsdict.get(name, cls)(name)

    def __init__(self, name: str):
        info = self._infodict(name)
        self.name = name
        self.methodname = name.replace("-", "_")
        self.filename = info["filename"]
        self.url = self.base_url + info["filename"]
        self.format = info["format"]
        self.pkg_filename = "_data/" + self.filename
        self.is_local = info["is_local"]
        self.description = info.get("description", None)
        self.references = info.get("references", None)
        self.__doc__ = self._make_docstring()

    def _make_docstring(self) -> str:
        info = self._infodict(self.name)

        # construct, indent, and line-wrap dataset description
        description = info.get("description", "")
        if not description:
            description = (
                "This dataset is described at " "https://github.com/vega/vega-datasets/"
            )
        wrapper = textwrap.TextWrapper(
            width=70, initial_indent="", subsequent_indent=4 * " "
        )
        description = "\n".join(wrapper.wrap(description))

        # construct, indent, and join references
        reflist = info.get("references", [])  # type: Iterable[str]
        reflist = (".. [{0}] ".format(i + 1) + ref for i, ref in enumerate(reflist))
        wrapper = textwrap.TextWrapper(
            width=70, initial_indent=4 * " ", subsequent_indent=7 * " "
        )
        reflist = ("\n".join(wrapper.wrap(ref)) for ref in reflist)
        references = "\n\n".join(reflist)  # type: str
        if references.strip():
            references = "References\n    ----------\n" + references

        # add information about bundling of data
        if self.is_local:
            bundle_info = (
                "This dataset is bundled with vega_datasets; "
                "it can be loaded without web access."
            )
        else:
            bundle_info = (
                "This dataset is not bundled with vega_datasets; "
                "it requires web access to load."
            )

        return self._instance_doc.format(
            additional_docs=self._additional_docs,
            data_description=description,
            reference_info=references,
            bundle_info=bundle_info,
            return_type=self._return_type,
            **self.__dict__
        )

    @classmethod
    def list_datasets(cls) -> List[str]:
        """Return a list of names of available datasets"""
        return sorted(cls._dataset_info.keys())

    @classmethod
    def list_local_datasets(cls) -> List[str]:
        return sorted(
            name for name, info in cls._dataset_info.items() if info["is_local"]
        )

    @classmethod
    def _infodict(cls, name: str) -> Dict[str, str]:
        """load the info dictionary for the given name"""
        info = cls._dataset_info.get(name, None)
        if info is None:
            raise ValueError(
                "No such dataset {0} exists, "
                "use list_datasets() to get a list "
                "of available datasets.".format(name)
            )
        return info

    def raw(self, use_local: bool = True) -> bytes:
        """Load the raw dataset from remote URL or local file

        Parameters
        ----------
        use_local : boolean
            If True (default), then attempt to load the dataset locally. If
            False or if the dataset is not available locally, then load the
            data from an external URL.
        """
        if use_local and self.is_local:
            out = pkgutil.get_data("restart_datasets", self.pkg_filename)
            if out is not None:
                return out
            raise ValueError(
                "Cannot locate package path restart_datasets:{}".format(
                    self.pkg_filename
                )
            )
        else:
            return urlopen(self.url).read()

    def __call__(self, use_local: bool = True, **kwargs) -> pd.DataFrame:
        """Load and parse the dataset from remote URL or local file

        Parameters
        ----------
        use_local : boolean
            If True (default), then attempt to load the dataset locally. If
            False or if the dataset is not available locally, then load the
            data from an external URL.
        **kwargs :
            additional keyword arguments are passed to data parser (usually
            pd.read_csv or pd.read_json, depending on the format of the data
            source)

        Returns
        -------
        data :
            parsed data
        """
        datasource = BytesIO(self.raw(use_local=use_local))

        kwds = self._pd_read_kwds.copy()
        kwds.update(kwargs)

        if self.format == "json":
            return pd.read_json(datasource, **kwds)
        elif self.format == "csv":
            return pd.read_csv(datasource, **kwds)
        elif self.format == "tsv":
            kwds.setdefault("sep", "\t")
            return pd.read_csv(datasource, **kwds)
        elif self.format == "xls" or self.format == "xlsx":
            return pd.read_excel(datasource, **kwds)
        else:
            raise ValueError(
                "Unrecognized file format: {0}. "
                "Valid options are ['json', 'csv', 'xlsx', 'xls', 'tsv']."
                "".format(self.format)
            )

    @property
    def filepath(self) -> str:
        if not self.is_local:
            raise ValueError("filepath is only valid for local datasets")
        else:
            return os.path.abspath(
                os.path.join(os.path.dirname(__file__), "_data", self.filename)
            )


class Census(Dataset):
    name = "co-est2019-alldata"
    _pd_read_kwds = {"encoding": "ISO-8859-1"}

class BLS(Dataset):
    name = "all_data_M_2019.xlsx"
    _pd_read_kwds = {}

class FipsList(Dataset):
    name = "list1_2020.xls"
    _pd_read_kwds = {}

class CovidSurge(Dataset):
    name = "covid-surge-who.xlsx"
    _pd_read_kwds = {}

class Georgia(Dataset):
  name = 'Georgia.csv'
  _pd_read_kwds = {}

class NorthCarolina(Dataset):
  name = 'NorthCarolina.csv'
  _pd_read_kwds = {}

class Wyoming(Dataset):
  name = 'Wyoming.csv'
  _pd_read_kwds = {}

class NewHampshire(Dataset):
  name = 'NewHampshire.csv'
  _pd_read_kwds = {}

class Wisconsin(Dataset):
  name = 'Wisconsin.csv'
  _pd_read_kwds = {}

class Minnesota(Dataset):
  name = 'Minnesota.csv'
  _pd_read_kwds = {}

class Maryland(Dataset):
  name = 'Maryland.csv'
  _pd_read_kwds = {}

class Pennsylvania(Dataset):
  name = 'Pennsylvania.csv'
  _pd_read_kwds = {}

class Texas(Dataset):
  name = 'Texas.csv'
  _pd_read_kwds = {}

class Florida(Dataset):
  name = 'Florida.csv'
  _pd_read_kwds = {}

class Michigan(Dataset):
  name = 'Michigan.csv'
  _pd_read_kwds = {}

class Hawaii(Dataset):
  name = 'Hawaii.csv'
  _pd_read_kwds = {}

class Tennessee(Dataset):
  name = 'Tennessee.csv'
  _pd_read_kwds = {}

class DistrictOfColumbia(Dataset):
  name = 'DistrictOfColumbia.csv'
  _pd_read_kwds = {}

class Arkansas(Dataset):
  name = 'Arkansas.csv'
  _pd_read_kwds = {}

class Ohio(Dataset):
  name = 'Ohio.csv'
  _pd_read_kwds = {}

class Nebraska(Dataset):
  name = 'Nebraska.csv'
  _pd_read_kwds = {}

class Montana(Dataset):
  name = 'Montana.csv'
  _pd_read_kwds = {}

class Indiana(Dataset):
  name = 'Indiana.csv'
  _pd_read_kwds = {}

class SouthDakota(Dataset):
  name = 'SouthDakota.csv'
  _pd_read_kwds = {}

class Mississippi(Dataset):
  name = 'Mississippi.csv'
  _pd_read_kwds = {}

class Counties(Dataset):
  name = 'counties.csv'
  _pd_read_kwds = {}

class Connecticut(Dataset):
  name = 'Connecticut.csv'
  _pd_read_kwds = {}

class Oklahoma(Dataset):
  name = 'Oklahoma.csv'
  _pd_read_kwds = {}

class Colorado(Dataset):
  name = 'Colorado.csv'
  _pd_read_kwds = {}

class Maine(Dataset):
  name = 'Maine.csv'
  _pd_read_kwds = {}

class SouthCarolina(Dataset):
  name = 'SouthCarolina.csv'
  _pd_read_kwds = {}

class list1_2020(Dataset):
  name = 'list1_2020.xls'
  _pd_read_kwds = {}

class NorthDakota(Dataset):
  name = 'NorthDakota.csv'
  _pd_read_kwds = {}

class Louisiana(Dataset):
  name = 'Louisiana.csv'
  _pd_read_kwds = {}

class Utah(Dataset):
  name = 'Utah.csv'
  _pd_read_kwds = {}

class Virginia(Dataset):
  name = 'Virginia.csv'
  _pd_read_kwds = {}

class NewYork(Dataset):
  name = 'NewYork.csv'
  _pd_read_kwds = {}

class NewMexico(Dataset):
  name = 'NewMexico.csv'
  _pd_read_kwds = {}

class Delaware(Dataset):
  name = 'Delaware.csv'
  _pd_read_kwds = {}

class Kentucky(Dataset):
  name = 'Kentucky.csv'
  _pd_read_kwds = {}

class Massachusetts(Dataset):
  name = 'Massachusetts.csv'
  _pd_read_kwds = {}

class Alabama(Dataset):
  name = 'Alabama.csv'
  _pd_read_kwds = {}

class Arizona(Dataset):
  name = 'Arizona.csv'
  _pd_read_kwds = {}

class California(Dataset):
  name = 'California.csv'
  _pd_read_kwds = {}

class Nevada(Dataset):
  name = 'Nevada.csv'
  _pd_read_kwds = {}

class Alaska(Dataset):
  name = 'Alaska.csv'
  _pd_read_kwds = {}

class Illinois(Dataset):
  name = 'Illinois.csv'
  _pd_read_kwds = {}

class Idaho(Dataset):
  name = 'Idaho.csv'
  _pd_read_kwds = {}

class Oregon(Dataset):
  name = 'Oregon.csv'
  _pd_read_kwds = {}

class Iowa(Dataset):
  name = 'Iowa.csv'
  _pd_read_kwds = {}

class Vermont(Dataset):
  name = 'Vermont.csv'
  _pd_read_kwds = {}

class WestVirginia(Dataset):
  name = 'WestVirginia.csv'
  _pd_read_kwds = {}

class Kansas(Dataset):
  name = 'Kansas.csv'
  _pd_read_kwds = {}

class NewJersey(Dataset):
  name = 'NewJersey.csv'
  _pd_read_kwds = {}

class Washington(Dataset):
  name = 'Washington.csv'
  _pd_read_kwds = {}

class Missouri(Dataset):
  name = 'Missouri.csv'
  _pd_read_kwds = {}

class RhodeIsland(Dataset):
  name = 'RhodeIsland.csv'
  _pd_read_kwds = {}

class DataLoader(object):
    """Load a dataset from a local file or remote URL.

    There are two ways to call this; for example to load the iris dataset, you
    can call this object and pass the dataset name by string:

        >>> from vega_datasets import data
        >>> df = data('iris')

    or you can call the associated named method:

        >>> df = data.iris()

    Optionally, additional parameters can be passed to either of these

    Optional parameters
    -------------------
    return_raw : boolean
        If True, then return the raw string or bytes.
        If False (default), then return a pandas dataframe.
    use_local : boolean
        If True (default), then attempt to load the dataset locally. If
        False or if the dataset is not available locally, then load the
        data from an external URL.
    **kwargs :
        additional keyword arguments are passed to the pandas parsing function,
        either ``read_csv()`` or ``read_json()`` depending on the data format.
    """

    _datasets = {name.replace("-", "_"): name for name in Dataset.list_datasets()}

    def list_datasets(self):
        return Dataset.list_datasets()

    def __call__(self, name, return_raw=False, use_local=True, **kwargs):
        loader = getattr(self, name.replace("-", "_"))
        if return_raw:
            return loader.raw(use_local=use_local, **kwargs)
        else:
            return loader(use_local=use_local, **kwargs)

    def __getattr__(self, dataset_name):
        if dataset_name in self._datasets:
            return Dataset.init(self._datasets[dataset_name])
        else:
            raise AttributeError("No dataset named '{0}'".format(dataset_name))

    def __dir__(self):
        return list(self._datasets.keys())


class LocalDataLoader(DataLoader):
    _datasets = {name.replace("-", "_"): name for name in Dataset.list_local_datasets()}

    def list_datasets(self):
        return Dataset.list_local_datasets()

    def __getattr__(self, dataset_name):
        if dataset_name in self._datasets:
            return Dataset.init(self._datasets[dataset_name])
        elif dataset_name in DataLoader._datasets:
            raise ValueError(
                "'{0}' dataset is not available locally. To "
                "download it, use ``vega_datasets.data.{0}()"
                "".format(dataset_name)
            )
        else:
            raise AttributeError("No dataset named '{0}'".format(dataset_name))
