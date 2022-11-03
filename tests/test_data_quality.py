import unittest
from financeanalytics import dataquality
from pathlib import Path
import pandas as pd

class TestDataQuality(unittest.TestCase):

    def test_extract_month_stamp_bank_only_no_gaps(self):

        input_data = pd.DataFrame([["RBC", "C:/root_folder/RBC/Statement 2000-01-06.pdf"],
                                   ["RBC", "C:/root_folder/RBC/Statement 2000-02-09.pdf"],
                                   ["RBC", "C:/root_folder/RBC/Statement 2000-03-13.pdf"],
                                   ["RBC", "C:/root_folder/RBC/Statement 2000-04-06.pdf"],
                                   ["RBC", "C:/root_folder/RBC/Statement 2000-05-08.pdf"]],
                                  columns=["Bank", "Filepath"])

        # Convert to proper path
        input_data["Filepath"] = input_data["Filepath"].apply(lambda x: Path(x))

        expected_output = pd.DataFrame([["RBC", "C:/root_folder/RBC/Statement 2000-01-06.pdf", "2000-01-01"],
                                        ["RBC", "C:/root_folder/RBC/Statement 2000-02-09.pdf", "2000-02-01"],
                                        ["RBC", "C:/root_folder/RBC/Statement 2000-03-13.pdf", "2000-03-01"],
                                        ["RBC", "C:/root_folder/RBC/Statement 2000-04-06.pdf", "2000-04-01"],
                                        ["RBC", "C:/root_folder/RBC/Statement 2000-05-08.pdf", "2000-05-01"]],
                                  columns=["Bank", "Filepath", "MonthStamp"])

        expected_output["Filepath"] = expected_output["Filepath"].apply(lambda x: Path(x))

        DataQuality = dataquality.DataQuality()

        actual_output = DataQuality._extract_month_year_stamps(input_data)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_extract_month_stamp_bank_only_with_gaps(self):

        input_data = pd.DataFrame([["RBC", "C:/root_folder/RBC/Statement 2000-01-06.pdf"],
                                   ["RBC", "C:/root_folder/RBC/Statement 2000-03-13.pdf"],
                                   ["RBC", "C:/root_folder/RBC/Statement 2000-05-08.pdf"]],
                                  columns=["Bank", "Filepath"])

        input_data["Filepath"] = input_data["Filepath"].apply(lambda x: Path(x))

        expected_output = pd.DataFrame([["RBC", "C:/root_folder/RBC/Statement 2000-01-06.pdf", "2000-01-01"],
                                        ["RBC", "C:/root_folder/RBC/Statement 2000-03-13.pdf", "2000-03-01"],
                                        ["RBC", "C:/root_folder/RBC/Statement 2000-05-08.pdf", "2000-05-01"]],
                                  columns=["Bank", "Filepath", "MonthStamp"])

        expected_output["Filepath"] = expected_output["Filepath"].apply(lambda x: Path(x))

        DataQuality = dataquality.DataQuality()

        actual_output = DataQuality._extract_month_year_stamps(input_data)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_extract_month_stamp_two_levels(self):

        input_data = pd.DataFrame([["RBC", "A", "A-1", "C:/root_folder/RBC/A/A-1/Statement 2000-01-06.pdf"],
                                   ["RBC", "A", "A-1", "C:/root_folder/RBC/A/A-1/Statement 2000-02-09.pdf"],
                                   ["RBC", "A", "A-2", "C:/root_folder/RBC/A/A-2/Statement 2000-03-13.pdf"],
                                   ["RBC", "A", "A-2", "C:/root_folder/RBC/A/A-2/Statement 2000-04-06.pdf"],
                                   ["RBC", "A", "A-3", "C:/root_folder/RBC/A/A-3/Statement 2000-05-08.pdf"]],
                                  columns=["Bank", "Level 1", "Level 2", "Filepath"])

        input_data["Filepath"] = input_data["Filepath"].apply(lambda x: Path(x))

        expected_output = pd.DataFrame([["RBC", "A", "A-1", "C:/root_folder/RBC/A/A-1/Statement 2000-01-06.pdf", "2000-01-01"],
                                        ["RBC", "A", "A-1", "C:/root_folder/RBC/A/A-1/Statement 2000-02-09.pdf", "2000-02-01"],
                                        ["RBC", "A", "A-2", "C:/root_folder/RBC/A/A-2/Statement 2000-03-13.pdf", "2000-03-01"],
                                        ["RBC", "A", "A-2", "C:/root_folder/RBC/A/A-2/Statement 2000-04-06.pdf", "2000-04-01"],
                                        ["RBC", "A", "A-3", "C:/root_folder/RBC/A/A-3/Statement 2000-05-08.pdf", "2000-05-01"]],
                                  columns=["Bank", "Level 1", "Level 2", "Filepath", "MonthStamp"])

        expected_output["Filepath"] = expected_output["Filepath"].apply(lambda x: Path(x))

        DataQuality = dataquality.DataQuality()

        actual_output = DataQuality._extract_month_year_stamps(input_data)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_extract_month_stamp_five_levels_with_nones(self):

        input_data = pd.DataFrame([["RBC", "A", "B", "C", "D", "E", "C:/root_folder/RBC/A/A-1/Statement 2000-01-06.pdf"],
                                        ["RBC", "A", "B", "C", "D", "NONE", "C:/root_folder/RBC/A/A-1/Statement 2000-02-09.pdf"],
                                        ["RBC", "A", "B", "C", "NONE", "NONE", "C:/root_folder/RBC/A/A-2/Statement 2000-03-13.pdf"],
                                        ["RBC", "A", "B", "NONE", "NONE", "NONE", "C:/root_folder/RBC/A/A-2/Statement 2000-04-06.pdf"],
                                        ["RBC", "A", "NONE", "NONE", "NONE", "NONE", "C:/root_folder/RBC/A/A-3/Statement 2000-05-08.pdf"],
                                        ["RBC", "NONE", "NONE", "NONE", "NONE", "NONE", "C:/root_folder/RBC/A/A-3/Statement 2000-06-04.pdf"]],
                                  columns=["Bank", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Filepath"])

        input_data["Filepath"] = input_data["Filepath"].apply(lambda x: Path(x))

        expected_output = pd.DataFrame([["RBC", "A", "B", "C", "D", "E", "C:/root_folder/RBC/A/A-1/Statement 2000-01-06.pdf", "2000-01-01"],
                                        ["RBC", "A", "B", "C", "D", "NONE", "C:/root_folder/RBC/A/A-1/Statement 2000-02-09.pdf", "2000-02-01"],
                                        ["RBC", "A", "B", "C", "NONE", "NONE", "C:/root_folder/RBC/A/A-2/Statement 2000-03-13.pdf", "2000-03-01"],
                                        ["RBC", "A", "B", "NONE", "NONE", "NONE", "C:/root_folder/RBC/A/A-2/Statement 2000-04-06.pdf", "2000-04-01"],
                                        ["RBC", "A", "NONE", "NONE", "NONE", "NONE", "C:/root_folder/RBC/A/A-3/Statement 2000-05-08.pdf", "2000-05-01"],
                                        ["RBC", "NONE", "NONE", "NONE", "NONE", "NONE", "C:/root_folder/RBC/A/A-3/Statement 2000-06-04.pdf", "2000-06-01"]],
                                  columns=["Bank", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Filepath", "MonthStamp"])

        expected_output["Filepath"] = expected_output["Filepath"].apply(lambda x: Path(x))

        DataQuality = dataquality.DataQuality()

        actual_output = DataQuality._extract_month_year_stamps(input_data)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_aggregate_bank_only(self):

        input_data = pd.DataFrame([["RBC", "C:/root_folder/RBC/Statement 2000-01-06.pdf", "2000-01-01"],
                                   ["RBC", "C:/root_folder/RBC/Statement 2000-02-13.pdf", "2000-02-01"],
                                   ["RBC", "C:/root_folder/RBC/Statement 2000-04-17.pdf", "2000-04-01"],
                                   ["TD", "C:/root_folder/RBC/Statement 2000-01-02.pdf", "2000-01-01"],
                                   ["TD", "C:/root_folder/RBC/Statement 2000-02-06.pdf", "2000-02-01"],
                                   ["TD", "C:/root_folder/RBC/Statement 2000-03-13.pdf", "2000-03-01"],
                                   ["TD", "C:/root_folder/RBC/Statement 2000-04-08.pdf", "2000-04-01"]
                                   ], columns=["Bank", "Filepath", "MonthStamp"])

        input_data["Filepath"] = input_data["Filepath"].apply(lambda x: Path(x))

        expected_output = pd.DataFrame([["RBC", "2000-01-01", "2000-04-01", ["2000-01-01", "2000-02-01", "2000-04-01"]],
                                        ["TD", "2000-01-01", "2000-04-01", ["2000-01-01", "2000-02-01", "2000-03-01", "2000-04-01"]],
                                   ], columns=["Bank", "min_date", "max_date", "all_dates"])

        DataQuality = dataquality.DataQuality()

        actual_output = DataQuality._aggregate_df_analytics(input_data)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_aggregate_two_levels(self):

        input_data = pd.DataFrame([["RBC", "A", "A-1", "unused", "1999-10-01"],
                                   ["RBC", "A", "A-1", "unused", "1999-11-01"],
                                   ["RBC", "A", "A-1", "unused", "2000-02-01"],
                                   ["RBC", "A", "A-1", "unused", "2000-04-01"],
                                   ["RBC", "A", "A-2", "unused", "2000-01-01"],
                                   ["RBC", "A", "A-2", "unused", "2000-02-01"],
                                   ["RBC", "A", "A-2", "unused", "2000-04-01"],
                                   ["RBC", "B", "B-1", "unused", "2000-01-01"],
                                   ["RBC", "B", "B-1", "unused", "2000-02-01"],
                                   ["RBC", "B", "B-1", "unused", "2000-03-01"]
                                   ], columns=["Bank", "Level 1", "Level 2", "Filepath", "MonthStamp"])

        expected_output = pd.DataFrame([["RBC", "A", "A-1", "1999-10-01", "2000-04-01", ["1999-10-01", "1999-11-01", "2000-02-01", "2000-04-01"]],
                                        ["RBC", "A", "A-2", "2000-01-01", "2000-04-01", ["2000-01-01", "2000-02-01", "2000-04-01"]],
                                        ["RBC", "B", "B-1", "2000-01-01", "2000-03-01", ["2000-01-01", "2000-02-01", "2000-03-01"]]
                                   ], columns=["Bank", "Level 1", "Level 2", "min_date", "max_date", "all_dates"])

        DataQuality = dataquality.DataQuality()

        actual_output = DataQuality._aggregate_df_analytics(input_data)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_aggregate_five_levels(self):

        input_data = pd.DataFrame([["RBC", "A", "B", "C", "D", "E", "unused", "2000-01-01"],
                                   ["RBC", "A", "B", "C", "D", "E", "unused", "2000-02-01"],
                                   ["RBC", "A", "B", "C", "D", "E", "unused", "2000-04-01"],
                                   ["RBC", "A", "B", "C", "D", "NONE", "unused", "2000-01-01"],
                                   ["RBC", "A", "B", "C", "NONE", "NONE", "unused", "2000-02-01"],
                                   ["RBC", "A", "B", "NONE", "NONE", "NONE", "unused", "2000-03-01"],
                                   ["RBC", "A", "NONE", "NONE", "NONE", "NONE", "unused", "2000-04-01"],
                                   ["RBC", "A", "NONE", "NONE", "NONE", "NONE", "unused", "2000-05-01"],
                                   ["RBC", "NONE", "NONE", "NONE", "NONE", "NONE", "unused", "2000-06-01"]
                                   ], columns=["Bank", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Filepath", "MonthStamp"])

        expected_output = pd.DataFrame([["RBC", "A", "B", "C", "D", "E", "2000-01-01", "2000-04-01", ["2000-01-01", "2000-02-01", "2000-04-01"]],
                                        ["RBC", "A", "B", "C", "D", "NONE", "2000-01-01", "2000-01-01", ["2000-01-01"]],
                                        ["RBC", "A", "B", "C", "NONE", "NONE", "2000-02-01", "2000-02-01", ["2000-02-01"]],
                                        ["RBC", "A", "B", "NONE", "NONE", "NONE", "2000-03-01", "2000-03-01", ["2000-03-01"]],
                                        ["RBC", "A", "NONE", "NONE", "NONE", "NONE", "2000-04-01", "2000-05-01", ["2000-04-01", "2000-05-01"]],
                                        ["RBC", "NONE", "NONE", "NONE", "NONE", "NONE", "2000-06-01", "2000-06-01", ["2000-06-01"]]
                                   ], columns=["Bank", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "min_date", "max_date", "all_dates"])

        DataQuality = dataquality.DataQuality()

        actual_output = DataQuality._aggregate_df_analytics(input_data)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_remove_duplicate_data_bank_only(self):

        input_data = pd.DataFrame([["RBC", "C:/root_folder/RBC/Statement 2000-01-06.pdf", "2000-01-01"],
                                   ["RBC", "C:/root_folder/rbc/Statement 2000-01-06.pdf", "2000-01-01"],
                                   ["RBC", "C:/root_folder/RBC/Statement 2000-03-03.pdf", "2000-03-01"],
                                   ["RBC", "C:/root_folder/RBC/Statement 2000-04-06.pdf", "2000-04-01"],
                                   ["RBC", "C:/root_folder/RBC/Statement 2000-05-08.pdf", "2000-05-01"]],
                                  columns=["Bank", "Filepath", "MonthStamp"])

        input_data["Filepath"] = input_data["Filepath"].apply(lambda x: Path(x))

        expected_output = pd.DataFrame([["RBC", "C:/root_folder/RBC/Statement 2000-01-06.pdf", "2000-01-01"],
                                        ["RBC", "C:/root_folder/RBC/Statement 2000-03-03.pdf", "2000-03-01"],
                                        ["RBC", "C:/root_folder/RBC/Statement 2000-04-06.pdf", "2000-04-01"],
                                        ["RBC", "C:/root_folder/RBC/Statement 2000-05-08.pdf", "2000-05-01"]],
                                       columns=["Bank", "Filepath", "MonthStamp"])

        expected_output["Filepath"] = expected_output["Filepath"].apply(lambda x: Path(x))

        DataQuality = dataquality.DataQuality()

        actual_output = DataQuality._remove_duplicate_references(input_data)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_remove_duplicate_data_two_level(self):

        input_data = pd.DataFrame([["RBC", "A", "B", "C:/root_folder/RBC/A/B/Statement 2000-01-06.pdf", "2000-01-01"],
                                   ["RBC", "A", "B", "C:/root_folder/RBC/a/B/Statement 2000-01-06.pdf", "2000-01-01"],
                                   ["RBC", "A", "B", "C:/root_folder/RBC/A/B/Statement 2000-02-06.pdf", "2000-02-01"]],
                                  columns=["Bank", "Level 1", "Level 2", "Filepath", "MonthStamp"])

        input_data["Filepath"] = input_data["Filepath"].apply(lambda x: Path(x))

        expected_output = pd.DataFrame([["RBC", "A", "B", "C:/root_folder/RBC/A/B/Statement 2000-01-06.pdf", "2000-01-01"],
                                        ["RBC", "A", "B", "C:/root_folder/RBC/A/B/Statement 2000-02-06.pdf", "2000-02-01"]],
                                       columns=["Bank", "Level 1", "Level 2", "Filepath", "MonthStamp"])

        expected_output["Filepath"] = expected_output["Filepath"].apply(lambda x: Path(x))

        DataQuality = dataquality.DataQuality()

        actual_output = DataQuality._remove_duplicate_references(input_data)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_remove_duplicate_data_many_levels(self):

        input_data = pd.DataFrame([["RBC", "A", "B", "C", "D", "E", "C:/root_folder/RBC/A/B/C/D/E/Statement 2000-01-06.pdf", "2000-01-01"],
                                   ["RBC", "A", "B", "C", "D", "E", "C:/root_folder/RBC/a/B/C/D/E/Statement 2000-01-06.pdf", "2000-01-01"],
                                   ["RBC", "A", "B", "C", "D", "E", "C:/root_folder/RBC/A/B/C/D/E/Statement 2000-03-06.pdf", "2000-03-01"],
                                   ["RBC", "A", "B", "NONE", "NONE", "NONE", "C:/root_folder/RBC/a/B/Statement 2000-01-06.pdf", "2000-01-01"],
                                   ["RBC", "A", "B", "NONE", "NONE", "NONE", "C:/root_folder/RBC/A/B/Statement 2000-01-06.pdf", "2000-01-01"],
                                   ["RBC", "A", "B", "NONE", "NONE", "NONE", "C:/root_folder/RBC/A/B/Statement 2000-02-06.pdf", "2000-02-01"]],
                                  columns=["Bank", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Filepath", "MonthStamp"])

        input_data["Filepath"] = input_data["Filepath"].apply(lambda x: Path(x))

        expected_output = pd.DataFrame([["RBC", "A", "B", "C", "D", "E", "C:/root_folder/RBC/A/B/C/D/E/Statement 2000-01-06.pdf", "2000-01-01"],
                                        ["RBC", "A", "B", "C", "D", "E", "C:/root_folder/RBC/A/B/C/D/E/Statement 2000-03-06.pdf", "2000-03-01"],
                                        ["RBC", "A", "B", "NONE", "NONE", "NONE", "C:/root_folder/RBC/a/B/Statement 2000-01-06.pdf", "2000-01-01"],
                                        ["RBC", "A", "B", "NONE", "NONE", "NONE", "C:/root_folder/RBC/A/B/Statement 2000-02-06.pdf", "2000-02-01"]],
                                       columns=["Bank", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Filepath", "MonthStamp"])

        expected_output["Filepath"] = expected_output["Filepath"].apply(lambda x: Path(x))

        DataQuality = dataquality.DataQuality()

        actual_output = DataQuality._remove_duplicate_references(input_data)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_gap_detection_bank_only(self):

        input_data = pd.DataFrame([["RBC", "1999-11-01", "2000-03-01", ["1999-11-01", "2000-02-01", "2000-03-01"]],
                                   ["TD", "1999-11-01", "2000-01-01", ["1999-11-01", "1999-12-01", "2000-01-01"]],
                                   ["BMO", "1999-11-01", "2000-01-01", ["1999-11-01", "2000-01-01"]],
                                   ["CIBC", "2000-01-01", "2000-01-01", ["2000-01-01"]]
                                   ], columns=["Bank", "min_date", "max_date", "all_dates"])

        expected_output = pd.DataFrame([["RBC", "1999-11-01", "2000-03-01", ["1999-11-01", "2000-02-01", "2000-03-01"], ["1999-12-01", "2000-01-01"]],
                                   ["TD", "1999-11-01", "2000-01-01", ["1999-11-01", "1999-12-01", "2000-01-01"], []],
                                   ["BMO", "1999-11-01", "2000-01-01", ["1999-11-01", "2000-01-01"], ["1999-12-01"]],
                                   ["CIBC", "2000-01-01", "2000-01-01", ["2000-01-01"], []]
                                   ], columns=["Bank", "min_date", "max_date", "all_dates", "all_gaps"])

        DataQuality = dataquality.DataQuality()

        actual_output = DataQuality._identify_data_gaps(input_data)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_gap_detection_missing_year(self):

        input_data = pd.DataFrame([["RBC", "1999-12-01", "2001-01-01", ["1999-12-01", "2001-01-01"]]
                                   ], columns=["Bank", "min_date", "max_date", "all_dates"])

        expected_output = pd.DataFrame([["RBC", "1999-12-01", "2001-01-01", ["1999-12-01", "2001-01-01"], ["2000-01-01", "2000-02-01", "2000-03-01", "2000-04-01", "2000-05-01", "2000-06-01", "2000-07-01", "2000-08-01", "2000-09-01", "2000-10-01", "2000-11-01", "2000-12-01"]]
                                   ], columns=["Bank", "min_date", "max_date", "all_dates", "all_gaps"])

        DataQuality = dataquality.DataQuality()

        actual_output = DataQuality._identify_data_gaps(input_data)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_gap_detection_two_levels(self):

        input_data = pd.DataFrame(
            [["RBC", "A", "A-1", "1999-10-01", "2000-04-01", ["1999-10-01", "1999-11-01", "2000-02-01", "2000-04-01"]],
             ["RBC", "A", "A-2", "2000-01-01", "2000-04-01", ["2000-01-01", "2000-02-01", "2000-04-01"]],
             ["RBC", "B", "B-1", "2000-01-01", "2000-03-01", ["2000-01-01", "2000-02-01", "2000-03-01"]]
             ], columns=["Bank", "Level 1", "Level 2", "min_date", "max_date", "all_dates"])

        expected_output = pd.DataFrame([["RBC", "A", "A-1", "1999-10-01", "2000-04-01", ["1999-10-01", "1999-11-01", "2000-02-01", "2000-04-01"], ["1999-12-01", "2000-01-01", "2000-03-01"]],
                                        ["RBC", "A", "A-2", "2000-01-01", "2000-04-01", ["2000-01-01", "2000-02-01", "2000-04-01"], ["2000-03-01"]],
                                        ["RBC", "B", "B-1", "2000-01-01", "2000-03-01", ["2000-01-01", "2000-02-01", "2000-03-01"], []]
                                        ], columns=["Bank", "Level 1", "Level 2", "min_date", "max_date", "all_dates", "all_gaps"])

        DataQuality = dataquality.DataQuality()

        actual_output = DataQuality._identify_data_gaps(input_data)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_gap_detection_five_levels(self):
        input_data = pd.DataFrame([["RBC", "A", "B", "C", "D", "E", "2000-01-01", "2000-05-01", ["2000-01-01", "2000-03-01", "2000-05-01"]],
                                   ["RBC", "A", "B", "C", "D", "NONE", "2000-01-01", "2000-01-01", ["2000-01-01"]],
                                   ["RBC", "A", "B", "C", "NONE", "NONE", "2000-02-01", "2000-02-01", ["2000-02-01"]],
                                   ["RBC", "A", "B", "NONE", "NONE", "NONE", "2000-03-01", "2000-03-01", ["2000-03-01"]],
                                   ["RBC", "A", "NONE", "NONE", "NONE", "NONE", "2000-04-01", "2000-06-01", ["2000-04-01", "2000-06-01"]],
                                   ["RBC", "NONE", "NONE", "NONE", "NONE", "NONE", "2000-07-01", "2000-07-01", ["2000-07-01"]]
                                   ], columns=["Bank", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "min_date", "max_date", "all_dates"])

        expected_output = pd.DataFrame([["RBC", "A", "B", "C", "D", "E", "2000-01-01", "2000-05-01", ["2000-01-01", "2000-03-01", "2000-05-01"], ["2000-02-01", "2000-04-01"]],
                                        ["RBC", "A", "B", "C", "D", "NONE", "2000-01-01", "2000-01-01", ["2000-01-01"], []],
                                        ["RBC", "A", "B", "C", "NONE", "NONE", "2000-02-01", "2000-02-01", ["2000-02-01"], []],
                                        ["RBC", "A", "B", "NONE", "NONE", "NONE", "2000-03-01", "2000-03-01", ["2000-03-01"], []],
                                        ["RBC", "A", "NONE", "NONE", "NONE", "NONE", "2000-04-01", "2000-06-01", ["2000-04-01", "2000-06-01"], ["2000-05-01"]],
                                        ["RBC", "NONE", "NONE", "NONE", "NONE", "NONE", "2000-07-01", "2000-07-01", ["2000-07-01"], []]
                                        ], columns=["Bank", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "min_date", "max_date", "all_dates", "all_gaps"])

        DataQuality = dataquality.DataQuality()

        actual_output = DataQuality._identify_data_gaps(input_data)

        pd.testing.assert_frame_equal(expected_output, actual_output)

if __name__ == '__main__':
    unittest.main()