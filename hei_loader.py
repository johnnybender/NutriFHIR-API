import pandas as pd
import configs
import utils
import random
import numpy as np

# Gets DF that's more suited for API endpoints keyed by hhid
def get_household_df():
    nutrients_df, items_df = get_dataframes(configs.NUTRIENTS_FILE_PATH, configs.ITEMS_FILE_PATH)
    # Generate random hhnum from list of valid ones
    df = clean_and_merge(nutrients_df, items_df)
    random_index = random.randint(0, df.shape[0] - 1)
    random_hh = df['hhnum'].iloc[random_index]
    # Don't need expensive merge on whole dataframe, just that with chosen hhid
    df = df.loc[df['hhnum'] == random_hh]
    # Do rest of cleaning and computing on reduced df
    df = add_hei_scores(df)
    return df

# Gets DF that's more suited for API endpoints keyed by foodcode
def get_foodcode_df(foodcode):
    nutrients_df, items_df = get_dataframes(configs.NUTRIENTS_FILE_PATH, configs.ITEMS_FILE_PATH)
    df = clean_and_merge(nutrients_df, items_df)
    df = df.set_index('foodcode')
    # Filter to avoid computing hei for all entries
    if (foodcode in df.index.values):
        df = df.loc[foodcode]
        df = add_hei_scores(df)
        return df
    else: # empty DF
        return pd.DataFrame()

# Gets DF that's more suited for API endpoints keyed by UPC
def get_upc_df(upc):
    nutrients_df, items_df = get_dataframes(configs.NUTRIENTS_FILE_PATH, configs.ITEMS_FILE_PATH)
    df = clean_and_merge(nutrients_df, items_df)
    df = df.set_index('barcode')
    # Filter to avoid computing hei for all entries
    if (upc in df.index.values):
        df = df.loc[upc]
        df = add_hei_scores(df)
        return df
    else:  # empty DF
        return pd.DataFrame()

# called by write_output_file.py
def get_unique_upc_df():
    nutrients_df, items_df = get_dataframes(configs.NUTRIENTS_FILE_PATH, configs.ITEMS_FILE_PATH)
    df = clean_and_merge(nutrients_df, items_df)
    df = add_hei_scores(df)
    cols_to_keep = ['barcode', 'foodcode', 'usdadescmain', 'hei_score']
    brief_df = df[cols_to_keep]
    unique_df = brief_df.drop_duplicates(subset='barcode', keep='first')
    return unique_df


def get_dataframes(nutrients_path, items_path):
    # Read files and make data types float, only keep cols we want
    nutrients_df = pd.read_csv(nutrients_path, usecols=configs.NUTRIENTS_FILE_COLS)
    items_df = pd.read_csv(items_path, usecols=configs.ITEMS_FILE_COLS)
    return nutrients_df, items_df


def clean_and_merge(nutrients_df, items_df):
    # Remove all rows with empty values
    nutrients_df = nutrients_df.dropna(how='any')
    items_df = items_df.dropna(how='any')

    # MIGHT WANT TO CHANGE THIS TO NOT USE .APPLY (NOT EFFICIENT)
    # Change values to numeric, using ignore for the description col (string)
    nutrients_df = nutrients_df.apply(pd.to_numeric, errors='ignore')
    items_df = items_df.apply(pd.to_numeric, errors='ignore')

    # Create unique key (eventid, itemnum) to join on
    nutrients_df['key'] = nutrients_df['eventid'].astype(str) + "_" + nutrients_df['itemnum'].astype(str)
    items_df['key'] = items_df['eventid'].astype(str) + "_" + items_df['itemnum'].astype(str)

    # Drop the eventid and itemnum cols from one df so we don't have multiple cols in enriched
    drop_cols = ['eventid', 'itemnum']
    nutrients_df.drop(drop_cols, inplace=True, axis='columns')

    # Join the 2 Dataframes return enriched one
    enriched_df = nutrients_df.merge(items_df, how='inner', on='key')

    # Compute values for SAAS headers instead of having CSV headers
    enriched_df = convert_column_names(enriched_df)
    return enriched_df


def add_hei_scores(df):
    # Add column for HEI score
    df['hei_score'] = df.apply(utils.compute_hei, axis=1)
    return df

# Converts/creates column to what HEI SAAS program is expecting
def convert_column_names(df):
    # Create columns that aren't 1-to-1 mapping
    df['vtotalleg'] = df['v_total'].add(df['v_legumes'])
    df['fwholefrt'] = df['f_citmlb'].add(df['f_other'])
    df['pfseaplantleg'] = df['pf_seafd_hi'].add(df['pf_seafd_low'])
    df['monopoly'] = df['monofat'].add(df['polyfat'])

    #drop these old boys that we just used to compute new boys
    drop_cols = [
        'v_total','v_legumes','f_citmlb','f_other','pf_seafd_hi',
        'pf_seafd_low','monofat','polyfat'
    ]
    df.drop(columns=drop_cols, inplace=True)

    #rename the other ones
    rename_dict = {
    'energy': 'kcal',
    'protein': 'pfallprotleg',
    'v_drkgr': 'vdrkgrleg',
    }
    df.rename(columns=rename_dict, inplace=True)
    return df
