from financeanalytics.dataloader import DataLoader
from financeanalytics.dataquality import DataQuality
from financeanalytics.statementprocessor import StatementProcessor

from pathlib import Path

import logging

import pandas as pd

class FinanceAnalytics:

    def welcome(self):
        print("Welcome to the Financial Planner Application\n(C) Matt Gray 2022")
        print("Please specify the folder location where the data is stored:")
        root_location = "C:\\FinanceData"
        return root_location

    def determine_statement_type(self, pdf_filepath):
        if 'chequing' in str(pdf_filepath).lower():
            return 'Chequing'
        elif 'visa' in str(pdf_filepath).lower():
            return 'Visa'
        else:
            raise NameError('Filepath does not specify chequing or visa statement type explicitly, please include')

    def extract_statement_data(self, df_record):

        pdf_filepath = df_record["Filepath"]
        bank = df_record["Bank"]
        statement_type = self.determine_statement_type(pdf_filepath)
        return StatementProcessor().extract_with_validation(pdf_filepath, bank, statement_type)

    def extract_all_statements(self, structured_data):
        total_records = structured_data.shape[0]
        column_names = list(structured_data.columns)

        df_all_statements = []

        for index, row in structured_data.iterrows():
            pdf_filepath = row["Filepath"]
            bank = row["Bank"]
            statement_type = self.determine_statement_type(pdf_filepath)

            statement_df = StatementProcessor().extract_with_validation(pdf_filepath, bank, statement_type)

            # Append the hierarchy onto the results
            statement_df[column_names] = row.values

            # Add the statement with hierarchy to the complete dataset
            df_all_statements.append(statement_df)

            logging.warning("Processed file {idx} of {max_idx}, ({prcnt}% Complete): {fname}".format(idx=index + 1, max_idx=total_records, prcnt=round((float(index + 1) / total_records) * 100, 2), fname=pdf_filepath))

        # Merge statements into one dataframe
        return pd.concat(df_all_statements, axis=0).reset_index(drop=True)

    def write_output_to_location(self, all_statements, root_location):
        output_path = Path(root_location + '/extracted_transactions.xlsx')
        all_statements.to_excel(output_path, index=False)

    def __init__(self):
        root_input_folder = self.welcome()

        # Load the data
        structured_data = DataLoader().load_data(root_input_folder)

        # Run the DQ analysis
        DataQuality().analyze_data_quality(structured_data)

        # Extract the statements and write
        self.write_output_to_location(self.extract_all_statements(structured_data), root_input_folder)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.WARNING)
    complete_df = FinanceAnalytics()