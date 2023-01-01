import argparse

from financeanalytics import FinanceAnalytics

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Extract and analyze Bank Statements")

    # Terminal path
    parser.add_argument("-i", "--input_directory", required=True, type=str)

    # Default to the input directory root
    parser.add_argument("-o", "--output_directory", required=False, type=str)

    parser.add_argument("-f", "--output_filename", required=False, type=str, default="output_table")

    parser.add_argument("-x", "--output_extension", required=True, default="xlsx", choices=["csv", "xlsx"])

    args = parser.parse_args()

    # Input quality checks

    # Input should not be a filetype, should be a directory

    # If output is None, default to input location and default filename

    FinanceAnalytics()