import pandas as pd
import os

filename = "india-districts-census-2011.csv"
filepath = os.path.join("data", filename)

df = pd.read_csv(filepath)

# for literacy rate get no of literate / total poulation


def most_literate():
    highest_literacy_rate_index = df["Literate"].idxmax()
    literacy_rate = df.iloc[highest_literacy_rate_index, 6]
    district = df.iloc[highest_literacy_rate_index, 2]
    state = df.iloc[highest_literacy_rate_index, 1]
    print(f"State:{state} \nDistrict:{district} \nLiteracy rate:{literacy_rate}")


most_literate()


def least_literate():
    lowest_literacy_rate_index = df["Literate"].idxmin()
    literacy_rate = df.iloc[lowest_literacy_rate_index, 6]
    district = df.iloc[lowest_literacy_rate_index, 2]
    state = df.iloc[lowest_literacy_rate_index, 1]
    print(f"State:{state} \nDistrict:{district} \nLiteracy rate:{literacy_rate}")


least_literate()
