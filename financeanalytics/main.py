from financeanalytics.dataloader import DataLoader
from financeanalytics.dataquality import DataQuality
from financeanalytics.statementprocessor import StatementProcessor

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

    def __init__(self):
        root_input_folder = self.welcome()

        # Load the data
        structured_data = DataLoader().load_data(root_input_folder)

        # Run the DQ analysis
        DataQuality().analyze_data_quality(structured_data)

        # Extract the statements
        import pandas as pd
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        print('Extract Statements Here')

        pdf_filepath = structured_data.iloc[0, :]["Filepath"]
        bank = structured_data.iloc[0, :]["Bank"]
        statement_type = self.determine_statement_type(pdf_filepath)
        StatementProcessor().extract_with_validation(pdf_filepath, bank, statement_type)

if __name__ == '__main__':
    FinanceAnalytics()