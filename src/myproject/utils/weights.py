"""Weight generation: SMARTER, reciprocal, and rank-sum methods."""

import numpy as np
import pandas as pd


def generate_weights(
    data: int | float | list[int] | dict[str, int] | pd.Series,
) -> pd.DataFrame:
    """Generate weights for ranked items using three methods.

    Accepts a count (N), a list of ranks, a dict of {name: rank}, or a Series.
    Ranks may contain ties.

    Args:
        data: One of:
            - int/float: number of items (ranks auto-assigned 1..N)
            - list: explicit ranks (ties allowed)
            - dict or Series: named attributes with ranks

    Returns:
        DataFrame with columns: Ranks, SMARTER, Rank Reciprocal, Rank Sum.
    """
    if isinstance(data, dict):
        data = pd.Series(data)

    if isinstance(data, pd.Series):
        number = len(data)
        df = pd.DataFrame(data, columns=["Ranks"])
    elif isinstance(data, (int, float)):
        number = int(data)
        ranks = list(range(1, number + 1))
        df = pd.DataFrame({"Ranks": ranks}, index=ranks)
    elif isinstance(data, list):
        number = len(data)
        df = pd.DataFrame({"Ranks": data}, index=range(1, number + 1))
    else:
        raise TypeError(f"Unsupported data type: {type(data)}")

    df.index.name = "Attributes"
    original_order = df.index.copy()
    df = df.sort_values(by="Ranks", ascending=True)

    # SMARTER
    df["1-n"] = range(1, 1 + number)
    df["1/n"] = np.reciprocal(df["1-n"].astype(float))
    df["partial_sum"] = df["1/n"].sort_values(ascending=True).values.cumsum()
    df["partial_sum"] = df["partial_sum"].sort_values(ascending=False).values

    # Rank reciprocal
    df["1/R"] = np.reciprocal(df["Ranks"].astype(float))

    # Rank sum — adjust for ties
    df["rank_adj"] = df["Ranks"].copy(deep=True)
    repeats = df["Ranks"].value_counts()
    repeats = repeats[repeats > 1]
    for repeat in repeats.index:
        match_index = df[df["Ranks"] == repeat].index
        df.loc[match_index, "rank_adj"] += (len(match_index) - 1) / len(match_index)
        df.loc[match_index, "partial_sum"] = df.loc[match_index, "partial_sum"].max()
    df["rank_adj_rev"] = number - df["rank_adj"].values + 1

    df["SMARTER"] = df["partial_sum"] / number
    df["SMARTER"] = df["SMARTER"] / df["SMARTER"].sum()
    df["Rank_Reciprocal"] = df["1/R"] / df["1/R"].sum()
    df["Rank_Sum"] = df["rank_adj_rev"] / df["rank_adj_rev"].sum()

    results = df[["Ranks", "SMARTER", "Rank_Reciprocal", "Rank_Sum"]].copy()
    results.columns = ["Ranks", "SMARTER", "Rank Reciprocal", "Rank Sum"]
    results = results.reindex(original_order)

    return results
