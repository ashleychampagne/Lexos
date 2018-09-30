"""This is the receiver for the cutter model."""

from typing import NamedTuple, Optional, List
from lexos.receivers.base_receiver import BaseReceiver


class CutByChunkOptions(NamedTuple):
    # The desired cutting type.
    cut_type: str

    # The desired segment size of each chunk.
    cut_size: int

    # The amount of overlapping content at segment boundaries.
    overlap_size: int

    # The smallest size the last segment has to be to become a single chunk.
    last_prop: float


class CutByNumberOfSegmentsOptions(NamedTuple):
    number_of_segments: int


class CutByMilestoneOptions(NamedTuple):
    # A milestone to cut by, it is none if it is not given from frontend.
    milestone: Optional[str]


class CutterFrontEndOptions(NamedTuple):
    """The typed tuple to hold cutter front end option."""
    cut_by_chunk_option: Optional[CutByChunkOptions]

    cut_by_milestone_option: Optional[CutByMilestoneOptions]

    cut_by_number_of_segments_option: Optional[CutByNumberOfSegmentsOptions]

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
        A = self._front_end_data
        # Get active file ids from front end as a string.
        active_file_ids_string = self._front_end_data["active_file_ids"]
        # Split the file ids.
        active_file_ids_string_list = active_file_ids_string.split(" ")
        # Force file ids to be integer type and remove extra blank.
        active_file_ids = \
            [int(file_id)
             for file_id in active_file_ids_string_list if file_id != ""]

        if self._front_end_data["method"] == "segments":
            return CutterFrontEndOptions(
                cut_by_chunk_option=None,
                cut_by_milestone_option=None,
                cut_by_number_of_segments_option=CutByNumberOfSegmentsOptions(
                    number_of_segments=int(self._front_end_data["num-segment"])
                ),
                active_file_ids=active_file_ids
            )

        elif self._front_end_data["method"] == "milestone":
            return CutterFrontEndOptions(
                cut_by_chunk_option=None,
                cut_by_number_of_segments_option=None,
                cut_by_milestone_option=CutByMilestoneOptions(
                    milestone=self._front_end_data["milestone"]
                ),
                active_file_ids=active_file_ids
            )

        else:
            return CutterFrontEndOptions(
                cut_by_milestone_option=None,
                cut_by_number_of_segments_option=None,
                cut_by_chunk_option=CutByChunkOptions(
                    cut_type=self._front_end_data["method"],
                    cut_size=int(self._front_end_data["chunk-size"]),
                    overlap_size=int(self._front_end_data["overlap"]),
                    last_prop=int(self._front_end_data["last-prop"]) / 100
                ),
                active_file_ids=active_file_ids
            )
