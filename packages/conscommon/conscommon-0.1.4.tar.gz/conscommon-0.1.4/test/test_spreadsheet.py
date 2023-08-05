#!/usr/bin/env python3

import unittest
import os
from conscommon.spreadsheet import SheetName
import conscommon.spreadsheet.parser as spreadsheet_parser


class TestDataModel(unittest.TestCase):
    def test_spreadsheetParser(self):
        spreadsheet_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "Redes e Beaglebones.xlsx"
        )
        self.assertIs(os.path.exists(spreadsheet_path), True)
        data = spreadsheet_parser.loadSheets(spreadsheet_path)

        self.assertIsNot(data[SheetName.AGILENT].__len__(), 0)
        self.assertIsNot(data[SheetName.MKS].__len__(), 0)
        self.assertIsNot(data[SheetName.MBTEMP].__len__(), 0)


if __name__ == "__main__":
    unittest.main()
