import datetime
import logging
import pdfplumber
import re
import numpy as np
import pandas as pd

class StatementProcessor:
    """
    A class used to actually convert Bank pdf statements to text for downstream processing.
    """

    def extract_with_validation(self, pdf_filepath, bank, statement_type):
        """Extracts transactions from a statement and validates extraction successful

        This function extracts statement metadata (year of last transaction, opening balance, closing balance), extracts
        the transactions, then validates the transactions against the opening and closing balance to ensure all
        transactions were successfully pulled.

        This function is applied to one statement and does not aggregate across statements, to be performed by a
        separate function.

        :param pdf_filepath:The path to the file for loading
        :param bank: The Bank the statement comes from
        :param statement_type: The type of statement (Chequing, Visa)
        :return: DataFrame of the transaction listing
        """

        # Extract the metadata
        (year_of_last_transaction, opening_balance, closing_balance) = self.extract_statement_metadata(pdf_filepath, bank, statement_type)

        # Extract the transactions
        if bank == "RBC":
            if statement_type == "Chequing":
                transactions = self.standardized_rbc_chequing_transactions(self.extract_rbc_chequing_statement(pdf_filepath), year_of_last_transaction)
            elif statement_type == "Visa":
                transactions = self.standardized_rbc_visa_transactions(self.extract_rbc_visa_statement(pdf_filepath), year_of_last_transaction)

        # Validate the transactions
        self.validate_transactions(transactions, opening_balance, closing_balance)

        # Return the transactions if validated
        return transactions

    def validate_transactions(self, transactions, opening_balance, closing_balance):
        """Validates the transactions found in a Bank statement against the opening and closing balance found in the
        statement. Errors would indicate that the transaction list was not fully pulled (or the opening/closing balance
        were not detected correctly)

        :param transactions:DataFrame containing transactions for one Bank statement in standardized format
        :param opening_balance: The opening balance of the Bank statement as detected through the metadata function
        :param closing_balance: The closing balance of the Bank statement as detected through the metadata function
        :return:
        """

        # Use np.around() to compensate for miniscule rounding errors caused by using floats
        return closing_balance == (opening_balance+np.around(transactions["Amount"].sum(), 2))

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

            # Ignore empty pages
            if extracted_table_for_page is not None:
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

            if page_df is not None:
                df_all_pages.append(page_df)

        # After conversion merge all the df pages into a single table
        merged_df = pd.concat(df_all_pages, axis=0).reset_index(drop=True)

        # Remove all records without a "$" in amount to remove non-transaction lines
        # Also remove 'Amount($)' header records by removing lines with Amount containing ")"
        return merged_df[merged_df["Amount"].str.contains('\$') & ~merged_df["Amount"].str.contains("\)")]

    def standardized_rbc_chequing_transactions(self, transaction_df, year_of_last_transaction):
        """Converts extract of rbc chequing to a standard format for aggregation and analysis

        :param transactions: The DataFrame of transactions pulled from an rbc visa statement
        :param year_of_last_transaction: The year that the statement ends for
        :return: DataFrame of transactions in common format
        """

        # Used for safety in df manipulation
        transactions = transaction_df.copy(deep=True)

        # Remove records without either a deposit or a withdrawl
        transactions = transactions[~(((transactions["Deposits"]=="")|(transactions["Deposits"].isna()))
                                      &((transactions["Withdrawals"]=="")|(transactions["Withdrawals"].isna())))]

        # Propagate dates when multiple transactions occur on same day
        transactions["Date"] = transactions["Date"].replace("", np.nan).ffill(axis=0)

        # Merge withdrawls and deposits into one column
        transactions["Deposits"] = transactions["Deposits"].str.replace(",", "").replace("", np.nan).fillna(0).astype(float)
        transactions["Withdrawals"] = transactions["Withdrawals"].str.replace(",", "").replace("", np.nan).fillna(0).astype(float)
        transactions["Amount"] = transactions["Deposits"] - transactions["Withdrawals"]

        # Extract relevant columns
        standard_column_df = self._standardize_preprocessed_table(transactions,self.column_mapping_for_standardization['RBC']['Chequing'])

        # Prepare Date to match style of standard input for conversion to datetime object
        standard_column_df["Date"] = standard_column_df["Date"].apply(lambda x:"".join((x[-3:].upper(), x[:-3].zfill(2))))

        # If transactions for the statement include January, then the month period includes rollover and Dec must be adjusted one year back
        return self._standardize_date_columns(standard_column_df, year_of_last_transaction).reset_index(drop=True)

    def _standardize_date_columns(self, transactions, year_of_last_transaction):
        """Converts 'JAN01'-like dates to datetime objects and compensates for statements that roll the year over

        :param transactions: List of transactions with Date field set up like 'JAN01'
        :param year_of_last_transaction: The integer year of the last transaction in the statement
        :return: DataFrame with Date column as datetime
        """

        transactions["Date"] = transactions["Date"].apply(lambda x: self._convert_date_to_datestamps(x, year_of_last_transaction))

        return self._adjust_dates_for_rollover(transactions)

    def _adjust_dates_for_rollover(self, standard_column_df):
        """Adjust December dates back one year if the statement includes January transactions

        :param dates: The pandas Series list of all dates
        :return: A pandas Series with December dates shifted one year back if last transaction includes January month
        """
        if any(standard_column_df["Date"].dt.month == 1):
            standard_column_df.loc[standard_column_df["Date"].dt.month == 12, "Date"] = \
            standard_column_df[standard_column_df["Date"].dt.month == 12]["Date"] - pd.DateOffset(years=1)

        return standard_column_df

    def standardized_rbc_visa_transactions(self, transactions, year_of_last_transaction):
        """Converts extract of rbc visa to a standard format for aggregation and analysis

        :param transactions: The DataFrame of transactions pulled from an rbc visa statement
        :param year_of_last_transaction: The year that the statement ends for
        :return: DataFrame of transactions in common format
        """

        standard_column_df = self._standardize_preprocessed_table(transactions, self.column_mapping_for_standardization['RBC']['Visa'])

        # Convert amounts to float
        standard_column_df["Amount"] = standard_column_df["Amount"].apply(lambda x: float(x.replace('$', '').replace(',', '')))

        # If transactions for the statement include January, then the month period includes rollover and Dec must be adjusted one year back
        return self._standardize_date_columns(standard_column_df, year_of_last_transaction).reset_index(drop=True)

    def _standardize_preprocessed_table(self, transactions, column_mapping):
        """Performs all standardization methods from Bank statement DataFrames that have been preprocesses to easily streamline standardization.

        Standardized preprocessed tables include mapping and filtering for only columns included in the standard table for downstream analysis, as well as removal of records that contain empty date values

        :param transactions: Preprocessed Bank statement DataFrame
        :param column_mapping: Dictionary which maps the columns in the Bank statement to standard columns, typically comes from the class mapping dict
        :return: DataFrame with column-level filtering to only pass mapped columns and row-level filtering for only transactions with dates
        """

        return self._drop_records_without_date(self._standardize_columns_in_df(transactions, column_mapping))

    def _standardize_columns_in_df(self, transactions, column_mapping):
        """Maps different bank statement fields to the standard fields for analysis.
        Also removes all non-standardized fields to reduce complexity of downstream handling

        :param transactions:Listing of all transactions from any Bank statement
        :param column_mapping:Mapping of which fields for this Bank statement map to the standard fields
        :return:DataFrame with no record level filtering, but column filtering for standardized DataFrame output
        """
        transactions.rename(columns=column_mapping, inplace=True)

        return transactions[column_mapping.values()]

    def _drop_records_without_date(self, transactions):
        """Filters records without a Date

        :param transactions:DataFrame of transactions on standard column schema
        :return:DataFrame filtered for only records with a Date
        """

        # Drop records that have no date (visa no date indicates balance statements)
        return transactions.replace('', np.nan).dropna(subset=["Date"]).reset_index(drop=True)

    def _convert_date_to_datestamps(self, date_string, year):
        """Converts MMMDD statement transaction date format to string

        :param date_string: String containing transaction date as MMMDD using abbreviated month name
        :param year: The year to tag to the transaction
        :return: Datetime type of the transaction date
        """

        month_mapping = {
            "JAN": "01",
            "FEB": "02",
            "MAR": "03",
            "APR": "04",
            "MAY": "05",
            "JUN": "06",
            "JUL": "07",
            "AUG": "08",
            "SEP": "09",
            "OCT": "10",
            "NOV": "11",
            "DEC": "12",
        }

        # Split into pieces and join as a single string for conversion
        return datetime.datetime.strptime('-'.join((str(year), month_mapping[date_string[:3]], date_string[-2:])), '%Y-%m-%d')


    def extract_statement_metadata(self, pdf_filepath, bank, account_type):
        """Extracts the ending transaction year, starting balance, and ending balance for data completion.

        This function extracts raw text from the first page of each statement and uses regex to pull the year of the
        final transaction (used for analytics spanning more than one year), and the starting/ending balances (for
        validation step after pulling all transactions)

        :return:Tuple of (year, starting_balance, ending_balance)
        """

        pdf = pdfplumber.open(pdf_filepath)
        first_page_text = pdf.pages[0].extract_text()

        year_of_last_transaction = int(re.search(self.regex_statements[bank][account_type]['last_transaction_date'], first_page_text).groups()[-1])

        # If starting balance regex doesn't work it is likely the opening of a new account
        try:
            starting_balance = float(re.search(self.regex_statements[bank][account_type]['starting_balance'], first_page_text).groups()[-1].replace("$","").replace(",", ""))
        except:
            starting_balance = float(0)

        ending_balance = float(re.search(self.regex_statements[bank][account_type]['ending_balance'], first_page_text).groups()[-1].replace("$","").replace(",", ""))

        return (year_of_last_transaction, starting_balance, ending_balance)

    def __init__(self):

        # Store all regex statements for metadata parsing
        self.regex_statements = {
            'RBC': {
                'Chequing': {
                    'last_transaction_date':  r"From ?\w*,\w*,(\d{4})",
                    'starting_balance': r"Your ?opening ?balance ?on ?\w*, ?\d* ?(-?\$?.*)",
                    'ending_balance': r"Your ?closing ?balance ?on ?\w*, ?\d* ?=?(-?\$?.*)",
                },
                'Visa': {
                    'last_transaction_date': r"STATEMENT ?FROM ?\w*,(\d{4})",
                    'starting_balance': r"PREVIOUS ?STATEMENT ?BALANCE ?(-?\$?[0-9,.]*)",
                    'ending_balance': r"(CREDIT ?BALANCE ?|NEW ?BALANCE ?)(-?\$?[0-9,.]*)",
                }
            }
        }

        self.column_mapping_for_standardization = {
            'RBC': {
                'Chequing': {
                    "Date": "Date",
                    "Description": "Description",
                    "Amount": "Amount",
                },
                'Visa': {
                    "Transaction Date": "Date",
                    "Activity Description": "Description",
                    "Amount": "Amount",
                }
            }
        }

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