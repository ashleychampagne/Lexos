"""This is the receiver for the cutter model."""

from typing import NamedTuple, Optional, List

from lexos.receivers.base_receiver import BaseReceiver


class CutterFrontEndOptions(NamedTuple):
    """The typed tuple to hold cutter front end option."""

    # The desired segment size of each chunk.
    cut_size: int

    # The desired cutting type.
    cut_type: str

    # The amount of overlapping content at segment boundaries.
    overlap_size: float

    # The smallest size the last segment has to be to become a single chunk.
    last_proportion: float

    # A milestone to cut by, it is none if it is not given from frontend.
    milestone: Optional[str]

    # This is the list of active file ids.
    active_file_ids: List[int]


class CutterReceiver(BaseReceiver):
    """This is the class that gets front end options for the cutter model."""

    def __init__(self):
        """Get cutter front end options using the receiver."""
        super().__init__()

    def options_from_front_end(self) -> CutterFrontEndOptions:
        """Get the options from front end.

        :return: a CutterFrontEndOptions object that contains all desired
        front end options for the cutter model.
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
