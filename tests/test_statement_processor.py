import unittest
from financeanalytics import statementprocessor
import pandas as pd

class TestStatementProcessor(unittest.TestCase):

    def test_standardize_rbc_visa_example_1(self):
        input_data = pd.read_csv("tests/mock_parsed_statements/rbc_visa_example_1.csv")

        expected_output = pd.DataFrame([["JUN13", "AMAZON.CA*AB1CD23E4AMAZON.CAON", 2.22],
                                        ["JUN13", "TIMHORTONS#9999555-555-5555ON", 2.22],
                                        ["JUN14", "UBER*EATSTORONTOON", 99.99],
                                        ["JUN16", "UBERCANADA/UBEREATSTORONTOON", 11.11],
                                        ["JUN16", "PETROCAN-1TAUNTONRDNTORONTOON", 22.22],
                                        ["JUN17", "MCDONALD'S12345TORONTOON", 3.33],
                                        ["JUN24", "PAYMENT-THANKYOU/PAIEMENT-MERCI", -1000.00],
                                        ["JUL03", "UBERCANADA/UBEREATSTORONTOON", 66.66]],
                                       columns=["Date", "Description", "Amount"])

        StatementProcessor = statementprocessor.StatementProcessor()

        actual_output = StatementProcessor

        pd.testing.assert_frame_equal(expected_output, actual_output)

if __name__ == '__main__':
    unittest.main()
