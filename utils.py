import pandas as pd
import xlrd
import os
import numpy as np

ROOT = os.path.abspath(os.path.dirname(__file__))

REGIONS = ["Asia", "China", "EU15", "NorthAmerica", "US"]

PPES = ['630790'
        '392690',
        '621010',
        '392620',
        '900490',
        '401511']


def countries_of(continent):
    file_path = f"{ROOT}/data/countries_by_continent.xlsx"
    assert continent in ["African", "Asian", "European",
                         "North_American", "Oceanian", "South_American"]
    try:
        countries = pd.read_excel(file_path, sheet_name=continent)
    except (FileNotFoundError, xlrd.biffh.XLRDError):
        url = f"https://en.wikipedia.org/wiki/List_of_{continent}_countries_by_area"
        if continent == "Asian":
            countries = pd.read_html(url)[1]
        else:
            countries = pd.read_html(url)[0]

        mode = "w" if not os.path.exists(file_path) else "a"

        with pd.ExcelWriter(file_path, engine='openpyxl', mode=mode) as writer:
            countries.to_excel(writer, sheet_name=continent)

    return countries.iloc[:, 2].to_list()


def iso_alpha_codes_of(continent):
    assert continent in ["AF", "AS", "EU",
                         "NAM", "OC", "SA"], f"Unknown continent {continent}"
    file_path = f"{ROOT}/data/iso_alpha.xlsx"
    try:
        table = pd.read_excel(file_path)
    except FileNotFoundError:
        url = "https://en.wikipedia.org/wiki/List_of_sovereign_state" \
              "s_and_dependent_territories_by_continent_(data_file)"
        table = pd.read_html(url)[2]
        table.to_excel(file_path)

    return table[table.CC == continent]["a-3"].to_list()


def get_iso_alpha(region):
    assert region in ["Asia", "China", "EU15", "NorthAmerica", "US"]

    if region == "China":
        return ["CHN"]
    if region == "US":
        return ["USA"]
    if region == "NorthAmerica":
        ret = iso_alpha_codes_of("NAM")
        ret.remove("USA")
        return ret
    if region == "EU15":
        ret = iso_alpha_codes_of("EU")
        ret.remove("RUS")
        ret.remove("KAZ")
        return ret
    if region == "Asia":
        ret = iso_alpha_codes_of("AS")
        ret.remove("CHN")
        ret.remove(np.nan)
        ret.remove(np.nan)
        return ret


def entity_to_entity_data(a, b):
    assert a in REGIONS
    assert b in REGIONS

    return pd.read_excel(f"{ROOT}/data/export_data/{a} Export.xlsx",
                         sheet_name=f"{a}_to_{b}",
                         header=1,
                         usecols=[0, 1, 2, 3, 4]
                         if b != "NorthAmerica" else [0, 1, 8, 9, 10],
                         names=["ppe", "desc", "2017", "2018", "2019"])


def supplier_number(region="all"):
    file_path = f"{ROOT}/data/export_data/suppliers.xlsx"
    df = pd.read_excel(file_path)
    if region == "all":
        return df
    else:
        return df[df["Countries or Regions"] == region]


