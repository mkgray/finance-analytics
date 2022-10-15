from financeanalytics.planner import Planner

# TODO: Unit Tests
# TODO: Add proper logging

def welcome():
    print("Welcome to the Financial Planner Application\n(C) Matt Gray 2022")
    print("Please specify the folder location where the data is stored:")
    root_location = "C:\\FinanceData"
    return root_location

if __name__ == '__main__':
    root_input_folder = welcome()

    planner = Planner(root_input_folder)

    identified_data = planner.identify_data(root_input_folder)

    data_gap_results = planner.analyze_data_gaps(identified_data)
