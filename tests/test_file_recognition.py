import unittest
from financeanalytics import dataloader
from pathlib import Path

class TestFileRecognition(unittest.TestCase):

    def test_case_1(self):
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


if __name__ == '__main__':
    unittest.main()