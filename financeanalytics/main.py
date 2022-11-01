from financeanalytics.dataloader import DataLoader
from financeanalytics.dataquality import DataQuality
from financeanalytics.statementprocessor import StatementProcessor


# TODO: Unit Tests
# TODO: Add proper logging

def welcome():
    print("Welcome to the Financial Planner Application\n(C) Matt Gray 2022")
    print("Please specify the folder location where the data is stored:")
    root_location = "C:\\FinanceData"
    return root_location

if __name__ == '__main__':
    root_input_folder = welcome()

    # Load the data
    structured_data = DataLoader().load_data(root_input_folder)

    # Run the DQ analysis
    DataQuality().analyze_data_quality(structured_data)

    # Extract the statements
    print('Extract Statements Here')
