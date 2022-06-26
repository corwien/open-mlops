"""``MemoryDataSet`` is a data set implementation which handles in-memory data.
"""

import copy
from typing import Any, Dict

from mlopskit.io.core import AbstractDataSet, DataSetError

_EMPTY = object()


class MemoryDataSet(AbstractDataSet):
    """``MemoryDataSet`` loads and saves data from/to an in-memory
    Python object.
    Example:
    ::
        >>> from kedro.io import MemoryDataSet
        >>> import pandas as pd
        >>>
        >>> data = pd.DataFrame({'col1': [1, 2], 'col2': [4, 5],
        >>>                      'col3': [5, 6]})
        >>> data_set = MemoryDataSet(data=data)
        >>>
        >>> loaded_data = data_set.load()
        >>> assert loaded_data.equals(data)
        >>>
        >>> new_data = pd.DataFrame({'col1': [1, 2], 'col2': [4, 5]})
        >>> data_set.save(new_data)
        >>> reloaded_data = data_set.load()
        >>> assert reloaded_data.equals(new_data)
    """

    def __init__(self, data: Any = _EMPTY, copy_mode: str = None):
        """Creates a new instance of ``MemoryDataSet`` pointing to the
        provided Python object.
        Args:
            data: Python object containing the data.
            copy_mode: The copy mode used to copy the data. Possible
                values are: "deepcopy", "copy" and "assign". If not
                provided, it is inferred based on the data type.
        """
        self._data = _EMPTY
        self._copy_mode = copy_mode
        if data is not _EMPTY:
            self._save(data)

    def _load(self) -> Any:
        if self._data is _EMPTY:
            raise DataSetError("Data for MemoryDataSet has not been saved yet.")

        copy_mode = self._copy_mode or _infer_copy_mode(self._data)
        data = _copy_with_mode(self._data, copy_mode=copy_mode)
        return data

    def _save(self, data: Any):
        copy_mode = self._copy_mode or _infer_copy_mode(data)
        self._data = _copy_with_mode(data, copy_mode=copy_mode)

    def _exists(self) -> bool:
        return self._data is not _EMPTY

    def _release(self) -> None:
        self._data = _EMPTY

    def _describe(self) -> Dict[str, Any]:
        if self._data is not _EMPTY:
            return dict(data=f"<{type(self._data).__name__}>")
        # the string representation of datasets leaves out __init__
        # arguments that are empty/None, equivalent here is _EMPTY
        return dict(data=None)  # pragma: no cover


def _infer_copy_mode(data: Any) -> str:
    """Infers the copy mode to use given the data type.
    Args:
        data: The data whose type will be used to infer the copy mode.
    Returns:
        One of "copy", "assign" or "deepcopy" as the copy mode to use.
    """
    # pylint: disable=import-outside-toplevel
    try:
        import pandas as pd
    except ImportError:  # pragma: no cover
        pd = None  # pragma: no cover
    try:
        import numpy as np
    except ImportError:  # pragma: no cover
        np = None  # pragma: no cover

    if pd and isinstance(data, pd.DataFrame) or np and isinstance(data, np.ndarray):
        copy_mode = "copy"
    elif type(data).__name__ == "DataFrame":
        copy_mode = "assign"
    else:
        copy_mode = "deepcopy"
    return copy_mode


def _copy_with_mode(data: Any, copy_mode: str) -> Any:
    """Returns the copied data using the copy mode specified.
    If no copy mode is provided, then it is inferred based on the type of the data.
    Args:
        data: The data to copy.
        copy_mode: The copy mode to use, one of "deepcopy", "copy" and "assign".
    Raises:
        DataSetError: If copy_mode is specified, but isn't valid
            (i.e: not one of deepcopy, copy, assign)
    Returns:
        The data copied according to the specified copy mode.
    """
    if copy_mode == "deepcopy":
        copied_data = copy.deepcopy(data)
    elif copy_mode == "copy":
        copied_data = data.copy()
    elif copy_mode == "assign":
        copied_data = data
    else:
        raise DataSetError(
            f"Invalid copy mode: {copy_mode}. "
            f"Possible values are: deepcopy, copy, assign."
        )

    return copied_data