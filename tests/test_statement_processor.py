import datetime
import unittest
from financeanalytics import statementprocessor
import pandas as pd

class TestStatementProcessor(unittest.TestCase):

    def test_standardize_rbc_chequing_example_1(self):
        input_data = pd.DataFrame([["", "OpeningBalance", "", "", "1111.11"],
                                   ["12Aug", "Interacpurchase-9999 TEST-CO", "222.22", "", "888.89"],
                                   ["", "ContactlessInteracpurchase-9999\nBATTLEBOX-SQU", "11.11", "", "877.78"],
                                   ["13Aug", "BIGMONEY-NOWHAMMIES", "", "1000.00", ""],
                                   ["", "ContactlessInteracpurchase-9999\nSTARBUCKS#1234", "11.11", "", "1866.67"],
                                   ["26Aug", "BillPayment BIGBILLS", "11.11", "", "1855.56"],
                                   ["4Sep", "Interacpurchase-7777 BIGBOXSTORE#", "22.22", "", ""],
                                   ["", "Interacpurchase-4444 ABCD/EFG#1234", "33.33", "", "1800.01"],
                                   ["", "ContactlessInteracpurchase-8888\nKRUSTYKREME#1", "44.44", "", ""],
                                   ["", "ContactlessInteracpurchase-9876\nTHESTEERSTORE", "55.55", "", "1700.02"],
                                   ["11Sep", "ContactlessInteracpurchase-1234\nTABLEROCKLOBSTER", "6.66", "", ""],
                                   ["", "ContactlessInteracpurchase-1111\nKARTHOUSE", "7.77", "", "1685.59"]],
                                  columns=["Date", "Description", "Withdrawl", "Deposits", "Balance"])

        input_year = int(2020)

        expected_output = pd.DataFrame(
            [[datetime.datetime.strptime("2020-08-12", '%Y-%m-%d'), "Interacpurchase-9999 TEST-CO", -222.22],
             [datetime.datetime.strptime("2020-08-12", '%Y-%m-%d'), "ContactlessInteracpurchase-9999\nBATTLEBOX-SQU", -11.11],
             [datetime.datetime.strptime("2020-08-13", '%Y-%m-%d'), "BIGMONEY-NOWHAMMIES", 1000.00],
             [datetime.datetime.strptime("2020-08-13", '%Y-%m-%d'), "ContactlessInteracpurchase-9999\nSTARBUCKS#1234", -11.11],
             [datetime.datetime.strptime("2020-08-26", '%Y-%m-%d'), "BillPayment BIGBILLS", -11.11],
             [datetime.datetime.strptime("2020-09-04", '%Y-%m-%d'), "Interacpurchase-7777 BIGBOXSTORE#", -22.22],
             [datetime.datetime.strptime("2020-09-04", '%Y-%m-%d'), "Interacpurchase-4444 ABCD/EFG#1234", -33.33],
             [datetime.datetime.strptime("2020-09-04", '%Y-%m-%d'), "ContactlessInteracpurchase-8888\nKRUSTYKREME#1", -44.44],
             [datetime.datetime.strptime("2020-09-04", '%Y-%m-%d'), "ContactlessInteracpurchase-9876\nTHESTEERSTORE", -55.55],
             [datetime.datetime.strptime("2020-09-11", '%Y-%m-%d'), "ContactlessInteracpurchase-1234\nTABLEROCKLOBSTER", -6.66],
             [datetime.datetime.strptime("2020-09-11", '%Y-%m-%d'), "ContactlessInteracpurchase-1111\nKARTHOUSE", -7.77]],
            columns=["Date", "Description", "Amount"])

        StatementProcessor = statementprocessor.StatementProcessor()

        actual_output = StatementProcessor.standardized_rbc_chequing_transactions(input_data, input_year)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_standardize_rbc_visa_example_1(self):
        input_data = pd.DataFrame([["JUN13", "JUN14", "AMAZON.CA*AB1CD23E4AMAZON.CAON", "$11.11"],
                                   ["JUN13", "JUN13", "TIMHORTONS#9999555-555-5555ON", "$2.22"],
                                   ["JUN14", "JUN15", "UBER*EATSTORONTOON", "$99.99"],
                                   ["JUN16", "JUN17", "UBERCANADA/UBEREATSTORONTOON", "$11.11"],
                                   ["JUN16", "JUN17", "PETROCAN-1TAUNTONRDNTORONTOON", "$22.22"],
                                   ["JUN17", "JUN20", "MCDONALD'S12345TORONTOON", "$3.33"],
                                   ["JUN24", "JUN27", "PAYMENT-THANKYOU/PAIEMENT-MERCI", "-$1,000.00"],
                                   ["", "", "CREDITBALANCE", "-$532.75"],
                                   ["JUL03", "JUL04", "UBERCANADA/UBEREATSTORONTOON", "$66.66"],
                                   ["", "", "CREDITBALANCE", "-$532.75"]],
                                  columns=["Transaction Date", "Posting Date", "Activity Description", "Amount"])

        input_year = int(2020)

        expected_output = pd.DataFrame([[datetime.datetime.strptime("2020-06-13", '%Y-%m-%d'), "AMAZON.CA*AB1CD23E4AMAZON.CAON", 11.11],
                                        [datetime.datetime.strptime("2020-06-13", '%Y-%m-%d'), "TIMHORTONS#9999555-555-5555ON", 2.22],
                                        [datetime.datetime.strptime("2020-06-14", '%Y-%m-%d'), "UBER*EATSTORONTOON", 99.99],
                                        [datetime.datetime.strptime("2020-06-16", '%Y-%m-%d'), "UBERCANADA/UBEREATSTORONTOON", 11.11],
                                        [datetime.datetime.strptime("2020-06-16", '%Y-%m-%d'), "PETROCAN-1TAUNTONRDNTORONTOON", 22.22],
                                        [datetime.datetime.strptime("2020-06-17", '%Y-%m-%d'), "MCDONALD'S12345TORONTOON", 3.33],
                                        [datetime.datetime.strptime("2020-06-24", '%Y-%m-%d'), "PAYMENT-THANKYOU/PAIEMENT-MERCI", -1000.00],
                                        [datetime.datetime.strptime("2020-07-03", '%Y-%m-%d'), "UBERCANADA/UBEREATSTORONTOON", 66.66]],
                                       columns=["Date", "Description", "Amount"])

        StatementProcessor = statementprocessor.StatementProcessor()

        actual_output = StatementProcessor.standardized_rbc_visa_transactions(input_data, input_year)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_standardize_rbc_visa_rollover_year(self):
        input_data = pd.DataFrame([["DEC13", "DEC14", "AMAZON.CA*AB1CD23E4AMAZON.CAON", "$11.11"],
                                   ["DEC13", "DEC13", "TIMHORTONS#9999555-555-5555ON", "$2.22"],
                                   ["DEC14", "DEC15", "UBER*EATSTORONTOON", "$99.99"],
                                   ["DEC16", "DEC17", "UBERCANADA/UBEREATSTORONTOON", "$11.11"],
                                   ["DEC16", "DEC17", "PETROCAN-1TAUNTONRDNTORONTOON", "$22.22"],
                                   ["DEC17", "DEC20", "MCDONALD'S12345TORONTOON", "$3.33"],
                                   ["DEC24", "DEC27", "PAYMENT-THANKYOU/PAIEMENT-MERCI", "-$1,000.00"],
                                   ["", "", "CREDITBALANCE", "-$532.75"],
                                   ["JAN03", "JAN04", "UBERCANADA/UBEREATSTORONTOON", "$66.66"],
                                   ["", "", "CREDITBALANCE", "-$532.75"]],
                                  columns=["Transaction Date", "Posting Date", "Activity Description", "Amount"])

        input_year = int(2020)

        expected_output = pd.DataFrame([[datetime.datetime.strptime("2019-12-13", '%Y-%m-%d'), "AMAZON.CA*AB1CD23E4AMAZON.CAON", 11.11],
                                        [datetime.datetime.strptime("2019-12-13", '%Y-%m-%d'), "TIMHORTONS#9999555-555-5555ON", 2.22],
                                        [datetime.datetime.strptime("2019-12-14", '%Y-%m-%d'), "UBER*EATSTORONTOON", 99.99],
                                        [datetime.datetime.strptime("2019-12-16", '%Y-%m-%d'), "UBERCANADA/UBEREATSTORONTOON", 11.11],
                                        [datetime.datetime.strptime("2019-12-16", '%Y-%m-%d'), "PETROCAN-1TAUNTONRDNTORONTOON", 22.22],
                                        [datetime.datetime.strptime("2019-12-17", '%Y-%m-%d'), "MCDONALD'S12345TORONTOON", 3.33],
                                        [datetime.datetime.strptime("2019-12-24", '%Y-%m-%d'), "PAYMENT-THANKYOU/PAIEMENT-MERCI", -1000.00],
                                        [datetime.datetime.strptime("2020-01-03", '%Y-%m-%d'), "UBERCANADA/UBEREATSTORONTOON", 66.66]],
                                       columns=["Date", "Description", "Amount"])

        StatementProcessor = statementprocessor.StatementProcessor()

        actual_output = StatementProcessor.standardized_rbc_visa_transactions(input_data, input_year)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_convert_date_to_datestamps_1(self):
        input_string = "JAN01"
        input_year = 2020

        expected_output = datetime.datetime.strptime("2020-01-01", '%Y-%m-%d')

        StatementProcessor = statementprocessor.StatementProcessor()

        actual_output = StatementProcessor._convert_date_to_datestamps(input_string, input_year)

        self.assertEqual(expected_output, actual_output)

    def test_convert_date_to_datestamps_2(self):
        # Test leap year date
        input_string = "FEB29"
        input_year = 2020

        expected_output = datetime.datetime.strptime("2020-02-29", '%Y-%m-%d')

        StatementProcessor = statementprocessor.StatementProcessor()

        actual_output = StatementProcessor._convert_date_to_datestamps(input_string, input_year)

        self.assertEqual(expected_output, actual_output)

    def test_convert_date_to_datestamps_3(self):
        input_string = "DEC31"
        input_year = 1111

        expected_output = datetime.datetime.strptime("1111-12-31", '%Y-%m-%d')

        StatementProcessor = statementprocessor.StatementProcessor()

        actual_output = StatementProcessor._convert_date_to_datestamps(input_string, input_year)

        self.assertEqual(expected_output, actual_output)

    def test_invalid_date_conversion(self):
        # Test on Feb 29 for non-leap year
        input_string = "FEB29"
        input_year = 2021

        StatementProcessor = statementprocessor.StatementProcessor()

        with self.assertRaises(Exception) as context:
            StatementProcessor._convert_date_to_datestamps(input_string, input_year)

        self.assertTrue('day is out of range for month' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
