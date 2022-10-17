import unittest
from financeanalytics import dataloader
from pathlib import Path
import pandas as pd

class TestDataLoader(unittest.TestCase):

    def test_file_recognition(self):
        # Intended to be run on the main project folder, not compatible with running in different working path
        expected_files = ["tests/detection_test/RBC/Chequing/empty.pdf",
                          "tests/detection_test/RBC/V1sa/empty.pdf",
                          "tests/detection_test/TD/Checking/empty.pdf",
                          "tests/detection_test/TD/Visa/empty.pdf"]
        expected_output = [Path(x) for x in expected_files]

        DataLoader = dataloader.DataLoader()

        root_folder = "tests/detection_test"

        actual_output = DataLoader._detect_relevant_files(root_folder)

        self.assertEqual(expected_output, actual_output)

    def test_detect_relevant_files_default_value(self):
        input_files = ["root_folder/RBC/Chequing/empty.pdf",
                       "root_folder/RbC/Chequing/empty.pdf",
                       "root_folder/rbc/Chequing/empty.pdf",
                       "root_folder/TD/Chequing/empty.pdf",
                       "root_folder/td/Chequing/empty.pdf",
                       "root_folder/nonbank/Chequing/empty.pdf"
                       ]

        expected_files = ["root_folder/RBC/Chequing/empty.pdf",
                          "root_folder/RbC/Chequing/empty.pdf",
                          "root_folder/rbc/Chequing/empty.pdf"
                       ]

        proper_input = [Path(x) for x in input_files]
        expected_output = [Path(x) for x in expected_files]

        DataLoader = dataloader.DataLoader()

        actual_output = DataLoader._remove_unsupported_banks(proper_input)

        self.assertEqual(expected_output, actual_output)

    def test_detect_relevant_files_multi_bank(self):
        input_files = ["root_folder/RBC/Chequing/empty.pdf",
                       "root_folder/RbC/Chequing/empty.pdf",
                       "root_folder/rbc/Chequing/empty.pdf",
                       "root_folder/TD/Chequing/empty.pdf",
                       "root_folder/td/Chequing/empty.pdf",
                       "root_folder/nonbank/Chequing/empty.pdf"
                       ]

        expected_files = ["root_folder/RBC/Chequing/empty.pdf",
                          "root_folder/RbC/Chequing/empty.pdf",
                          "root_folder/rbc/Chequing/empty.pdf",
                          "root_folder/TD/Chequing/empty.pdf",
                          "root_folder/td/Chequing/empty.pdf",
                       ]

        proper_input = [Path(x) for x in input_files]
        expected_output = [Path(x) for x in expected_files]

        DataLoader = dataloader.DataLoader(supported_banks=["rbc", "td"])

        actual_output = DataLoader._remove_unsupported_banks(proper_input)

        self.assertEqual(expected_output, actual_output)

    def test_filter_files_missing_dates(self):
        input_files = ["root_folder/RBC/Chequing/Chequing Statement-9999 2000-01-01.pdf",
                       "root_folder/RBC/Chequing/Chequing Statement-9999.pdf",
                       "root_folder/RBC/Visa/Visa Statement-0000 2000-01-01.pdf",
                       "root_folder/RBC/Visa/Visa Statement-0000.pdf",
                       ]

        expected_files = ["root_folder/RBC/Chequing/Chequing Statement-9999 2000-01-01.pdf",
                          "root_folder/RBC/Visa/Visa Statement-0000 2000-01-01.pdf"
                       ]

        proper_input = [Path(x) for x in input_files]
        expected_output = [Path(x) for x in expected_files]

        DataLoader = dataloader.DataLoader()

        actual_output = DataLoader._remove_files_missing_dates(proper_input)

        self.assertEqual(expected_output, actual_output)

    def test_structure_data_1(self):
        # Testing for mixed scenario
        input_files = ["root_folder/RBC/GroupA/GroupA-1/Statement 2000-01-01.pdf",
                       "root_folder/RBC/GroupA/GroupA-1/Statement 2000-02-01.pdf",
                       "root_folder/RBC/GroupA/GroupA-2/Statement 2000-01-01.pdf",
                       "root_folder/RBC/GroupA/GroupA-2/Statement 2000-02-01.pdf",
                       "root_folder/RBC/GroupB/Statement 2000-01-01.pdf",
                       "root_folder/RBC/GroupB/Statement 2000-02-01.pdf",
                       "root_folder/TD/GroupA/GroupA-1/Statement 2000-01-01.pdf",
                       "root_folder/TD/GroupA/GroupA-1/Statement 2000-02-01.pdf",
                       "root_folder/TD/GroupA/GroupA-3/Statement 2000-01-01.pdf",
                       "root_folder/TD/GroupA/GroupA-3/Statement 2000-02-01.pdf"
                       ]

        proper_input = [Path(x) for x in input_files]

        output_data = [["RBC", "GROUPA", "GROUPA-1", "root_folder/RBC/GroupA/GroupA-1/Statement 2000-01-01.pdf"],
                       ["RBC", "GROUPA", "GROUPA-1", "root_folder/RBC/GroupA/GroupA-1/Statement 2000-02-01.pdf"],
                       ["RBC", "GROUPA", "GROUPA-2", "root_folder/RBC/GroupA/GroupA-2/Statement 2000-01-01.pdf"],
                       ["RBC", "GROUPA", "GROUPA-2", "root_folder/RBC/GroupA/GroupA-2/Statement 2000-02-01.pdf"],
                       ["RBC", "GROUPB", "NONE", "root_folder/RBC/GroupB/Statement 2000-01-01.pdf"],
                       ["RBC", "GROUPB", "NONE", "root_folder/RBC/GroupB/Statement 2000-02-01.pdf"],
                       ["TD", "GROUPA", "GROUPA-1", "root_folder/TD/GroupA/GroupA-1/Statement 2000-01-01.pdf"],
                       ["TD", "GROUPA", "GROUPA-1", "root_folder/TD/GroupA/GroupA-1/Statement 2000-02-01.pdf"],
                       ["TD", "GROUPA", "GROUPA-3", "root_folder/TD/GroupA/GroupA-3/Statement 2000-01-01.pdf"],
                       ["TD", "GROUPA", "GROUPA-3", "root_folder/TD/GroupA/GroupA-3/Statement 2000-02-01.pdf"],
                       ]

        expected_output = pd.DataFrame(output_data, columns=["Bank", "Level 1", "Level 2", "Filepath"])

        DataLoader = dataloader.DataLoader()

        actual_output = DataLoader._structure_cleaned_file_listing(proper_input)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_structure_data_2(self):
        # Testing for case insensitivity
        input_files = ["root_folder/RBC/GroupA/GroupA-1/Statement 2000-01-01.pdf",
                       "root_folder/RBC/GroupA/groupa-1/Statement 2000-02-01.pdf",
                       "root_folder/rBC/GroupA/GroupA-1/Statement 2000-03-01.pdf",
                       "root_folder/rbc/groupa/GroupA-1/Statement 2000-04-01.pdf"
                       ]

        proper_input = [Path(x) for x in input_files]

        output_data = [["RBC", "GROUPA", "GROUPA-1", "root_folder/RBC/GroupA/GroupA-1/Statement 2000-01-01.pdf"],
                       ["RBC", "GROUPA", "GROUPA-1", "root_folder/RBC/GroupA/groupa-1/Statement 2000-02-01.pdf"],
                       ["RBC", "GROUPA", "GROUPA-1", "root_folder/rBC/GroupA/GroupA-1/Statement 2000-03-01.pdf"],
                       ["RBC", "GROUPA", "GROUPA-1", "root_folder/rbc/groupa/GroupA-1/Statement 2000-04-01.pdf"]
                       ]

        expected_output = pd.DataFrame(output_data, columns=["Bank", "Level 1", "Level 2", "Filepath"])

        DataLoader = dataloader.DataLoader()

        actual_output = DataLoader._structure_cleaned_file_listing(proper_input)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_structure_data_3(self):
        # Testing for no level hierarchy only bank folder
        input_files = ["root_folder/RBC/Statement 2000-01-01.pdf",
                       "root_folder/RBC/Statement 2000-02-01.pdf"
                       ]

        proper_input = [Path(x) for x in input_files]

        output_data = [["RBC", "root_folder/RBC/Statement 2000-01-01.pdf"],
                       ["RBC", "root_folder/RBC/Statement 2000-02-01.pdf"]
                       ]

        expected_output = pd.DataFrame(output_data, columns=["Bank", "Filepath"])

        DataLoader = dataloader.DataLoader()

        actual_output = DataLoader._structure_cleaned_file_listing(proper_input)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_structure_data_4(self):
        # Testing for many files on many levels
        input_files = ["root_folder/RBC/A/B/C/D/E/Statement 2000-01-01.pdf",
                       "root_folder/RBC/A/B/C/D/Statement 2000-02-01.pdf",
                       "root_folder/RBC/A/B/C/Statement 2000-03-01.pdf",
                       "root_folder/RBC/A/B/Statement 2000-04-01.pdf",
                       "root_folder/RBC/A/Statement 2000-05-01.pdf",
                       "root_folder/RBC/Statement 2000-06-01.pdf",
                       ]

        proper_input = [Path(x) for x in input_files]

        output_data = [["RBC", "A", "B", "C", "D", "E", "root_folder/RBC/A/B/C/D/E/Statement 2000-01-01.pdf"],
                       ["RBC", "A", "B", "C", "D", "NONE", "root_folder/RBC/A/B/C/D/Statement 2000-02-01.pdf"],
                       ["RBC", "A", "B", "C", "NONE", "NONE", "root_folder/RBC/A/B/C/Statement 2000-03-01.pdf"],
                       ["RBC", "A", "B", "NONE", "NONE", "NONE", "root_folder/RBC/A/B/Statement 2000-04-01.pdf"],
                       ["RBC", "A", "NONE", "NONE", "NONE", "NONE", "root_folder/RBC/A/Statement 2000-05-01.pdf"],
                       ["RBC", "NONE", "NONE", "NONE", "NONE", "NONE", "root_folder/RBC/Statement 2000-06-01.pdf"]
                       ]

        expected_output = pd.DataFrame(output_data, columns=["Bank", "Level 1", "Level 2", "Level 3", "Level 4",
                                                             "Level 5", "Filepath"])

        DataLoader = dataloader.DataLoader()

        actual_output = DataLoader._structure_cleaned_file_listing(proper_input)

        pd.testing.assert_frame_equal(expected_output, actual_output)

if __name__ == '__main__':
    unittest.main()