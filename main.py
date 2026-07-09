from functions import *

if __name__ == '__main__':
    # Radial Pump
    dict_4k = {"Q1": 273, "Q2": 390, "Q3": 542, "Q4": 595, "Q5": 150}
    dict_6k = {"Q1": 1263, "Q2": 1228, "Q3": 1163, "Q4": 1031, "Q5": 887, "Q6": 819}
    dict_8k = {"Q1": 1772, "Q2": 1723, "Q3": 1684, "Q4": 1642, "Q5": 1603, "Q6": 1459, "Q7": 1409}

    path = "radial_pump/Kontinuierlich_HM3.csv"

    sorted_data_4k = sort_data(path=path, dictionary=dict_4k, index_range=25)
    sorted_data_6k = sort_data(path=path, dictionary=dict_6k, index_range=25)
    sorted_data_8k = sort_data(path=path, dictionary=dict_8k, index_range=25)

    data = [sorted_data_4k, sorted_data_6k, sorted_data_8k]

    plot_pump_curve(data=data,
                    col_names=["Druckdifferenz H", "Volumenstrom Q"],
                    rpm=[4000, 6000, 8000])

    plot_boxplot(data=data,
                 col_names=["Druckdifferenz H", "Volumenstrom Q"],
                 rpm=[4000, 6000, 8000], by_list="Timestamp")

    plot_std(data=data,
             col_names=["Druckdifferenz H", "Volumenstrom Q"],
             rpm=[4000, 6000, 8000])

    # Axial Pump
    df_axial_6k = pd.DataFrame(data=
                               {"Druckdifferenz H": [14, 6, 7, 6, 9],
                                "Volumenstrom Q": [0, 2, 3, 4, 4.5]})
    df_axial_7k = pd.DataFrame(data=
                               {"Druckdifferenz H": [30, 23, 26, 24, 25],
                                "Volumenstrom Q": [0, 1, 3, 4, 5.3]})
    df_axial_8k = pd.DataFrame(data=
                               {"Druckdifferenz H": [58, 47, 42, 43, 35],
                                "Volumenstrom Q": [0, 1, 3, 4, 5.6]})
    df_axial_9k = pd.DataFrame(data=
                               {"Druckdifferenz H": [74, 62, 55, 58, 45],
                                "Volumenstrom Q": [0, 1, 3, 4, 5.6]})

    # Original Data
    """
    df = pd.read_csv(path, skiprows=0)
    print(df)
    df.plot.line("time", ["Druck1", "Druckdifferenz H", "Volumenstrom Q"],
                 xlabel="Zeit in s", ylabel="Druck in mmHg",
                 grid=True, figsize=(15, 7.5), subplots=True)
    plt.tight_layout()
    plt.show()
    """

    # Pulsatile Messungen
    path_4000 = "radial_pump/Pulsatil_4000rpm.csv"
    path_6000 = "radial_pump/Pulsatil_6000rpm.csv"
    path_8000 = "radial_pump/Pulsatil_8000rpm.csv"

    evaluate_pulsatile("radial_pump/Pulsatil_4000rpm.csv", 4000, 9, 21)
    evaluate_pulsatile("radial_pump/Pulsatil_6000rpm.csv", 6000, 55, 64)
    evaluate_pulsatile("radial_pump/Pulsatil_8000rpm.csv", 8000, 70, 100)
    evaluate_pulsatile("radial_pump/Pulsatil_8000rpm.csv", 8000, 92, 94)

    #HQ Axial
    axial_data = {
    6000: {
        "Q":  [4.5, 4, 3, 2, 0],
        "H":  [9, 6, 7, 6, 14]
    },
    7000: {
        "Q":  [5.3, 4, 3, 1, 0],
        "H":  [25, 24, 23, 26, 30]
    },
    8000: {
        "Q":  [5.6, 4, 3, 1, 0],
        "H":  [35, 43, 42, 47, 58]
    },
    9000: {
        "Q":  [5.6, 4, 3, 1, 0],
        "H":  [45, 58, 55, 62, 74]
    }
    }
    plot_axial_curve(axial_data)

    evaluate_pulsatile("radial_pump/Pulsatil_8000rpm.csv", 8000, 92, 94)

    # Compare pulsatile with stationary
    col_names = ["Volumenstrom Q", "Druckdifferenz H"]
    mean_6k = mean_sorted_data(data=sorted_data_6k,
                               col_names=col_names)
    mean_8k = mean_sorted_data(data=sorted_data_8k,
                               col_names=col_names)

    comp_data = [mean_6k, mean_8k, df_axial_6k, df_axial_8k]
    comp_legend = ["Radial bei 6000 rpm", "Radial bei 8000 rpm", "Axial bei 6000 rpm", "Axial bei 8000 rpm"]
    plot_pump_curve_compare(data=comp_data,
                            legend_names=comp_legend)
