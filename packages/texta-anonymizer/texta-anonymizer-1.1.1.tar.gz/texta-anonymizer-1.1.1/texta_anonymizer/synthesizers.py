# -*- coding: utf-8 -*-
import regex as re
from difflib import SequenceMatcher
from typing import List, Dict, Tuple
from .exceptions import InvalidInputError

SUPPORTED_SYNTHESIZERS = (
    "INITIALS"
)

class Synthesizer:
    def __init__(self):
        self.synthesizers = {
                              "INITIALS": InitialsSynthesizerET()
                             }

    def _args_to_list(self, s1_form: str, s1: str, s2: str, synthesizer_type: str) -> List[Tuple[str, str]]:
        args = [("s1_form", s1_form), ("s1", s1), ("s2", s2), ("synthesizer_type", synthesizer_type)]
        return args

    def synthesize(self, s1_form: str, s1: str, s2: str, synthesizer_type="INITIALS") -> str:
        """ Synthesize correct form of s2 based on s1's respective form.

        Parameters:
            s1_form - string s1 in some form, e.g. 'Adolf Hitlerisse'
            s1 - root form of string s1, e.g. 'Adolf Hitler'
            s2 - root form of string s2, e.g. 'Jossif Stalin'

        Returns:
            s2_form - string s2 in the same form as s1_form, e.g. 'Jossif Stalinisse'

        """
        args = self._args_to_list(s1_form, s1, s2, synthesizer_type)

        # Check if synthesizer type is supported
        if synthesizer_type not in SUPPORTED_SYNTHESIZERS:
            raise InvalidInputError(exit_code=1, msg=f"Synthesizer type {synthesizer_type} is not supported.")

        # Check if input types are valid
        for arg, arg_val in args:
            if not isinstance(arg_val, str):
                raise InvalidInputError(exit_code=2, msg=f"Invalid input type for arg {arg}: {type(arg_val)}, excpected type {type('str')}.")

        s2_form = self.synthesizers[synthesizer_type].synthesize(s1_form, s1, s2)

        return s2_form

class InitialsSynthesizerET:
    """ Synthesizing correct forms for initials in Estonian.
    """
    def __init__(self):

        self.endings = ["sse", "st", "ks", "le", "lt", "na", "ni", "ga", "ta", "t", "d", "a", "i", "u", "e", "l"]
        self.end_vocals = {"a", "i", "u", "e"}
        self.f_set_i_morph_1 = {"d", "t"}
        self.f_set_i_morph_2 = {"sse"}

        self._a_set = {"A", "I", "B", "C", "D", "E", "G", "H", "I", "K", "O", "P", "Q", "T", "U", "V", "W", "Y"}
        self._f_set = {"F", "J", "L", "M", "N", "R", "S", "X", "Z"}


    def _get_endings_pattern(self) -> str:
        """ Generate endings pattern.

            Returns:
                pattern - Compiled endings pattern.
        """
        endings_pattern = "|".join(self.endings)
        pattern = f"(?:{endings_pattern})$"
        return re.compile(pattern)


    def _get_longest_substring(self, s1: str, s1_form: str) -> str:
        """ Find longest mutual substring of strings s1 and s1_form.

            Parameters:
                s1 - string 1, e.g. 'Adolf Hitler'
                s1_form - string s1_form, e.g. 'Adolf Hitlerisse'

            Returns:
                longest_subtring - longest mutual substring of s1 and s2, e.g. 'Adolf Hitler'.

        """
        match = SequenceMatcher(None, s1, s1_form).find_longest_match(0, len(s1), 0, len(s1_form))
        longest_substring = s1[match.a:match.a + match.size]
        return longest_substring


    def _get_substitutor_type(self, s2: str) -> str:
        """ Get the type of substitutor based on the last letter of
            substitute string s2.

            Parameters:
                s2 - substitution string.

            Returns:
                substitutor_type - Type of substitutor.
        """

        s2_normalized = s2.strip(".")
        s2_last_char = s2_normalized[-1]

        substitutor_type = "A_SET" if s2_last_char in self._a_set else "F_SET"
        return substitutor_type

    def _get_end_punctuation(self, s1_form: str) -> str:
        """ Get punctuation in the end of detected s1_form, if it exists.

            Parameters:
                s1_form - string s1 in some form, e.g. 'Adolf Hitlerisse'.

            Returns:
                end_punctuation - punctuation in the end of s1_form, e.g. '.'
        """
        end_punctuation = ""
        match = re.search(r"\W+$", s1_form)
        if match:
            end_punctuation = match.group()
        return end_punctuation


    def _get_ending(self, form_ending: str, substitutor_type: str) -> str:
        """ Get correct ending for s2 based on form ending detected from s1_form and
            substitutor_type detected from s2.

            Parameters:
                form_ending - ending detected from s1_form.
                substitutor_type - "A_SET" of "F_SET" based on s2.

            Returns:
                ending - correct ending for s2.
        """
        ending = ""
        best_match = ""

        endings_pattern = self._get_endings_pattern()
        ending_matches = re.findall(endings_pattern, form_ending)
        ending_matches.sort(key=lambda x: len(x), reverse=True)

        if ending_matches:
            best_match = ending_matches[0]

            if best_match in self.f_set_i_morph_1:
                ending = "i" if substitutor_type == "F_SET" else "d"

            elif best_match in self.f_set_i_morph_2:
                ending = "i" if substitutor_type == "F_SET" else best_match

            elif best_match in self.end_vocals:
                    ending = "i" if substitutor_type == "F_SET" else ""

            else:
                ending = best_match if substitutor_type == "A_SET" else f"i{best_match}"
        return ending

    def synthesize(self, s1_form: str, s1: str, s2: str) -> str:
        """ Synthesize correct form of s2 based on s1's respective form.

        Parameters:
            s1_form - string s1 in some form, e.g. 'Adolf Hitlerisse'
            s1 - root form of string s1, e.g. 'Adolf Hitler'
            s2 - replacement initals, e.g. 'K.G'

        Returns:
            s2_form - replacement initals s2 in the same form as s1_form,
                      e.g. 'K.G-sse'
        """
        s1_normalized = re.sub(r"\s+", "", s1.lower())
        s1_form_normalized = re.sub(r"\s+", "", s1_form.lower())

        s2_normalized = s2.strip(".")

        common_substring = self._get_longest_substring(s1_form_normalized, s1_normalized)
        form_ending = s1_form_normalized.split(common_substring)[-1]


        substitutor_type = self._get_substitutor_type(s2)

        ending = self._get_ending(form_ending, substitutor_type)
        end_punctuation = self._get_end_punctuation(s1_form_normalized)
        if ending:
            s2_form = rf"{s2}-{ending}{end_punctuation}"
        else:
            s2_form = rf"{s2}{end_punctuation}"
        return s2_form
