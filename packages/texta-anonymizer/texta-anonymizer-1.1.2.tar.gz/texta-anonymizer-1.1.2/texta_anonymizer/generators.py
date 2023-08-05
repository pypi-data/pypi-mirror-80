# -*- coding: utf-8 -*-
import regex as re
from itertools import product
from string import ascii_uppercase as alphabet
from random import sample
from typing import List, Dict, Tuple

class InitialsGenerator:
    def __init__(self, num_letters: int = 2, separator: str = "."):
        self.num_letters = num_letters
        self.separator = separator

        self.initials_list = self._get_initials_list()


    def _get_initials_list(self) -> List[str]:
        """ Generate all possible initals' combinations containing
            given number of letters.

            Returns:
                initials_list - all possible combinations of initials containg
                                given number of letters.

        """
        initials_list = [self.separator.join(init_p) for init_p in list(product(alphabet, repeat=self.num_letters))]
        return initials_list

    def set_params(self, **kwargs):
        """ Add new generator settings and generate new initials list
            based on the given settings.

            Parameters:
                num_letters - number of letters in each initals' pattern.
                separator - separator to separate the letters with.

        """
        if "num_letters" in kwargs:
            self.num_letters = kwargs["num_letters"]
        if "separator" in kwargs:
            self.separator = kwargs["separator"]
        self.initials_list = self._get_initials_list()

    def generate(self, n: int) -> List[str]:
        """ Generate n pairs of initials with given params.

            Parameters:
                n - number of different initals to be generated.

            Returns:
                initials - list of randomly generated initials.
        """
        initials = sample(self.initials_list, n)
        return initials
