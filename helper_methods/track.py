import pandas as pd

def update_records(tfrrs_file, records_file, drop_link_col, drop_relay_sb):
    df = pd.read_csv(records_file, header=None)


    records = pd.DataFrame(df[7].str.split(' ').tolist())

    records["record"] = df[8]
    del records[2]
    records = records.apply(lambda x: x.astype(str).str.lower())

    relays = ['4x400', '4x100','4x800','4000dmr', 'poo']

    tfrrs_dict = {
        "60hurdles": "60h",
        "100hurdles": "100h",
        "110hurdles": "110h",
        "400hurdles": "400h",
        "1run": "1mile",
        "2run": "2mile",
        "1": "1mile",
        "3000steeplechase": "3000steeple",
        "indoor": "ipentathlon",
        "distance": "4000dmr",
        "dmr": "4000dmr",
        "high": "hj",
        "long": "lj",
        "pole": "pv",
        "triple": "tj",
        "shot": "sp",
        "weight": "wt",
        "javelin": "jav",
        "hammer": "ht",
        "discus": "dt",

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
        try:
            event_record = records.loc[(records[0] == gender) & (records[1] == event_identifier)].iloc[0]['record']
            meet.set_value(index, "record", event_record)
        except (IndexError):
            pass
            print '{}\'s {} record not supplied. Therefore it cannot be set in the new tffrs file.'.format(gender, event_identifier)

    if drop_link_col == 'true':
        meet[8] = meet[8] + " " + "onclick='return false;'"

    if drop_relay_sb == 'true':
        for relay in relays:
            for index, row in meet.loc[(meet[0] == relay)].iterrows():
                meet.set_value(index, 6, "")

    return meet
