import logging
from pathlib import Path


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
        raw_list = self._detect_all_files_folders(root_folder)
        supported_bank_files = self._remove_unsupported_banks(raw_list)
        structured_data = self._structure_cleaned_file_listing(supported_bank_files)
        cleaned_structured_data = self._clean_structured_data(structured_data)
        return cleaned_structured_data

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
