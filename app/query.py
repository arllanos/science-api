import numpy as np
import pandas as pd
from sqlalchemy.sql import text
from database import engine

conn = engine.connect()

CATEGORICAL_COLS = ['CountryCodeoftheProvider', 'StateCodeoftheProvider', 'CityoftheProvider', 'ZipCodeoftheProvider', 'HCPCSCode']
NUMERICAL_COLS = ['NumberofServices', 'NumberofMedicareBeneficiaries', 'NumberofDistinctMedicareBeneficiaryPerDayServices'
        , 'AverageMedicareAllowedAmount', 'AverageSubmittedChargeAmount', 'AverageMedicarePaymentAmount', 'AverageMedicareStandardizedAmount'
        ]

def to_dataframe(data):
    df = pd.DataFrame(data, columns=CATEGORICAL_COLS+NUMERICAL_COLS)

    # TODO: transform data type in the initialization of db so we can get rid of this function
    for col_name in NUMERICAL_COLS:
        df[col_name] = df[col_name].str.replace(',', '').astype(float)

    return df


def query_submit(country: str, state: str, city: str, zip_code: str, hcpcs_code: int):
    sql = text(
        "SELECT"
        # TODO: make more DRY using CATEGORICAL_COLS and NUMERICAL_COLS
        " CountryCodeoftheProvider, StateCodeoftheProvider, CityoftheProvider, ZipCodeoftheProvider, HCPCSCode"
        "     , NumberofServices, NumberofMedicareBeneficiaries, NumberofDistinctMedicareBeneficiaryPerDayServices"
        "     , AverageMedicareAllowedAmount, AverageSubmittedChargeAmount, AverageMedicarePaymentAmount, AverageMedicareStandardizedAmount"
        "  FROM mytable"
        " WHERE (CountryCodeoftheProvider = :c OR :c = '')"
        " AND (StateCodeoftheProvider = :s OR :s = '')"
        " AND (CityoftheProvider = :y OR :y = '')"
        " AND (ZipCodeoftheProvider = :z OR :z = '')"
        " AND (HCPCSCode = :h OR :h = '')"
        " LIMIT 1000"
        )
    result = conn.execute(sql, c=country, s=state, y=city,  z=zip_code, h=hcpcs_code).fetchall()
    df = to_dataframe(result)
    return df


def get_stats(metric: str, filters: dict) -> dict:
    country = filters.get('CountryCodeoftheProvider', '')
    state = filters.get('StateCodeoftheProvider', '')
    city = filters.get('CityoftheProvider', '')
    zip_code = filters.get('ZipCodeoftheProvider', '')
    hcpcs_code = filters.get('HCPCSCode', '')

    df = query_submit(country, state, city, zip_code, hcpcs_code)
    result = {
        "min":  df[metric].min(),
        "max":  df[metric].max(),
        "mean": df[metric].mean()
    }
    return result

    # return df.groupby(list(filters.keys()))[metric].agg([np.min, np.max, np.mean])

# metric_id = "NumberofServices"
# d_filters = {"CountryCodeoftheProvider": "US", "ZipCodeoftheProvider": 602011718, "HCPCSCode": 99232}
# stats = get_stats(metric_id, d_filters)
# print(stats)