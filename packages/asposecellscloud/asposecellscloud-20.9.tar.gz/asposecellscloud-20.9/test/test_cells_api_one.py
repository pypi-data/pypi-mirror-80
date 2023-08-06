# coding: utf-8

from __future__ import absolute_import

import os
import sys
import unittest
import warnings

ABSPATH = os.path.abspath(os.path.realpath(os.path.dirname(__file__)) + "/..")
sys.path.append(ABSPATH)
import asposecellscloud
from asposecellscloud.rest import ApiException
from asposecellscloud.apis.cells_api import CellsApi
import AuthUtil
from asposecellscloud.models import FontSetting
from asposecellscloud.models import Font
from asposecellscloud.models import ImportIntArrayOption
from asposecellscloud.models import CalculationOptions
from asposecellscloud.models import WorkbookSettings
from asposecellscloud.models import PasswordRequest
from asposecellscloud.models import ColorFilterRequest
from asposecellscloud.models import Color
from asposecellscloud.models import CellsColor
from asposecellscloud.models import ThemeColor
from asposecellscloud.models.font import Font

class TestCellsApi(unittest.TestCase):
    """ CellsApi unit test stubs """

    def setUp(self):
        # warnings.simplefilter("ignore", ResourceWarning)
        # self.api_client = AuthUtil.GetApiClient()
        self.api = asposecellscloud.apis.cells_api.CellsApi(AuthUtil.GetAPPSID(),AuthUtil.GetAPPKey(),"v3.0")

    def tearDown(self):
        pass

    def test_cells_post_cell_characters(self):
        """
        Test case for cells_post_cell_characters

        Set cell characters 
        """
        name ='Book1.xlsx'
        sheet_name ='Sheet2'
        cellName = 'G8'
        font = Font()
        font.size = 10.0
        fs1 = FontSetting(font=font, length=2, start_index=0)
        options = [fs1]
        folder = "Temp"
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0)
        
        result = self.api.cells_post_cell_characters(name, sheet_name, cellName, options=options, folder=folder)
        self.assertEqual(result.code,200)
        pass

if __name__ == '__main__':
    unittest.main()
