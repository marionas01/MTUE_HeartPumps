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
        df_sorted.index = range(df_sorted.shape[0])
        df_sorted["Timestamp"] = pd.Series([dictionary[key] for x in range(df_sorted.shape[0])])
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
                    xlabel="Volumenstrom Q in L/min", ylabel="Druckdifferenz H in mmHg",
                    title="H-Q-Diagramm")
            del df_storage

        plt.tight_layout()
        plt.show()


def plot_boxplot(data: list[dict], col_names: list[str], by_list: list[str], rpm: list) -> None:
    if len(data) != len(rpm):
        raise ValueError("Length of data and rpm lists does not match!")

    for dd, i in zip(data, rpm):
        df_box = pd.DataFrame()
        for key in dd.keys():
            df_box = pd.concat([df_box, dd[key]], ignore_index=True)

        fig, axes = plt.subplots(1, len(col_names), figsize=(15, 7.5))
        if len(col_names) == 1:
            axes = [axes]  # keep it iterable/subscriptable for a single column

        y_labels = ["H in mmHg", "Q in L/min"]

        for idx, col in enumerate(col_names):
            df_box.boxplot(column=col, by=by_list, ax=axes[idx])
            axes[idx].set_ylabel(y_labels[idx])

        fig.suptitle(f"Drehzahl = {i} rpm")
        plt.tight_layout()
        plt.show()


def plot_std(data: list[dict], col_names: list[str], rpm: list) -> None:
    if len(data) != len(rpm):
        raise ValueError("Length of data and rpm lists does not match!")

    for dd, i in zip(data, rpm):
        d: dict = dict()
        for col in col_names:
            d[col] = []
            d[f"{col}_mean"] = []
        d["Timestamp"] = []
        for key in dd.keys():
            d["Timestamp"].append(dd[key].iloc[0, -1])
            stds = dd[key].std()
            means = dd[key].mean()
            for col in col_names:
                d[col].append(stds[col])
                d[f"{col}_mean"].append(means[col])

        fig, axes = plt.subplots(1, len(col_names), figsize=(15, 7.5))
        if len(col_names) == 1:
            axes = [axes]  # keep it iterable/subscriptable for a single column

        fig.suptitle(f"Drehzahl = {i} rpm")
        y_labels = ["H in mmHg", "Q in L/min"]
        for idx, col in enumerate(col_names):

            axes[idx].set_axisbelow(True)
            axes[idx].grid(color='gray', linestyle='dashed')
            #axes[idx].bar([str(x) for x in d["Timestamp"]], d[f"{col}_mean"])
            axes[idx].bar([str(x) for x in d["Timestamp"]], [(s/m) for s, m in zip(d[col], d[f"{col}_mean"])])
            #axes[idx].errorbar([str(x) for x in d["Timestamp"]], d[f"{col}_mean"], yerr=d[col],
            #                   fmt="o", color="k")
            axes[idx].set_title(col_names[idx])
            axes[idx].set_xlabel("Timestamp in s")
            axes[idx].set_ylabel("Variationskoeffizient")
            #axes[idx].set_ylabel(f"Standardabweichung von {y_labels[idx]}")

        plt.tight_layout()
        plt.show()
