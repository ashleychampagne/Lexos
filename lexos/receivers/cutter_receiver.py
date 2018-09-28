"""This is the receiver for the cutter model."""

from typing import NamedTuple, Optional, List

from lexos.receivers.base_receiver import BaseReceiver


class CutterFrontEndOptions(NamedTuple):
    cut_size: int
    cut_type: str
    overlap_size: float
    last_proportion: float
    # A milestone, it is none if it is not given from frontend.
    milestone: Optional[str]
    # This is the list of active file ids.
    active_file_ids: List[int]


class CutterReceiver(BaseReceiver):
    """This is the class that gets front end options for the stats model."""

    def __init__(self):
        """Get stats front end options using the receiver."""
        super().__init__()

    def options_from_front_end(self) -> CutterFrontEndOptions:
        """Get the options from front end.

        The only option is selected file ids.
        """
        # Get active file ids from front end as a string.
        active_file_ids_string = self._front_end_data["active_file_ids"]
        # Split the file ids.
        active_file_ids_string_list = active_file_ids_string.split(" ")
        # Force file ids to be integer type and remove extra blank.
        active_file_ids = \
            [int(file_id)
             for file_id in active_file_ids_string_list if file_id != ""]

        # Return stats front end option.
        return CutterFrontEndOptions(active_file_ids=active_file_ids)
