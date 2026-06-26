from functions import *

if __name__ == '__main__':
    # Radial Pump
    dict_4k = {"V1": 273, "V2": 390, "V3": 542, "V4": 595, "V5": 150}
    dict_6k = {"V1": 1263, "V2": 1228, "V3": 1163, "V4": 1031, "V5": 887, "V6": 819}
    dict_8k = {"V1": 1772, "V2": 1723, "V3": 1684, "V4": 1642, "V5": 1603, "V6": 1459, "V7": 1409}

    path = "radial_pump/Kontinuierlich_HM3.csv"

    sorted_data_4k = sort_data(path=path, dictionary=dict_4k, index_range=25)
    sorted_data_6k = sort_data(path=path, dictionary=dict_6k, index_range=25)
    sorted_data_8k = sort_data(path=path, dictionary=dict_8k, index_range=25)

    data = [sorted_data_4k, sorted_data_6k, sorted_data_8k]

    plot_pump_curve(data=data, col_names=["Druckdifferenz", "V"], rpm=[4000, 6000, 8000])

    # Axial Pump
    # dict_4000 = {"V1": 273, "V2": 390, "V3": 542, "V4": 595, "V5": 100}
    # dict_6000 = {"V1": 1263, "V2": 1228, "V3": 1163, "V4": 1031, "V5": 887, "V6": 819}
    # dict_8000 = {"V1": 1263, "V2": 1228, "V3": 1163, "V4": 1031, "V5": 887, "V6": 819}

    # Original Data
    """
    df = pd.read_csv(path, skiprows=0)
    print(df)
    df.plot.line("time", ["Druck1", "Druckdifferenz", "V"],
                 xlabel="Zeit in s", ylabel="Druck in mmHg",
                 grid=True, figsize=(15, 7.5), subplots=True)
    plt.tight_layout()
    plt.show()
    """
