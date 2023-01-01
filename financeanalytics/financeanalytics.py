from dataloader import DataLoader
from dataquality import DataQuality
from statementprocessor import StatementProcessor

from pathlib import Path

import pandas as pd

class FinanceAnalytics:

    def determine_statement_type(self, pdf_filepath):
        """Identifies chequing or visa statement based on filepath (directory or file name)"""
        if 'chequing' in str(pdf_filepath).lower():
            return 'Chequing'
        elif 'visa' in str(pdf_filepath).lower():
            return 'Visa'
        else:
            raise NameError('Filepath does not specify chequing or visa statement type explicitly, please include')

    def extract_statement_data(self, df_record):
        """Extract the transactions from the statement"""
        pdf_filepath = df_record["Filepath"]
        bank = df_record["Bank"]
        statement_type = self.determine_statement_type(pdf_filepath)
        return StatementProcessor().extract_with_validation(pdf_filepath, bank, statement_type)

    def extract_all_statements(self, structured_data):
        """Loops through all statements in the dataframe to extract transactions"""
        total_records = structured_data.shape[0]
        column_names = list(structured_data.columns)

        df_all_statements = []

        # Set the GUI progress bar
        #self.progress_bar["maximum"] = structured_data.shape[0]
        files_processed = 0

        # Iteratively process financial statements
        for index, row in structured_data.iterrows():
            pdf_filepath = row["Filepath"]
            bank = row["Bank"]
            statement_type = self.determine_statement_type(pdf_filepath)

            statement_df = StatementProcessor().extract_with_validation(pdf_filepath, bank, statement_type)

            # Append the hierarchy onto the results
            statement_df[column_names] = row.values

            # Add the statement with hierarchy to the complete dataset
            df_all_statements.append(statement_df)

            # Update the progress bar
            files_processed += 1
            #self.progress_bar["value"] = files_processed
            #self.progress_bar.update()

        # Merge statements into one dataframe
        return pd.concat(df_all_statements, axis=0).reset_index(drop=True)

    def write_output_to_location(self, all_statements, output_dir, output_fname="extracted_transactions", output_format="xlsx"):
        """Outputs the structured transaction data to the users designated output location"""
        output_path = Path(output_dir + '/' + output_fname + '.' + output_format)
        if output_format == "xlsx":
            all_statements.to_excel(output_path, index=False)
        elif output_format == "csv":
            all_statements.to_csv(output_path, index=False)
        else:
            raise ValueError('Import write format specified')

    def run(self, input_dir, output_dir, output_fname="extracted_transactions", output_format="xlsx"):
        """Runs the complete Finance Analytics process, including:
        1) Detect statements
        2) Metadata DQ analysis
        3) Extract transactions
        4) Write output"""

        # Load the data
        structured_data = DataLoader().load_data(input_dir)

        # Run the DQ analysis
        DataQuality().analyze_data_quality(structured_data)

        # Extract the statements and write
        self.write_output_to_location(self.extract_all_statements(structured_data), output_dir, output_fname, output_format)

