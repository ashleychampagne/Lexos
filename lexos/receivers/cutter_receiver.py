"""This is the receiver for the cutter model."""

from typing import NamedTuple, Optional, List


class CutterFrontEndOptions(NamedTuple):
    cut_size: int
    cut_type: str
    overlap_size: float
    last_proportion: float
    # A milestone, it is none if it is not given from frontend.
    milestone: Optional[str]
    # This is the list of active file ids.
    active_file_ids: List[int]
