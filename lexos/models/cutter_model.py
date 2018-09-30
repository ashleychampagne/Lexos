"""This is the model that cuts files into segments."""
import re
from typing import NamedTuple, Optional, Dict, List
from lexos.models.base_model import BaseModel
from lexos.models.filemanager_model import FileManagerModel
from lexos.receivers.cutter_receiver import CutterReceiver, \
    CutterFrontEndOptions
from lexos.helpers.error_messages import SEG_NON_POSITIVE_MESSAGE, \
    NEG_OVERLAP_LAST_PROP_MESSAGE, LARGER_SEG_SIZE_MESSAGE, \
    EMPTY_MILESTONE_MESSAGE, INVALID_CUTTING_TYPE_MESSAGE


class File(NamedTuple):
    """Structure for each file."""

    label: str
    content: str


class CutterTestOptions(NamedTuple):
    """Cutter test front end options."""

    active_file_ids: List[int]
    file_id_label_map: Dict[int, str]
    file_id_content_map: Dict[int, str]
    cutter_front_end_option: CutterFrontEndOptions


class CutterModel(BaseModel):
    """This is the model for the cutter."""

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
    def _cutter_option(self) -> CutterFrontEndOptions:
        """:return: cutter front end option."""
        return self._test_front_end_options \
            if self._test_front_end_options is not None \
            else CutterReceiver().options_from_front_end()

    @property
    def _active_file_ids(self) -> List[int]:
        """:return: list of ids of active files."""
        return self._test_active_file_ids \
            if self._test_active_file_ids is not None \
            else self._cutter_option.active_file_ids

    @property
    def _id_passages_map(self) -> Dict[int, str]:
        """Get a dictionary of file ids and file contents.

        :return: a dictionary where ids are keys and contents are items.
        """
        return self._test_file_id_content_map \
            if self._test_file_id_content_map is not None \
            else FileManagerModel().load_file_manager(). \
            get_content_of_active_with_id()

    @property
    def _id_labels_map(self) -> Dict[int, str]:
        """Get a dictionary of file ids and file labels.

        :return: a dictionary where ids are keys and labels are items.
        """
        return self._test_file_id_label_map \
            if self._test_file_id_label_map is not None \
            else FileManagerModel().load_file_manager(). \
            get_active_labels_with_id()

    @property
    def _active_file_label_content_map(self) -> List[File]:
        """:return: a list of File objects for the active files."""
        return [
            File(
                label=self._id_labels_map[active_id],
                content=self._id_passages_map[active_id]
            )
            for active_id in self._active_file_ids
        ]

    @staticmethod
    def cut_list_with_overlap(overlap: int,
                              last_prop: float,
                              input_list: list,
                              norm_seg_size: int) -> List[list]:
        """Cut the split list of text into list that contains sub-lists.

        This function takes care of both overlap and last proportion with the
        input list and the segment size. The function calculates the number of
        segment with the overlap value and then use it as indexing to capture
        all the sub-lists with the get_single_seg helper function.
        :param last_prop: the last segment size / other segment size.
        :param input_list: the segment list that is split by the desired type.
        :param norm_seg_size: the size of the segment.
        :param overlap: min proportional size that the last segment has to be.
        :return a list of list(segment) that the text has been cut into, which
        has not go through the last proportion size calculation.
        """
        # get the distance between starts of each two adjacent segments
        seg_start_distance = norm_seg_size - overlap

        # the length of the list excluding the last segment
        length_exclude_last = len(input_list) - norm_seg_size * last_prop

        # the total number of segments after cut
        # the `+ 1` is to add back the last segments
        num_segment = \
            int(length_exclude_last / seg_start_distance) + 1

        # need at least one segment
        if num_segment < 1:
            num_segment = 1

        def get_single_seg(index: int, is_last_prop: bool) -> list:
            """Helper to get one single segment with index.

            This function first evaluate whether the segment is the last one
            and grab different segment according to the result, and returns
            sub-lists while index is in the range of number of segment.
            :param is_last_prop: the bool value that determine whether the
            segment is the last one.
            :param index: the index of the segment in the final segment list.
            :return single segment in the input_list based on index.
            """
            # define current segment size based on if it is the last segment
            if is_last_prop:
                return input_list[seg_start_distance * index:]
            else:
                return input_list[seg_start_distance * index:
                                  seg_start_distance * index + norm_seg_size]

        # return the whole list of segment while evaluating if the last segment
        return [
            get_single_seg(
                index=index,
                is_last_prop=True if index == num_segment - 1 else False
            )
            for index in range(num_segment)
        ]

    @staticmethod
    def join_sublist_element(input_list: List[List[str]]) -> List[str]:
        """Join each sublist of chars into string.

        This function joins all the element(chars) in each sub-lists together,
        and turns every sub-lists to one element in the overall list. The
        sublist will turned into a string with all the same elements as before.
        :param input_list: the returned list after cut
        :return: the list that contains all the segments as strings.
        """
        return ["".join(chars) for chars in input_list]

    @staticmethod
    def cut_by_characters(text: str,
                          overlap: int,
                          seg_size: int,
                          last_prop: float) -> List[str]:
        """Cut the input text into segments by number of chars in each segment.

        Where the segment size is measured by counts of characters, with an
        option for an amount of overlap between segments and a minimum
        proportion threshold for the last segment.
        :param text: the string with the contents of the file.
        :param seg_size: the segment size, in characters.
        :param overlap: the number of characters to overlap between segments.
        :param last_prop: the last segment size / other segment size.
        :return: a list of list(segment) that the text has been cut into.
        """
        # pre-condition assertion
        assert seg_size > 0, SEG_NON_POSITIVE_MESSAGE
        assert seg_size > overlap, LARGER_SEG_SIZE_MESSAGE
        assert overlap >= 0 and last_prop >= 0, NEG_OVERLAP_LAST_PROP_MESSAGE

        # split all the chars while keeping all the whitespace
        seg_list = re.findall("\S", text)

        # add sub-lists(segment) to final list
        final_seg_list = CutterModel.cut_list_with_overlap(
            input_list=seg_list,
            norm_seg_size=seg_size,
            overlap=overlap,
            last_prop=last_prop
        )

        # join characters in each sublist
        final_seg_list = CutterModel.join_sublist_element(
            input_list=final_seg_list
        )

        return final_seg_list

    @staticmethod
    def cut_by_words(text: str,
                     overlap: int,
                     seg_size: int,
                     last_prop: float) -> List[str]:
        """Cut the input text into segments by number of words in each segment.

        Cuts the text into equally sized segments, where the segment size is
        measured by counts of words, with an option for an amount of overlap
        between segments and a minimum proportion threshold for the last chunk.
        :param text: the string with the contents of the file.
        :param seg_size: the segment size, in words.
        :param overlap: the number of words to overlap between segments.
        :param last_prop: the last segment size / other segment size.
        :return: a list of list(segment) that the text has been cut into.
        """
        # pre-condition assertion
        assert seg_size > 0, SEG_NON_POSITIVE_MESSAGE
        assert seg_size > overlap, LARGER_SEG_SIZE_MESSAGE
        assert overlap >= 0 and last_prop >= 0, NEG_OVERLAP_LAST_PROP_MESSAGE

        # split text by words while keeping all the whitespace
        seg_list = re.findall("\S+\s*", text)

        # add sub-lists(segment) to final list
        final_seg_list = CutterModel.cut_list_with_overlap(
            input_list=seg_list,
            norm_seg_size=seg_size,
            overlap=overlap,
            last_prop=last_prop
        )

        # join words in each sublist
        final_seg_list = CutterModel.join_sublist_element(
            input_list=final_seg_list
        )

        return final_seg_list

    @staticmethod
    def cut_by_lines(text: str,
                     overlap: int,
                     seg_size: int,
                     last_prop: float) -> List[str]:
        """Cut the input text into segments by number of lines in each segment.

        The size of the segment is measured by counts of lines, with an option
        for an amount of overlap between segments and a minimum proportion
        threshold for the last segment.
        :param text: the string with the contents of the file.
        :param seg_size: the segment size, in lines.
        :param overlap: the number of lines to overlap between segments.
        :param last_prop: the last segment size / other segment size.
        :return: a list of list(segment) that the text has been cut into.
        """
        # pre-condition assertion
        assert seg_size > 0, SEG_NON_POSITIVE_MESSAGE
        assert seg_size > overlap, LARGER_SEG_SIZE_MESSAGE
        assert overlap >= 0 and last_prop >= 0, NEG_OVERLAP_LAST_PROP_MESSAGE

        # split text by new line while keeping all the whitespace
        seg_list = text.splitlines(keepends=True)

        # add sub-lists(segment) to final list
        final_seg_list = CutterModel.cut_list_with_overlap(
            input_list=seg_list,
            norm_seg_size=seg_size,
            overlap=overlap,
            last_prop=last_prop
        )

        # join lines in each sublist
        final_seg_list = CutterModel.join_sublist_element(
            input_list=final_seg_list
        )

        return final_seg_list

    @staticmethod
    def cut_by_segments(text: str, num_segment: int) -> List[str]:
        """Cut the text by the input number of segment (equally sized).

        The chunks created will be equal in terms of word count, or line count
        if the text does not have words separated by whitespace (see Chinese).
        :param text: the string with the contents of the file.
        :param num_segment: number of segments to cut the text into.
        :return a list of list(segment) that the text has been cut into.
        """
        # pre-condition assertion
        assert num_segment > 0, SEG_NON_POSITIVE_MESSAGE

        # split text by words while stripping all the whitespace
        words_list = re.findall("\S+\s*", text)
        total_num_words = len(words_list)

        # the length of normal chunk
        norm_seg_size = int(total_num_words / num_segment)

        # long segment will have one more words in them than norm_seg_size
        num_long_seg = total_num_words % num_segment
        long_seg_size = norm_seg_size + 1

        def get_single_seg(index: int) -> List[str]:
            """Helper to get one single segment with index.

            This function first evaluate whether the segment is the last one
            and grab different segment according to the result, and returns
            sub-lists while index is in the range of number of segment.
            :param index: the index of the segment in the final segment list.
            :return single segment in the input_list based on index.
            """
            if index < num_long_seg:

                return words_list[long_seg_size * index:
                                  long_seg_size * index + long_seg_size]

            else:
                num_norm_seg_in_front = index - num_long_seg
                start = long_seg_size * num_long_seg + \
                    norm_seg_size * num_norm_seg_in_front

                return words_list[start: start + norm_seg_size]

        seg_list = [get_single_seg(index) for index in range(num_segment)]

        # join words in each sublist
        final_seg_list = CutterModel.join_sublist_element(input_list=seg_list)

        return final_seg_list

    @staticmethod
    def cut_by_milestone(text: str, milestone: str) -> List[str]:
        """Cuts the file by milestones.

        :param text: the string with the contents of the file.
        :param milestone: the milestone word that to cut the text by.
        :return: a list of segment that the text has been cut into.
        """
        # pre-condition assertion
        assert len(milestone) > 0, EMPTY_MILESTONE_MESSAGE

        # split text by milestone string
        final_seg_list = text.split(sep=milestone)

        return final_seg_list

    def _cut_selected_files(self):
        if self._cutter_option.cut_by_milestone_option is not None:
            mile_stone = self._cutter_option.cut_by_milestone_option.milestone
            cut_result = {
                label: self.cut_by_milestone(
                    text=content,
                    milestone=mile_stone
                )
                for label, content in self._active_file_label_content_map
            }

        elif self._cutter_option.cut_by_number_of_segments_option is not None:
            num_segment = self._cutter_option.\
                cut_by_number_of_segments_option.number_of_segments

            cut_result = {
                label: self.cut_by_segments(
                    text=content,
                    num_segment=num_segment
                )
                for label, content in self._active_file_label_content_map
            }

        elif self._cutter_option.cut_by_chunk_option.cut_type == "characters":
            option = self._cutter_option.cut_by_chunk_option
            cut_result = {
                label: self.cut_by_characters(
                    text=content,
                    seg_size=option.cut_size,
                    overlap=option.overlap_size,
                    last_prop=option.last_prop
                )
                for label, content in self._active_file_label_content_map
            }

        elif self._cutter_option.cut_by_chunk_option.cut_type == "tokens":
            option = self._cutter_option.cut_by_chunk_option
            cut_result = {
                label: self.cut_by_words(
                    text=content,
                    seg_size=option.cut_size,
                    overlap=option.overlap_size,
                    last_prop=option.last_prop
                )
                for label, content in self._active_file_label_content_map
            }

        elif self._cutter_option.cut_by_chunk_option.cut_type == "lines":
            option = self._cutter_option.cut_by_chunk_option
            cut_result = {
                label: self.cut_by_lines(
                    text=content,
                    seg_size=option.cut_size,
                    overlap=option.overlap_size,
                    last_prop=option.last_prop
                )
                for label, content in self._active_file_label_content_map
            }

        else:
            raise ValueError(INVALID_CUTTING_TYPE_MESSAGE)

        return cut_result

    def get_cut_files(self):
        unprocessed_files = self._cut_selected_files()
        processed_files = [
            [
                (f"{label}_part_{index + 1}", cut_file)
                for index, cut_file in enumerate(cut_files)
            ]
            for label, cut_files in unprocessed_files.items()
        ]

        flat_file_list = [
            file for file_list in processed_files for file in file_list
        ]

        return flat_file_list
