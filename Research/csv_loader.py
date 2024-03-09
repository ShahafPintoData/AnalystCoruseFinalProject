import zipfile
import os
import pandas as pd

def get_csv_file(file_name, encoding="ISO-8859-1"):
    global csv_files, cleaning_files

    # Get file paths
    csv_file = csv_files[file_name]
    csv = rf"../Temp/{csv_file.get('csv')}.csv"
    zip = rf"../Datasets/{csv_file.get('zip')}.zip"

    # Check if csv file is extracted - Do so if not
    if not os.path.exists(csv):
        with zipfile.ZipFile(zip, 'r') as zipped_file:
            zipped_file.extract(os.path.basename(csv), os.path.dirname(csv))

    # Create dataframe from csv
    dataframe = pd.read_csv(csv, encoding=encoding, low_memory=False)

    # Clean data if possible
    if file_name in cleaning_files:
        cleaning = cleaning_files[file_name]
        dataframe = cleaning(dataframe)

    # Return dataframe
    return dataframe

def cleaning_terrorism(dataframe):
    # Filter records with invalid date
    dataframe = dataframe.loc[(dataframe['iday'] != 0) &  (dataframe['imonth'] != 0)] 

    # Convert date to more usable format
    dataframe['approxdate'] = pd.to_datetime(dict(year=dataframe['iyear'], month=dataframe['imonth'], day=dataframe['iday']))

    # Remove unnecessary columns 
    drop_columns = [
        'extended', 'resolution', 'crit2', 'crit3', 'alternative', 'alternative_txt', 'multiple', 'related', 'country',
        'region', 'vicinity', 'specificity', 'attacktype1', 'attacktype2', 'attacktype3', 'weaptype1', 'weaptype2', 'weaptype3',
        'weaptype4', 'weapsubtype1', 'weapsubtype2', 'weapsubtype2_txt', 'weapsubtype3', 'weapsubtype3_txt',
        'weapsubtype4', 'weapsubtype4_txt', 'weapdetail', 'targtype1', 'targsubtype1', 'corp1', 'natlty1', 'targtype2', 
        'targsubtype1_txt', 'targsubtype2_txt', 'corp2', 'natlty2', 'targtype3', 'targsubtype3_txt', 'targsubtype2', 'corp3',
        'natlty3', 'gsubname', 'gsubname2', 'gsubname3', 'guncertain1', 'guncertain2', 'guncertain3', 'individual', 'claimed',
        'claimmode', 'claimmode_txt', 'compclaim', 'claim2', 'claimmode2', 'claim3', 'claimmode3', 'nkillus', 'nwoundus', 
        'propextent', 'propcomment', 'nhostkidus', 'ransomnote', 'addnotes', 'scite1', 'scite2', 'scite3', 'dbsource', 'location'
    ]

    dataframe.drop(columns=drop_columns, inplace=True)
    dataframe.set_index('eventid', inplace=True)

    return dataframe

def cleaning_israeli_wars(dataframe):
    dataframe.set_index('name', inplace=True)

    return dataframe

def cleaning_islam_holidays(dataframe):
    dataframe.set_index('name', inplace=True)

    # Set dates as datetime
    dataframe['start_date'] = pd.to_datetime(dataframe['start_date'], format="%d/%m/%Y")
    dataframe['end_date'] = pd.to_datetime(dataframe['end_date'], format="%d/%m/%Y")

    return dataframe

def cleaning_jewish_holidays(dataframe):
    dataframe.set_index('name', inplace=True)

    # Set dates as datetime
    dataframe['start_date'] = pd.to_datetime(dataframe['start_date'], format="%d/%m/%Y")
    dataframe['end_date'] = pd.to_datetime(dataframe['end_date'], format="%d/%m/%Y")

    return dataframe

def cleaning_prime_ministers(dataframe):
    # Set dates as datetime
    dataframe['time_started'] = pd.to_datetime(dataframe['time_started'], format="%d/%m/%Y")
    dataframe['time_ended'] = pd.to_datetime(dataframe['time_ended'], format="%d/%m/%Y")

    return dataframe

def cleaning_pales_national_days(dataframe):
    dataframe.set_index('name', inplace=True)

    # Set dates as datetime
    dataframe['start_date'] = pd.to_datetime(dataframe['start_date'], format="%d/%m/%Y")
    dataframe['end_date'] = pd.to_datetime(dataframe['end_date'], format="%d/%m/%Y")

    return dataframe

# ----------------------------------------------------------------------------------------------------

csv_files = {
    'terrorism': {
        'zip': "terrorism",
        'csv': "terrorism"
    },
    'international_refugees_migrants': {
        'zip': "international_refugees_migrants",
        'csv': "international_refugees_migrants"
    },
    'israeli_wars': {
        'zip': "israeli_wars",
        'csv': "israeli_wars"    
    },
     'prime_ministers': {
        'zip': "prime_ministers",
        'csv': "prime_ministers"    
    },
     'islam_holidays': {
        'zip': "islam_holidays",
        'csv': "islam_holidays"    
    },
     'jewish_holidays': {
        'zip': "jewish_holidays",
        'csv': "jewish_holidays"    
    },
    'pales_national_days': {
        'zip': "pales_national_days",
        'csv': "pales_national_days" 
    }
}

cleaning_files = {
    'terrorism': cleaning_terrorism,
    'israeli_wars': cleaning_israeli_wars,
    'islam_holidays': cleaning_islam_holidays,
    'jewish_holidays': cleaning_jewish_holidays,
    'prime_ministers': cleaning_prime_ministers,
    'pales_national_days': cleaning_pales_national_days
}