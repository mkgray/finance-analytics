import logging
import pdfplumber
import pandas as pd

class StatementProcessor:
    """
    A class used to actually convert Bank pdf statements to text for downstream processing.
    """

    def extract_rbc_chequing_statement(self, pdf_filepath):
        """Extracts a Pandas DataFrame from RBC chequing statements based on a cropped pattern

        :param pdf_filepath:The path to the statement for extracting to dataframe
        :return:Pandas DataFrame with no text preprocessing
        """

        first_page_crop_bounds = (0, 400, 612, 792)

        pdf = pdfplumber.open(pdf_filepath)

        df_all_pages = []

        # Convert each page separately
        for idx, page in enumerate(pdf.pages):
            if idx == 0:
                # Crop first page
                extracted_table_for_page = (page
                                            .crop(first_page_crop_bounds, relative=True)
                                            .extract_table(self.rbc_chequing_table_settings_odd_pages))
            elif (idx%2 == 1):
                # even pages are treated differently than odd pages
                extracted_table_for_page = (page
                                            .extract_table(self.rbc_chequing_table_settings_even_pages))
            else:
                # odd pages
                extracted_table_for_page = (page
                                            .extract_table(self.rbc_chequing_table_settings_odd_pages))
            df_all_pages.append(pd.DataFrame(extracted_table_for_page[1::], columns=self.rbc_chequing_columns))

        # After conversion merge all the df pages into a single table
        return pd.concat(df_all_pages, axis=0).reset_index(drop=True)

    def extract_rbc_visa_statement(self, pdf_filepath):
        """Extracts a Pandas DataFrame from RBC visa statements based on a cropped pattern

        :param pdf_filepath:The path to the statement for extracting to dataframe
        :return:Pandas DataFrame with no text preprocessing
        """

        visa_page_crop_bounds = (55,140,350,598)

        pdf = pdfplumber.open(pdf_filepath)

        df_all_pages = []

        for page in pdf.pages:
            page_raw_extract = page.crop(visa_page_crop_bounds).extract_table(self.rbc_visa_table_settings)

            # Failure to convert to DF indicates empty page, ignore and move to next page
            try:
                page_df = pd.DataFrame(page_raw_extract[1::], columns=self.rbc_visa_columns)
                if page_df["Amount"].str.contains('\$').sum() == 0:
                    # If no "$" character in the whole page it is legal text, dump and move on
                    continue
            except:
                logging.info("Blank page, ignoring")

            df_all_pages.append(page_df)

        # After conversion merge all the df pages into a single table
        merged_df = pd.concat(df_all_pages, axis=0).reset_index(drop=True)

        # Remove all records without a "$" in amount to remove non-transaction lines
        # Also remove 'Amount($)' header records by removing lines with Amount containing ")"
        return merged_df[merged_df["Amount"].str.contains('\$') & ~merged_df["Amount"].str.contains("\)")]

    def __init__(self):

        # Hard coded based on trial and error for now
        self.rbc_chequing_table_settings_odd_pages = {
            "vertical_strategy": "explicit",
            "horizontal_strategy": "lines",
            "explicit_vertical_lines": [45, 85, 300, 400, 500, 595],
        }

        # Hard coded based on trial and error for now
        self.rbc_chequing_table_settings_even_pages = {
            "vertical_strategy": "explicit",
            "horizontal_strategy": "lines",
            "explicit_vertical_lines": [15, 55, 270, 370, 470, 565],
        }

        # Hard coded based on trial and error for now
        self.rbc_visa_table_settings = {
            "vertical_strategy": "explicit",
            "horizontal_strategy": "text",
            "explicit_vertical_lines": [57, 95, 128, 305, 350],
        }

        # Fixed column scheme for RBC chequing
        self.rbc_chequing_columns = ["Date", "Description", "Withdrawals", "Deposits", "Balance"]

        # Fixed column scheme for RBC visa
        self.rbc_visa_columns = ["Transaction Date", "Posting Date", "Activity Description", "Amount"]