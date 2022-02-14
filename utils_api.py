# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 10:58:24 2022

@author: johnk

https://docs.python-requests.org/en/latest/
"""

# %% Packages

import json
import pandas as pd
import requests


# %% Labels

res_list = []
table_types = ["", "subject/", "profile/", "cprofile/"]
for table_type in table_types:
    link = "https://api.census.gov/data/2019/acs/acs5/" \
        + table_type + "variables.json"
    res = requests.get(link)
    response = json.loads(res.text)
    response = response["variables"]
    res_list.append(pd.DataFrame.from_dict(response).T)

Labels = pd.concat(res_list, axis=0)

# print(Labels.loc["DP03_0033E", "label"])
# print(Labels.info())


# %% Functions


def create_census_api(cols, full_table=False):
    """Build API link based on column information from a list of columns"""
    assert type(cols) == list, "input cols as list"
    # Split use case where we want the full table
    if full_table:
        id_table = cols[0]
        lnk_variable_list = f"group({id_table})"
    else:
        id_table = cols[0].split("_")[0]
        cols_str = ",".join(cols)
        lnk_variable_list = "NAME,GEO_ID," + cols_str
    # Identify table
    if id_table[:2] == "DP":
        lnk_get_fnc = "profile?get="
    elif id_table[0] == "S":
        lnk_get_fnc = "subject?get="

    # Base/static information
    lnk_census_data_api = "https://api.census.gov/data/"
    lnk_dataset = "2019/acs/acs5/"
    # lnk_get_fnc
    # lnk_variable_list
    lnk_predicate = "&for="
    lnk_geography = "county:*&in=state:*"
    lnk_key = "&key=d665833afd3f36d12b9a0e2832c3d6b92830a29a"
    link = f"{lnk_census_data_api}{lnk_dataset}{lnk_get_fnc}" + \
        f"{lnk_variable_list}{lnk_predicate}{lnk_geography}{lnk_key}"
    return link


def retrieve_data(link):
    res = requests.get(link)
    response = json.loads(res.text)
    data = pd.DataFrame(data=response[1:], columns=response[0])
    data = data.sort_values('GEO_ID').reset_index(drop=True)
    return data


# %% Economic Diversity

cols = ['DP03_00' + str(col) + 'E' for col in range(32, 46)]

link = create_census_api(cols)
data = retrieve_data(link)

print()
for feature in cols:
    print(Labels.loc[feature, 'label'])
print()


# %% Women in Workforce

cols = ['DP03_00' + str(col) + 'E' for col in range(10, 14)]

link = create_census_api(cols)
data = retrieve_data(link)

print()
for feature in cols:
    print(Labels.loc[feature, 'label'])
print()


# %% Access to Internet, S2801

cols = ["S2801_C02_001E", "S2801_C02_005E", "S2801_C02_006E"]

link = create_census_api(cols)
data = retrieve_data(link)
print("pulling -E, receiving percent estimate")

print()
for feature in cols:
    print(Labels.loc[feature, 'label'])
print()


# %% Old Code


# %% DP03, Full Table

# lnk_variable_list = "group(DP03)"

# res = requests.get(link)
# response = json.loads(res.text)
