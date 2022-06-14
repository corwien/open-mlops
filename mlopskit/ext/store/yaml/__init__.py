"""``YAMLDataSet`` loads the data from json/yaml format file
"""

__all__ = ["YAMLDataSet"]

from contextlib import suppress

with suppress(ImportError):
    from .yaml_dataset import YAMLDataSet
