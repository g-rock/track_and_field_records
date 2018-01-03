import pandas as pd

def update_records(tfrrs_file, records_file, use_link_col):
    df = pd.read_csv(records_file, header=None)


    records = pd.DataFrame(df[7].str.split(' ').tolist())

    records["record"] = df[8]
    del records[2]
    records = records.apply(lambda x: x.astype(str).str.lower())

    tfrrs_dict = {
        "60hurdles": "60h",
        "1run": "1mile",
        "2run": "2mile",
        "indoor": "ipentathlon",
        "distance": "4000dmr",
        "high": "hj",
        "long": "lj",
        "pole": "pv",
        "triple": "tj",
        "shot": "sp",
        "weight": "wt",

    }

    for index, row in records.iterrows():
        if row[3] != "none":
            key = row[1] + row[3]
            if tfrrs_dict.has_key(key):
                records.set_value(index, 1, tfrrs_dict[key])

        else:
            key = row[1]
            if tfrrs_dict.has_key(key):
                records.set_value(index, 1, tfrrs_dict[key])

    meet = pd.read_csv(tfrrs_file, header=None)
    meet["record"] = ""

    for index, row in meet.iterrows():
        gender = (meet[1][index]).lower()
        event_identifier = (meet[0][index]).lower()
        if event_identifier in records[1].values:
            meet.set_value(index, "record", records.loc[(records[0] == gender) & (records[1] == event_identifier)].iloc[0]['record'])

    if use_link_col == 'true':
        meet[8] = ""

    return meet
