"""This is the model that cuts files into segments """

from typing import NamedTuple, Optional, List, Dict

from lexos.models.base_model import BaseModel
from lexos.models.filemanager_model import FileManagerModel
from lexos.models.matrix_model import FileIDContentMap
from lexos.receivers.cutter_receiver import CutterFrontEndOptions


class CutterTestOptions(NamedTuple):
    """Cutter test front end options."""

    active_file_ids: List[int]
    file_id_label_map: Dict[int, str]
    file_id_content_map: FileIDContentMap
    cutter_front_end_option: CutterFrontEndOptions


class CutterModel(BaseModel):
    def __init__(self, test_option: Optional[CutterTestOptions] = None):
        """Initialize the class based on if test option was passed in.

        :param test_option: the options to send in for testing.
        """
        super().__init__()
        if test_option is not None:
            self._test_active_file_ids = test_option.active_file_ids
            self._test_file_id_label_map = test_option.file_id_label_map
            self._test_file_id_content_map = test_option.file_id_content_map
            self._test_front_end_options = test_option.cutter_front_end_option
        else:
            self._test_active_file_ids = None
            self._test_file_id_label_map = None
            self._test_file_id_content_map = None
            self._test_front_end_options = None

    @property
    def _stats_option(self):
        """:return: statistics front end option."""
        return self._test_front_end_option \
            if self._test_front_end_option is not None \
            else StatsReceiver().options_from_front_end()

    @property
    def _active_file_ids(self) -> List[int]:
        if self._test_active_file_ids is not None:
            return self._test_active_file_ids
        else:
            return self._


    @property
    def _active_id_passages_map(self) -> List[str]:
        """Get the passages to cut.

        :return: the content of the passage as a string.
        """
        # if test option is specified
        if self._test_file_id_content_map is not None and \
                self._test_front_end_options is not None:

            active_file_ids = self._test_front_end_options.active_file_ids
            file_id_content_map = self._test_file_id_content_map

        # if test option is not specified, get option from front end
        else:
            file_id =
            return FileManagerModel().load_file_manager() \
                .get_content_of_active_with_id()

    @property
    def _active_id_labels_map(self) -> List[str]:

    @property
    def _options(self) -> RWAFrontEndOptions:
        """Get the front end option packed as one named tuple.

        :return: a RWAFrontEndOption packs all the frontend option.
        """
        return self._test_front_end_options \
            if self._test_front_end_options is not None \
            else RollingWindowsReceiver().options_from_front_end()
