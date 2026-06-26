import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def sort_data(path: str, dictionary: dict, index_range: int) -> dict:

    storage: dict = {}

    df = pd.read_csv(path)

    for key in dictionary.keys():
        t: int | float = dictionary[key]

        idx: int = df.index[df['time'] == t].values[0]
        min_idx: int = idx - index_range
        max_idx: int = idx + index_range

        df_sorted = df.iloc[min_idx:max_idx, :]
        storage[key] = df_sorted

    return storage


def plot_pump_curve(data: list[dict], col_names: list, rpm: list) -> None:

    if len(data) != len(rpm):
        raise ValueError("Length of data and rpm lists does not match!")
    else:
        df = pd.DataFrame(np.nan,
                          index=range(0, 9),
                          columns=[str(col_elem) +
                                   " bei " +
                                   str(rpm_elem) + " rpm"
                                   for rpm_elem in rpm for col_elem in col_names])

        fig, ax = plt.subplots(figsize=(15, 7.5))
        for dd, i in zip(data, range(len(rpm))):
            df_storage = pd.DataFrame(np.nan,
                                      index=range(0, 9),
                                      columns=col_names)

            for key, j in zip(dd.keys(), range(len(dd.keys()))):
                df_mean = dd[key].mean().to_frame().T

                df_storage.iloc[j, :] = df_mean[col_names]

            df.iloc[:, (i*2):(i*2)+2] = df_storage
            df.plot((i*2)+1, (i*2), ax=ax, style='s-', grid=True,
                    xlabel="Volumenstrom in L/min", ylabel="Druckdifferenz in mmHg")
            del df_storage

        plt.tight_layout()
        plt.show()
