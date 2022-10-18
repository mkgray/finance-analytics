import unittest
from financeanalytics import dataquality
from pathlib import Path
import pandas as pd

class TestDataQuality(unittest.TestCase):

    def test_extract_month_stamp_bank_only_no_gaps(self):

        input_data = pd.DataFrame([["RBC", "root_folder/RBC/Statement 2000-01-06.pdf"],
                                   ["RBC", "root_folder/RBC/Statement 2000-02-09.pdf"],
                                   ["RBC", "root_folder/RBC/Statement 2000-03-13.pdf"],
                                   ["RBC", "root_folder/RBC/Statement 2000-04-06.pdf"],
                                   ["RBC", "root_folder/RBC/Statement 2000-05-08.pdf"]],
                                  columns=["Bank", "Filepath"])

        expected_output = pd.DataFrame([["RBC", "2000-01-01", "root_folder/RBC/Statement 2000-01-06.pdf"],
                                        ["RBC", "2000-02-01", "root_folder/RBC/Statement 2000-02-09.pdf"],
                                        ["RBC", "2000-03-01", "root_folder/RBC/Statement 2000-03-13.pdf"],
                                        ["RBC", "2000-04-01", "root_folder/RBC/Statement 2000-04-06.pdf"],
                                        ["RBC", "2000-05-01", "root_folder/RBC/Statement 2000-05-08.pdf"]],
                                  columns=["Bank", "MonthStamp", "Filepath"])

        DataQuality = dataquality.DataQuality()

        actual_output = DataQuality._extract_month_year_stamps(input_data)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_extract_month_stamp_bank_only_with_gaps(self):

        input_data = pd.DataFrame([["RBC", "root_folder/RBC/Statement 2000-01-06.pdf"],
                                   ["RBC", "root_folder/RBC/Statement 2000-03-13.pdf"],
                                   ["RBC", "root_folder/RBC/Statement 2000-05-08.pdf"]],
                                  columns=["Bank", "Filepath"])

        expected_output = pd.DataFrame([["RBC", "2000-01-01", "root_folder/RBC/Statement 2000-01-06.pdf"],
                                        ["RBC", "2000-03-01", "root_folder/RBC/Statement 2000-03-13.pdf"],
                                        ["RBC", "2000-05-01", "root_folder/RBC/Statement 2000-05-08.pdf"]],
                                  columns=["Bank", "MonthStamp", "Filepath"])

        DataQuality = dataquality.DataQuality()

        actual_output = DataQuality._extract_month_year_stamps(input_data)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_extract_month_stamp_two_levels(self):

        input_data = pd.DataFrame([["RBC", "A", "A-1", "root_folder/RBC/A/A-1/Statement 2000-01-06.pdf"],
                                   ["RBC", "A", "A-1", "root_folder/RBC/A/A-1/Statement 2000-02-09.pdf"],
                                   ["RBC", "A", "A-2", "root_folder/RBC/A/A-2/Statement 2000-03-13.pdf"],
                                   ["RBC", "A", "A-2", "root_folder/RBC/A/A-2/Statement 2000-04-06.pdf"],
                                   ["RBC", "A", "A-3", "root_folder/RBC/A/A-3/Statement 2000-05-08.pdf"]],
                                  columns=["Bank", "Level 1", "Level 2", "Filepath"])

        expected_output = pd.DataFrame([["RBC", "A", "A-1", "2000-01-01", "root_folder/RBC/A/A-1/Statement 2000-01-06.pdf"],
                                        ["RBC", "A", "A-1", "2000-02-01", "root_folder/RBC/A/A-1/Statement 2000-02-09.pdf"],
                                        ["RBC", "A", "A-2", "2000-03-01", "root_folder/RBC/A/A-2/Statement 2000-03-13.pdf"],
                                        ["RBC", "A", "A-2", "2000-04-01", "root_folder/RBC/A/A-2/Statement 2000-04-06.pdf"],
                                        ["RBC", "A", "A-3", "2000-05-01", "root_folder/RBC/A/A-3/Statement 2000-05-08.pdf"]],
                                  columns=["Bank", "Level 1", "Level 2", "Filepath"])

        DataQuality = dataquality.DataQuality()

        actual_output = DataQuality._extract_month_year_stamps(input_data)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_extract_month_stamp_five_levels_with_nones(self):

        input_data = pd.DataFrame([["RBC", "A", "B", "C", "D", "E", "root_folder/RBC/A/A-1/Statement 2000-01-06.pdf"],
                                        ["RBC", "A", "B", "C", "D", "NONE", "root_folder/RBC/A/A-1/Statement 2000-02-09.pdf"],
                                        ["RBC", "A", "B", "C", "NONE", "NONE", "root_folder/RBC/A/A-2/Statement 2000-03-13.pdf"],
                                        ["RBC", "A", "B", "NONE", "NONE", "NONE", "root_folder/RBC/A/A-2/Statement 2000-04-06.pdf"],
                                        ["RBC", "A", "NONE", "NONE", "NONE", "NONE", "root_folder/RBC/A/A-3/Statement 2000-05-08.pdf"],
                                        ["RBC", "NONE", "NONE", "NONE", "NONE", "NONE", "root_folder/RBC/A/A-3/Statement 2000-06-04.pdf"]],
                                  columns=["Bank", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "MonthStamp", "Filepath"])

        expected_output = pd.DataFrame([["RBC", "A", "B", "C", "D", "E", "2000-01-01", "root_folder/RBC/A/A-1/Statement 2000-01-06.pdf"],
                                        ["RBC", "A", "B", "C", "D", "NONE", "2000-02-01", "root_folder/RBC/A/A-1/Statement 2000-02-09.pdf"],
                                        ["RBC", "A", "B", "C", "NONE", "NONE", "2000-03-01", "root_folder/RBC/A/A-2/Statement 2000-03-13.pdf"],
                                        ["RBC", "A", "B", "NONE", "NONE", "NONE", "2000-04-01", "root_folder/RBC/A/A-2/Statement 2000-04-06.pdf"],
                                        ["RBC", "A", "NONE", "NONE", "NONE", "NONE", "2000-05-01", "root_folder/RBC/A/A-3/Statement 2000-05-08.pdf"],
                                        ["RBC", "NONE", "NONE", "NONE", "NONE", "NONE", "2000-06-01", "root_folder/RBC/A/A-3/Statement 2000-06-04.pdf"]],
                                  columns=["Bank", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "MonthStamp", "Filepath"])

        DataQuality = dataquality.DataQuality()

        actual_output = DataQuality._extract_month_year_stamps(input_data)

        pd.testing.assert_frame_equal(expected_output, actual_output)

if __name__ == '__main__':
    unittest.main()