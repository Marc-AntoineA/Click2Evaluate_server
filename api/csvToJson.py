import pandas as pd


def convert(name):
    """
    Convert a ";" csv file using pandas
    """
    data = pd.read_csv(name + ".csv", sep = ";")
    data.to_json(name + ".json", orient="records", double_precision = 0, force_ascii = False)
