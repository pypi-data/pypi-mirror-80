# -*- coding: utf-8 -*-

from typing import Optional, List
from dataclasses import dataclass

import pandas as pd
import pandas_flavor as pf
from ._helpers import control_duplicates, control_value


@pf.register_dataframe_method
def difference(dataframe1, dataframe2) -> pd.DataFrame:
    """The set difference between dataframe1 (S) and dataframe2 (T), i.e. it returns those elements that are in dataframe1
    but not in dataframe2. Formally S - T = {s|s ∈ S and s ∉ T}.

    If duplicates exists in either dataframe they are dropped and a UserWarning is issued.

    Does not alter the original DataFrame.

    Parameters
    ----------
    dataframe1 : pd.DataFrame\n
    dataframe2 : pd.DataFrame\n

    Returns
    -------
    pandas DataFrame\n
        The set difference between dataframe1 and dataframe2

    Raises
    ------
    ValueError\n
        Raises ValueError if the columns in datframe1 and dataframe2 are not identical.
    """
    return SetOperations(dataframe1, dataframe2).difference()


@pf.register_dataframe_method
def symmetric_difference(
    dataframe1, dataframe2, dataframe_names: Optional[List[str]] = None
) -> pd.DataFrame:
    """The symmetric set difference between dataframe1 (S) and dataframe2 (T). It is the same as the union of the set difference between
    dataframe1 and dataframe2 and the set difference between dataframe2 and dataframe1. Formally A ⊕ B = (A - B) ∪ (B - A).

    If duplicates exists in either dataframe they are dropped and a UserWarning is issued.

    Does not alter the original DataFrame.

    Parameters
    ----------
    dataframe1 : pd.DataFrame\n
    dataframe2 : pd.DataFrame\n
    dataframe_names : Optional[List[str]], default None\n
        The names given in the list is inserted in the returned dataframe in a column called 'original_dataframe'. The purpose
        of this column is to make it easier to track differences between the two dataframes.

    Returns
    -------
    pandas DataFrame\n
        The set symmetric difference between dataframe1 and dataframe2

    Raises
    ------
    ValueError\n
        Raises ValueError if the columns in datframe1 and dataframe2 are not identical.
    ValueError\n
        Raises ValueError if the dataframe_names parameter is used and the length of the passed list is not 2.

    Example
    -------
    ```python
    import pandas as pd
    import neat_panda

    print(df1)

        country  continent  year  actual
    0   Sweden     Europe  2018       1
    1   Sweden     Europe  2019       2
    2  Denmark  Not known  2018       3

    print(df2)

        country  continent  year  actual
    0    Sweden     Europe  2018       1
    1   Denmark  Not known  2018       3
    2  Iceleand     Europe  2019       0

    df3 = df1.symmetric_difference(df2, dataframe_names=["df1", "df2"])
    print(df3)

    country       continent  year  actual original_dataframe
    0   Sweden       Europe  2019       2                df1
    1  Denmark    Not known  2018       3                df1
    2   Sweden       Europe  2012       2                df2
    3  Finland  Scandinavia  2018       3                df2
    ```
    """
    return SetOperations(dataframe1, dataframe2).symmetric_difference(
        dataframe_names=dataframe_names
    )


@pf.register_dataframe_method
def intersection(dataframe1, dataframe2) -> pd.DataFrame:
    """The set intersection between dataframe1 (S) and dataframe2 (T), i.e. it returns the elements that are both in dataframe1
    and dataframe2. Formally S ∩ T = {s|s ∈ S and s ∈ T}.

    If duplicates exists in either dataframe they are dropped and a UserWarning is issued.

    Does not alter the original DataFrame.

    Parameters
    ----------
    dataframe1 : pd.DataFrame\n
    dataframe2 : pd.DataFrame\n

    Returns
    -------
    pandas DataFrame\n
        The set intersection between dataframe1 and dataframe2

    Raises
    ------
    ValueError\n
        Raises ValueError if the columns in datframe1 and dataframe2 are not identical.
    """
    return SetOperations(dataframe1, dataframe2).intersection()


@pf.register_dataframe_method
def union(dataframe1, dataframe2) -> pd.DataFrame:
    """The set union between dataframe1 (S) and dataframe2 (T), i.e. it returns the elements that are both in dataframe1
    and dataframe2. Formally S ∩ T = {s|s ∈ S and s ∈ T}.

    If duplicates exists in either dataframe they are dropped and a UserWarning is issued.

    Does not alter the original DataFrame.

    Syntactic sugar for the pandas dataframe append method.

    Parameters
    ----------
    dataframe1 : pd.DataFrame\n
    dataframe2 : pd.DataFrame\n

    Returns
    -------
    pandas DataFrame\n
        The set difference between dataframe1 and dataframe2

    Raises
    ------
    ValueError\n
        Raises ValueError if the columns in datframe1 and dataframe2 are not identical.

    Example
    -------
    ```python
    import panda as pd
    import neat_panda

    print(df1)

        country  continent  year  actual
    0    Sweden     Europe  2018       1
    1   Denmark  Not known  2018       3
    2  Iceleand     Europe  2019       0

    print(df2)

        country  continent  year  actual
    0    Sweden     Europe  2020       1
    1   Denmark  Not known  2020       3

    df3 = df1.union(df2)
    print(df3)

        country  continent  year  actual
    0    Sweden     Europe  2018       1
    1   Denmark  Not known  2018       3
    2  Iceleand     Europe  2019       0
    3    Sweden     Europe  2020       1
    4   Denmark  Not known  2020       3
    ```
    """
    return SetOperations(dataframe1, dataframe2).union()


@dataclass
class SetOperations:
    dataframe1: pd.DataFrame
    dataframe2: pd.DataFrame

    @control_value
    @control_duplicates
    def difference(self) -> pd.DataFrame:
        """The set difference between dataframe1 (S) and dataframe2 (T), i.e. it returns those elements that are in dataframe1
        but not in dataframe2. Formally S - T = {s|s ∈ S and s ∉ T}.

        If duplicates exists in either dataframe they are dropped and a UserWarning is issued.

        Does not alter the original DataFrame.

        Parameters
        ----------
        dataframe1 : pd.DataFrame\n
        dataframe2 : pd.DataFrame\n

        The code is copied from the users WeNYoBen answer to the question "Python Pandas - Find difference between two data
        frames" at [StackOverflow](https://stackoverflow.com/questions/48647534/python-pandas-find-difference-between-two-data-frames)

        Returns
        -------
        pandas DataFrame\n
            The set difference between dataframe1 and dataframe2

        Raises
        ------
        ValueError\n
            Raises ValueError if the columns in datframe1 and dataframe2 are not identical.
        """
        return pd.concat(
            [self.dataframe1, self.dataframe2, self.dataframe2]
        ).drop_duplicates(keep=False)

    @control_value
    @control_duplicates
    def symmetric_difference(
        self, dataframe_names: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """The symmetric set difference between dataframe1 (S) and dataframe2 (T). It is the same as the union of the set difference between
        dataframe1 and dataframe2 and the set difference between dataframe2 and dataframe1. Formally A ⊕ B = (A - B) ∪ (B - A).

        If duplicates exists in either dataframe they are dropped and a UserWarning is issued.

        Does not alter the original DataFrame.

        Parameters
        ----------
        dataframe1 : pd.DataFrame\n
        dataframe2 : pd.DataFrame\n
        dataframe_names : Optional[List[str]], default None\n
            The names given in the list is inserted in the returned dataframe in a column called 'original_dataframe'. The purpose
            of this column is to make it easier to track differences between the two dataframes.

        Returns
        -------
        pandas DataFrame\n
            The set symmetric difference between dataframe1 and dataframe2

        Raises
        ------
        ValueError\n
            Raises ValueError if the columns in datframe1 and dataframe2 are not identical.
        ValueError\n
            Raises ValueError if the dataframe_names parameter is used and the length of the passed list is not 2.
        """
        if dataframe_names and len(dataframe_names) != 2:
            raise ValueError("Only two dataframe names")
        df1 = self.difference()
        self._swap_dataframes()
        df2 = self.difference()
        if dataframe_names:
            df1["original_dataframe"] = dataframe_names[0]
            df2["original_dataframe"] = dataframe_names[1]
        return pd.concat([df1, df2]).reset_index(drop=True)

    def _swap_dataframes(self):
        temp = self.dataframe1.copy()
        self.dataframe1 = self.dataframe2.copy()
        self.dataframe2 = temp.copy()

    @control_value
    @control_duplicates
    def intersection(self) -> pd.DataFrame:
        """The set intersection between dataframe1 (S) and dataframe2 (T), i.e. it returns the elements that are both in dataframe1
        and dataframe2. Formally S ∩ T = {s|s ∈ S and s ∈ T}.

        If duplicates exists in either dataframe they are dropped and a UserWarning is issued.

        Does not alter the original DataFrame.

        Parameters
        ----------
        dataframe1 : pd.DataFrame\n
        dataframe2 : pd.DataFrame\n

        Returns
        -------
        pandas DataFrame\n
            The set intersection between dataframe1 and dataframe2

        Raises
        ------
        ValueError\n
            Raises ValueError if the columns in datframe1 and dataframe2 are not identical.
        """
        return self.dataframe1.merge(right=self.dataframe2, how="inner").reset_index(
            drop=True
        )

    @control_value
    @control_duplicates
    def union(self) -> pd.DataFrame:
        """The set union between dataframe1 (S) and dataframe2 (T), i.e. it returns the elements that are both in dataframe1
        and dataframe2. Formally S ∩ T = {s|s ∈ S and s ∈ T}.

        If duplicates exists in either dataframe they are dropped and a UserWarning is issued.

        Does not alter the original DataFrame.

        Syntactic sugar for the pandas dataframe append method.

        Parameters
        ----------
        dataframe1 : pd.DataFrame\n
        dataframe2 : pd.DataFrame\n

        Returns
        -------
        pandas DataFrame\n
            The set difference between dataframe1 and dataframe2

        Raises
        ------
        ValueError\n
            Raises ValueError if the columns in datframe1 and dataframe2 are not identical.
        """
        return self.dataframe1.append(self.dataframe2).reset_index(drop=True)


if __name__ == "__main__":
    pass
