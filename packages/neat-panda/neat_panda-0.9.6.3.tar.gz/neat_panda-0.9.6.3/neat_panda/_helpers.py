import pandas as pd
from warnings import warn
import toml


def _control_types(
    _df,
    _key,
    _value,
    _fill="NaN",
    _convert=False,
    _sep=None,
    _columns=[],
    _drop_na=False,
    _invert_columns=False,
):
    # spread and gather
    if not isinstance(_df, pd.DataFrame):
        raise TypeError("write something")
    if not isinstance(_key, str):
        raise TypeError()
    if not isinstance(_value, str):
        raise TypeError()
    # spread
    if isinstance(_fill, bool):
        raise TypeError()
    if not isinstance(_fill, (str, float, int)):
        raise TypeError()
    if not isinstance(_convert, bool):
        raise TypeError()
    if not isinstance(_sep, (str, type(None))):
        raise TypeError()
    # gather
    if not isinstance(_columns, (list, range)):
        raise TypeError()
    if isinstance(_columns, range) and len(_df.columns) - 1 < _columns[-1]:
        raise IndexError()
    if not isinstance(_drop_na, bool):
        raise TypeError()
    if not isinstance(_invert_columns, bool):
        raise TypeError()


def _assure_consistent_value_dtypes(new_df, old_df, columns, value):
    """
    """
    _dtype = old_df[value].dtypes
    _error_columns = []
    for col in columns:
        try:
            new_df[col] = new_df[col].astype(_dtype)
        except ValueError:
            new_df[col] = new_df[col].astype("O")
            _error_columns.append(col)
            continue
    if _error_columns:
        warn(
            UserWarning(
                f"""At least one NaN is generated in the following columns: {", ".join(_error_columns)}. Hence, the type of these columns is set to Object."""
            )
        )
    return new_df


def _custom_columns(columns, new_columns, key, sep):
    _cols = [i for i in columns if i not in new_columns]
    _custom = [key + sep + i for i in new_columns]
    return _cols + _custom


def _get_version_from_toml(path: str) -> str:
    """
    """
    with open(path, "r") as f:
        data = toml.loads(f.read())
        return data["tool"]["poetry"]["version"]


def control_value(func):
    def _control_value(*args, **kwargs):
        if isinstance(args[0], pd.DataFrame):
            dataframe1, dataframe2 = args[:2]
        else:
            dataframe1, dataframe2 = args[0].dataframe1, args[0].dataframe2
        if len(dataframe1.columns.to_list()) != len(dataframe2.columns.to_list()):
            raise ValueError(
                "The number of columns in the two dataframes must be identical."
            )
        if dataframe1.columns.to_list() != dataframe2.columns.to_list():
            warn(
                "The columnnames are not identical. The columnnames of the second dataframe is renamed to match those of dataframe1"
            )
            dataframe2.columns = dataframe1.columns.to_list()
        return func(*args, **kwargs)

    return _control_value


def control_duplicates(func):
    def _control_duplicates(*args, **kwargs):
        if isinstance(args[0], pd.DataFrame):
            dataframe1, dataframe2 = args[:2]
        else:
            dataframe1, dataframe2 = args[0].dataframe1, args[0].dataframe2
        _duplicates_dataframe1 = dataframe1.duplicated().sum()
        _duplicates_dataframe2 = dataframe2.duplicated().sum()
        if _duplicates_dataframe1 > 0:
            warn(
                UserWarning(
                    f"There are {_duplicates_dataframe1} duplicate rows in dataframe1. These are dropped in order to perform set operations"
                )
            )
            dataframe1 = dataframe1.drop_duplicates()
        if _duplicates_dataframe2 > 0:
            warn(
                UserWarning(
                    f"There are {_duplicates_dataframe2} duplicate rows in dataframe2. These are dropped in order to perform set operations"
                )
            )
            dataframe2 = dataframe2.drop_duplicates()
        return func(*args, **kwargs)

    return _control_duplicates
