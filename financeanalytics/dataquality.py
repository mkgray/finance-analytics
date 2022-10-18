import logging

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

        logging.warning("No verbose stage included yet")

        return data_gaps

    def _compress_structured_data(self, structured_file_listing):
        """Gets the start date and end date for each hierarchy in the detected structure

        :param structured_file_listing:the DataFrame hierarchy and filepath data coming from the DataLoader
        :return:the aggregated data containing start date (month beginning), end date (month beginning), and a listing of all files (month beginning) for every hierarchy
        """

        df_with_extracted_dates = self._extract_month_year_stamps(structured_file_listing)
        compressed_df = self._aggregate_df_analytics(df_with_extracted_dates)

        return compressed_df

    def _extract_month_year_stamps(self, structured_df):
        """Extracts the datestamp for each file in the listing, uses first day of month to make gap analysis easy

        :param structured_df:the DataFrame hierarchy and filepath data coming from the DataLoader
        :return:same DataFrame from input with the addition of datestamps for each file (dated to the beginning of each month for easy gap analysis)
        """
        return 0

    def _aggregate_df_analytics(self, df_with_datestamps):
        """Determines the range and gaps of detected data for all hierarchies

        :param df_with_datestamps:DataFrame containing hierarchies and datestamps for each file (month beginning)
        :return: Aggregated DataFrame with hierarchies, start date (month beginning), end date (month beginning), and collection of all dates (month beginning)
        """

        return 0

    def _identify_data_gaps(self, compressed_data):
        """Identifies the data gaps from windowed data

        :param compressed_data:Aggregated DataFrame with hierarchies, start date (month beginning), end date (month beginning), and collection of all dates (month beginning)
        :return: DataFrame listing all the missing gaps of information needed for every hierarchy detected
        """

        return 0