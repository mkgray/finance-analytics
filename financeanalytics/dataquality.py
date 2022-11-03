import logging
import re

import pandas as pd

class DataQuality:
    """
    A class used to identify data quality issues related to metadata (hierarchies and missing data pieces)
    """

    def analyze_data_quality(self, structured_file_listing):
        """

        :param structured_file_listing:the DataFrame hierarchy and filepath data coming from the DataLoader
        :return:
        """

        compressed_data = self._compress_structured_data(structured_file_listing)
        data_gaps = self._identify_data_gaps(compressed_data)

        self._print_diagnostics(data_gaps)

        logging.warning("No verbose stage included yet")

        return data_gaps

    def _compress_structured_data(self, structured_file_listing):
        """Gets the start date and end date for each hierarchy in the detected structure

        :param structured_file_listing:the DataFrame hierarchy and filepath data coming from the DataLoader
        :return:the aggregated data containing start date (month beginning), end date (month beginning), and a listing of all files (month beginning) for every hierarchy
        """

        df_with_extracted_dates = self._extract_month_year_stamps(structured_file_listing)
        deduplicated_data = self._remove_duplicate_references(df_with_extracted_dates)
        compressed_df = self._aggregate_df_analytics(deduplicated_data)

        return compressed_df

    def _extract_month_year_stamps(self, structured_df):
        """Extracts the datestamp for each file in the listing, uses first day of month to make gap analysis easy

        :param structured_df:the DataFrame hierarchy and filepath data coming from the DataLoader
        :return:same DataFrame from input with the addition of datestamps for each file (dated to the beginning of each month for easy gap analysis)
        """

        datestamp_pattern = re.compile("[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])")

        # Extract the datestamp and change day to beginning of month
        structured_df["MonthStamp"] = structured_df["Filepath"].apply(
            lambda x: datestamp_pattern.search(str(x)).group(0)[:-2] + '01')

        return structured_df

    def _aggregate_df_analytics(self, df_with_datestamps):
        """Determines the range and gaps of detected data for all hierarchies

        :param df_with_datestamps:DataFrame containing hierarchies and datestamps for each file (month beginning)
        :return: Aggregated DataFrame with hierarchies, start date (month beginning), end date (month beginning), and collection of all dates (month beginning)
        """

        # Assumes only two suffix columns currently "Date" and "Filepath"
        # Determine range of each collection and list of all dates found
        return (df_with_datestamps
                .groupby(list(df_with_datestamps.columns)[:-2])
                .agg(min_date=('MonthStamp', 'min'),
                     max_date=('MonthStamp', 'max'),
                     all_dates=('MonthStamp', pd.Series.tolist)).reset_index())

    def _identify_data_gaps(self, compressed_data):
        """Identifies the data gaps from windowed data

        :param compressed_data:Aggregated DataFrame with hierarchies, start date (month beginning), end date (month beginning), and collection of all dates (month beginning)
        :return: DataFrame listing all the missing gaps of information needed for every hierarchy detected
        """

        compressed_data["all_gaps"] = compressed_data.apply(
            lambda x: self.__find_missing_dates(x.min_date, x.max_date, x.all_dates), axis=1)

        return compressed_data

    def _remove_duplicate_references(self, structured_data_with_monthstamp):
        """Removes duplicate monthstamps from a hierarchy if folder type insensitivity causes case to exist

        :param structured_data_with_monthstamp:DataFrame containing hierarchies and datestamps for each file (month beginning)
        :return:DataFrame with duplicate components removed
        """

        # Deduplicate based on Bank and level hierarchy plus the monthstamp found
        column_names = list(structured_data_with_monthstamp.columns)[:-2] + ['MonthStamp']

        return structured_data_with_monthstamp.drop_duplicates(subset=column_names, keep='first').reset_index(drop=True)

    def __find_missing_dates(self, start_date, end_date, all_dates):
        missing_daily_dates = list(pd.date_range(start_date, end_date).difference(pd.to_datetime(all_dates)).strftime('%Y-%m-%d'))
        missing_monthly_dates = [x for x in missing_daily_dates if x[-2:] == "01"]
        return missing_monthly_dates

    def _print_diagnostics(self, data_gaps):
        """Prints to console the basic data quality analysis for user determination to continue or not

        :param data_gaps: DataFrame listing all the missing gaps of information needed for every hierarchy detected
        :return:
        """

        data_gaps.apply(lambda x: self.__data_quality_record_diagnostics(x), axis=1)

        return 0
    def __data_quality_record_diagnostics(self, x):
        print("\n")
        print("Hierarchy: {}".format(list(x.index[:-4])))
        print("First Month-Year of Data: {}".format(x["min_date"]))
        print("Last Month-Year of Data: {}".format(x["max_date"]))
        print("Detected Month(s)-Year(s) of Data: {}".format(x["all_dates"]))
        print("Missing Month(s)-Year(s) of Data: {}".format(x["all_gaps"]))
        return 0