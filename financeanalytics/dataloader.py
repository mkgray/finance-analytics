import logging
import re

import pandas as pd

from pathlib import Path

# TODO: Add graphical interface for root folder selection

class DataLoader:
    """
    A class used to detect and do basic cleaning of the file and folder hierarchy the user points to.
    """

    def load_data(self, root_folder):
        """Detects and populates all relevant data for further analysis.

        Detects the entire file and folder hierarchy, and performs basic cleaning operations:
        - Whitelist only Banks that are supported (have compatible PDF statements for downstream analysis)
        - Remove empty file folders
        - Remove non-supported file formats (currently all formats except pdfs)

        Data gets converted into a pandas dataframe format for more advanced Data Quality checking, which requires
        handling of folder hierarchy case sensitivity in this function

        :param root_folder:  root location where hierarchy and statement files begin
        :type root_folder: string
        :return: DataFrame
        """
        raw_list = self._detect_relevant_files(root_folder)
        supported_bank_files = self._remove_unsupported_banks(raw_list)
        cleaned_file_list = self._remove_files_missing_dates(supported_bank_files)
        structured_data = self._structure_cleaned_file_listing(cleaned_file_list, root_folder)
        return structured_data

    def _structure_cleaned_file_listing(self, file_list, root_folder):
        """Converts list of files to be parsed into a structured format for initial data quality analysis

        :param file_list: list of all files to be structured
        :param root_folder: The parent folder to use as the starting point for hierarchy
        :return: DataFrame of structure file breakdown including Bank, Hierarchy of Levels, and Filepath
        """

        # Convert directly to a DataFrame and drop the root folder (start) and filename (end)
        df = pd.DataFrame([x.parts[len(Path(root_folder).parts):-1] for x in file_list])

        # Set up proper column names starting with Bank and Hierarchy Levels
        number_of_hierarchy_levels = len(df.columns) - 1
        hierarchy_columns = ["Bank"]
        hierarchy_columns.extend(["Level " + str(x + 1) for x in range(number_of_hierarchy_levels)])
        df.columns = hierarchy_columns

        # Convert all values to uppercase for case insensitivity of analytics
        df = df.apply(lambda x: x.astype(str).str.upper())

        logging.info("Detected {nhierarchy} hierarchy levels in data".format(nhierarchy = number_of_hierarchy_levels))

        # Manually convert Filepaths to Path format due to Pandas using OS specific format
        df["Filepath"] = file_list

        logging.info("Resultant structured table:")
        logging.info(df)

        return df

    def _remove_files_missing_dates(self, list_of_files):
        """Removes files which do not contain a datestamp for structured handling

        :param list_of_files: list of all files detected in locatoin specified by user
        :return: list of Path files for only files which contain date stamps
        """

        datestamp_pattern = re.compile("[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])")

        return [x for x in list_of_files if re.search(datestamp_pattern, str(x))]

    def _remove_unsupported_banks(self, list_of_all_filepaths):
        """Removes any PDF folders and files which are not supported downstream (based on Banks supported)

        :param raw_list: list of all files and folders detected in location specified by user
        :return: list of Path files for only supported banks
        """

        list_of_all_supported_banks = self.supported_banks

        # Converts all filepath folders into pieces for comparison against the supported bank whitelist
        # All filepaths are converted to lowercase to make the Bank folder case insensitive

        filtered_files = [file for file in list_of_all_filepaths if any(
            whitelisted_bank in [path_folder.lower() for path_folder in list(file.parts)] for whitelisted_bank in
            list_of_all_supported_banks)]

        # Output as info for user if needed
        logging.info("Files Detected:")
        [logging.info(x) for x in filtered_files]

        return filtered_files

    def _detect_relevant_files(self, root_folder):
        """Identifies all relevant files for analysis.

        Detects and lists all pdf files which will potentially be used in downstream files

        :param root_folder: root location where hierarchy and statement files begin
        :type root_folder: string
        :return: list of Path objects to file locations
        """
        found_files = [x for x in Path(root_folder).glob('**/*.pdf')]

        # Output as info for user if needed
        logging.info("Files Detected:")
        [logging.info(x) for x in found_files]

        return found_files

    def __init__(self, supported_banks=["rbc"]):
        self.supported_banks = supported_banks
