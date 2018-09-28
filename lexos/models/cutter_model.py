"""This is the model that cuts files into segments """

from typing import NamedTuple, Optional

from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import FileIDContentMap
from lexos.receivers.cutter_receiver import CutterFrontEndOptions


class CutterTestOptions(NamedTuple):
    """Cutter test front end options."""

    file_id_content_map: FileIDContentMap
    cutter_front_end_option: CutterFrontEndOptions


class CutterModel(BaseModel):
    def __init__(self, test_option: Optional[CutterTestOptions] = None):
        """Initialize the class based on if test option was passed in.

        :param test_option: the options to send in for testing.
        """
        super().__init__()
        if test_option is not None:
            self._test_file_id_content_map = test_option.file_id_content_map
            self._test_front_end_options = test_option.cutter_front_end_option
        else:
            self._test_file_id_content_map = None
            self._test_front_end_options = None
