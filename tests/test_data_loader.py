import unittest
from financeanalytics import dataloader
from pathlib import Path

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

        output = DataLoader._detect_relevant_files(root_folder)

        self.assertEqual(expected_output, output)

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

        output = DataLoader._remove_unsupported_banks(proper_input)

        self.assertEqual(expected_output, output)

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

        output = DataLoader._remove_unsupported_banks(proper_input)

        self.assertEqual(expected_output, output)

if __name__ == '__main__':
    unittest.main()