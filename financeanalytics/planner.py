import os
import re
import numpy as np
import pandas as pd

class Planner:

    def _find_missing_dates(self, start_date, end_date, all_dates):
        # Convert all days to 01 to ignore inconsistent day of month file names
        normalized_start_date = re.sub("(-(0[1-9]|[12]\d|3[01])$)", "-01", start_date)
        normalized_end_date = re.sub("(-(0[1-9]|[12]\d|3[01])$)", "-01", end_date)
        normalized_all_dates = [re.sub("(-(0[1-9]|[12]\d|3[01])$)", "-01", x) for x in all_dates]

        # Find the gaps in missing -01 dates
        missing_daily_dates = list(pd.date_range(normalized_start_date, normalized_end_date).difference(pd.to_datetime(normalized_all_dates)).strftime('%Y-%m-%d'))
        missing_monthly_dates = [x for x in missing_daily_dates if x[-2:] == "01"]

        return missing_monthly_dates

    def analyze_data_gaps(self, identified_data):

        # Assumes only two suffix columns currently "Date" and "Filepath"
        groupby_columns = list(identified_data.columns)[:-2]

        # Determine range of each collection and list of all dates found
        collection_range = identified_data.groupby(groupby_columns).agg(min_date=('Date', 'min'),
                                                                        max_date=('Date', 'max'),
                                                                        all_dates=('Date', pd.Series.tolist)).reset_index()

        # Determine missing dates in each list
        collection_range["missing_month_gaps"] = collection_range.apply(lambda x: self._find_missing_dates(x.min_date, x.max_date, x.all_dates), axis=1)

        # Print out results to user of analysis
        print("Results of Data Gap Analysis:")
        print(collection_range.loc[:, collection_range.columns != "all_dates"])

        return 0

    def identify_data(self, root_input_folder):

        complete_listing = []
        datestamp_pattern = re.compile("[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])")

        # Used to identify how many subfolder levels are below the root folder
        bank_list_pointer = len(root_input_folder.split(os.sep))

        for root, dir, files in os.walk(root_input_folder):
            path = root.split(os.sep)
            #print((len(path) - 1) * '---', os.path.basename(root))
            for file in files:

                # On first file location determine how many levels deep the folder structure goes
                #number_of_levels = len(path)-bank_list_pointer-1

                #print(len(path) * '---', file)

                # Determine full path location
                full_path_location = os.sep.join(path) + os.sep + file

                date = datestamp_pattern.search(file).group(0)
                #year = date.split('-')[0]
                #month = date.split('-')[1]


                complete_record = path[bank_list_pointer:]
                #complete_record.append(year)
                #complete_record.append(month)
                complete_record.append(date)
                complete_record.append(full_path_location)

                # Add to complete listing
                complete_listing.append(complete_record)

        # After all records obtained
        print("Records compiled...")

        # Convert to dataframe for analysis
        number_of_columns = len(complete_listing[0])

        prefix_column_names = ['Bank']
        suffix_column_names = ['Date', 'Filepath']

        number_of_levels = number_of_columns - len(prefix_column_names) - len(suffix_column_names)
        variable_level_columns = ["Level " + str(x + 1) for x in range(number_of_levels)]

        complete_column_names = prefix_column_names + variable_level_columns + suffix_column_names

        df = pd.DataFrame(complete_listing, columns = complete_column_names)

        return df

    def __init__(self, root_input_folder):
        self.root_input_folder = root_input_folder

        # Debugging
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)

def main():
    print("Shouldn't be running this directly")