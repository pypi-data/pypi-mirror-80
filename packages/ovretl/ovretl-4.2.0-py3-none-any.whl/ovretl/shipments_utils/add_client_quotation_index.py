import pandas as pd
import numpy as np


def sort_and_index_group(group: pd.DataFrame):
    sorted_group = group.sort_values("created_at", ascending=True)
    sorted_group.index = np.arange(1, len(sorted_group) + 1)
    return sorted_group


def add_client_quotation_index(quotation_df: pd.DataFrame):
    quotation_df = quotation_df.groupby(["client_name"]).apply(lambda g: sort_and_index_group(g))
    quotation_df = quotation_df.drop(columns="client_name").reset_index()
    quotation_df = quotation_df.rename(columns={"level_1": "quotation_number"})
    return quotation_df
