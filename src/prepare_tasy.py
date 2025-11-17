from typing import List

import pandas as pd
from tqdm import tqdm


def clear_df(df: pd.DataFrame) -> pd.DataFrame:
    return df.sort_values("data", ascending=False).drop_duplicates(
        subset=["rghc"], keep="first"
    )


def get_rghc_list(df_dict: dict) -> List[str]:
    rghc_list = []
    for df in df_dict.values():
        rghc_list.extend([id for id in df.rghc.unique().tolist()])
    return list(set(rghc_list))


def fill_records(df_dict: dict, id_list: List[str]) -> dict:
    full_records = dict.fromkeys(id_list, {})
    for db, df in tqdm(df_dict.items()):
        print("dataframe", db, "has shape", df.shape)
        for rghc in tqdm(df.rghc.unique().tolist()):
            df1 = df[df.rghc == rghc].drop(labels=["rghc"], axis=1)
            full_records[rghc][db] = df1.iloc[0].to_dict()
    return full_records


def pipeline(path_list: List[str]) -> dict:
    df_dict = {}
    for path in path_list:
        df_dict[path.split(".")[0]] = clear_df(pd.read_csv(path, low_memory=False))
    print("finished dataframe loading")
    id_list = get_rghc_list(df_dict)
    print("finished completing the datalake for", len(id_list), "patients")
    return fill_records(df_dict, id_list)


if __name__ == "__main__":
    import json

    export_path = "data/full_tasy_records.json"
    path_list = ["data/mm_tasy.csv", "data/tmo_tasy.csv"]

    full_records = pipeline(path_list)
    with open(export_path, "w") as f:
        json.dump(full_records, f, indent=4)
    print("Saved results at", export_path)
