import regex as re

from .extractors.name_extractor import NameExtractor
from .synthesizers import Synthesizer
from .generators import InitialsGenerator

from .exceptions import InvalidInputError

from typing import List, Union, Dict, Tuple
from jellyfish import jaro_winkler_similarity
from itertools import product


SUPPORTED_EXTRACTORS = (
    "NAMES"
)

SUPPORTED_SUBSTITUTORS = (
    "FAKE_INIT"
)

SUPPORTED_SYNTHESIZERS = (
    "INITIAL"
)

class Anonymizer:
    def __init__(self,
            replace_misspelled_names: bool = True,
            replace_single_last_names: bool = True,
            replace_single_first_names: bool = True,
            misspelling_threshold: float = 0.9,
            mimic_casing: bool = True,
            num_replacement_letters: int = 2,
            replacement_separator: str = ".",
            auto_adjust_threshold: bool = False,
            replace_non_breaking_spaces: bool = True
        ):
        self.auto_adjust_threshold = auto_adjust_threshold
        self.misspelling_threshold = misspelling_threshold
        self.replace_single_last_names = replace_single_last_names
        self.replace_single_first_names = replace_single_first_names
        self.replace_non_breaking_spaces = replace_non_breaking_spaces

        self.init_generator = InitialsGenerator(
                                    num_letters = num_replacement_letters,
                                    separator = replacement_separator
                              )

        self.name_extractor = NameExtractor(
                                    allow_fuzzy_matching = replace_misspelled_names,
                                    extract_single_last_names = replace_single_last_names,
                                    extract_single_first_names = replace_single_first_names,
                                    fuzzy_threshold = misspelling_threshold if replace_misspelled_names else 1.0,
                                    mimic_casing = mimic_casing
                              )

        self.synthesizer = Synthesizer()

    def _format_names(self, names: Union[List[str], List[Dict[str,str]]]) -> List[Dict[str,str]]:
        """ Format input names as List[Dict[str, str]] for further processing.

            Parameters:
                names - names to format
            Returns:
                formatted_names - formatted names
        """
        formatted_names = []
        for name in names:
            if isinstance(name, str):
                if "," not in name:
                    raise InvalidInputError(exit_code=3, msg="Incorrect format for names. Correct format is 'last_name, first_name'.")
                last_name, first_name = name.split(",")
                new_name = {"last_name": last_name.strip(), "first_name": first_name.strip()}
                formatted_names.append(new_name)
            elif isinstance(name, dict):
                if not "last_name" in name:
                    raise InvalidInputError(exit_code=4, msg="Missing required key 'last_name' in name.")
                if not "first_name" in name:
                    raise InvalidInputError(exit_code=5, msg="Missing required key 'first_name' in name.")
                formatted_names.append(name)
        return formatted_names

    def _organize_substitutions(self, matches_map: Dict[str, Union[List[str], str]]) -> List[Dict[str, str]]:
        # Prefer map with the highest number of matches:
        matches_map_sorted = sorted(list(matches_map.items()), key=lambda x: len(x[1]["matches"]), reverse=True)
        updated_matches = []
        seen_matches = set()
        for full_name, substitution_data in matches_map_sorted:
            matches = substitution_data["matches"]
            replacer = substitution_data["replacer"]
            for m in matches:
                if m not in seen_matches:
                    updated_matches.append({"full_name": full_name, "match": m, "replacer":  replacer})
            seen_matches.update(matches)
        updated_matches.sort(key=lambda x: len(x["match"]), reverse=True)
        return updated_matches

    def _get_combinations(self, name: str) -> List[str]:
        """ Generate all possible combinations of the name, e.g.:
            name = 'John' -> combinations = ['John']
            name = 'John-Dorian' -> combinations = ['John', 'Dorian', 'John-Dorian']
        """
        name_parts = [np for np in re.split(r"\W", name) if np.strip()]
        combinations = [name]
        for name_part in name_parts:
            combinations.append(name_part)
        combinations = list(set(combinations))
        return combinations

    def _get_name_forms_list(self, names: List[Dict[str, str]]) -> List[List[str]]:
        """ Get lists of name forms in accordance with replace_single_last_name
            and replace_single_first_name params.
        """
        name_forms = []
        for name in names:
            first_name = name["first_name"]
            last_name = name["last_name"]
            full_name = f"{first_name} {last_name}"
            name_parts = [full_name]
            if self.replace_single_last_names:
                last_name_parts = self._get_combinations(last_name)
                name_parts.extend(last_name_parts)
            if self.replace_single_first_names:
                first_name_parts = self._get_combinations(first_name)
                name_parts.extend(first_name_parts)
            name_parts = list(set(name_parts))
            name_forms.append(name_parts)
        return name_forms

    def _get_name_pairs(self, names: List[Dict[str, str]]) -> List[Tuple[str, str]]:
        """ Get all pairs of names to compare.
        """
        name_forms = self._get_name_forms_list(names)
        pairs = []
        for i, name_variations_i in enumerate(name_forms):
            for j, name_variations_j in enumerate(name_forms[i+1:]):
                new_pairs = [np for np in product(name_variations_i, name_variations_j)]
                pairs.extend(new_pairs)

        # Remove possible duplicates
        pairs = [tuple(sorted(p)) for p in pairs]
        pairs = list(set(pairs))
        return pairs

    def _get_adjusted_threshold(self, names: List[Dict[str, str]], eps:float = 0.01) -> float:
        """ Get adjusted threshold: if any two replacable name_parts belonging to
            different name entities have higher similarity than currently set
            similarity threshold, adjust the threshold accordingly.
        """
        names_to_compare = self._get_name_pairs(names)
        max_similarity = 0
        for name_1, name_2 in names_to_compare:
            jw_similarity = jaro_winkler_similarity(name_1, name_2)
            if jw_similarity > max_similarity and jw_similarity < 1.0:
                max_similarity = jw_similarity
        if max_similarity > self.misspelling_threshold:
            adjusted_threshold = min(1.0, max_similarity + eps)
        else:
            adjusted_threshold = self.misspelling_threshold
        return adjusted_threshold

    def _replace_nbsp(self, text: str) -> str:
        """ Replace non-breaking spaces.
        """
        text = re.sub("&nbsp;", " ", text)
        return text

    def anonymize_text(self, text: str, names: List[Dict[str, str]], replacers: List[str]) -> str:
        """ Anonymize given names in given text with given replacers.

            Parameters:
                text - text to anonymize
                names - list of names to anonymize,
                        e.g [{'first_name': 'Adolf', 'last_name': 'Hitler'}]
                replacers - list of replacers (each replacer corresponds to a name in the
                            name list with the same index)
            Returns:
                anonymized_text - text where given names are anonymized

        """
        matches_map = {}

        if self.replace_non_breaking_spaces:
            text = self._replace_nbsp(text)

        if self.auto_adjust_threshold:
            adjusted_threshold = self._get_adjusted_threshold(names)
            self.name_extractor.jw_threshold = adjusted_threshold

        # Step 1: Extract names
        for i, name in enumerate(names):
            replacer = replacers[i]
            full_name = f"{name['first_name']} {name['last_name']}"
            name_matches = self.name_extractor.extract(text, name)
            matches_map[full_name] = {"matches": name_matches, "replacer": replacer}

        organized_matches = self._organize_substitutions(matches_map)


        # Step 2: Replace
        for match in organized_matches:
            replacer_in_correct_form = self.synthesizer.synthesize(match["match"], match["full_name"], match["replacer"], "INITIALS")
            text = re.sub(match["match"], replacer_in_correct_form, text)

        anonymized_text = text
        return anonymized_text

    def anonymize(self, text: str, names: Union[List[str], List[Dict[str,str]]]) -> str:
        """ Anonymize given names in given text.

            Parameters:
                text - text to anonymize
                names - list of names to anonymize,
                        e.g [{'first_name': 'Adolf', 'last_name': 'Hitler'}]
            Returns:
                anonymized_text - text where given names are anonymized

        """
        names = self._format_names(names)
        n = len(names)

        replacers = self.init_generator.generate(n)

        anonymized_text = self.anonymize_text(text, names, replacers)
        return anonymized_text

    def anonymize_texts(self, texts: List[str], names: Union[List[str], List[Dict[str,str]]], consistent_replacement: bool=True) -> str:
        """ Anonymize given names in given texts.

            Parameters:
                texts - texts to anonymize
                names - list of names to anonymize,
                        e.g [{'first_name': 'Adolf', 'last_name': 'Hitler'}]
            Returns:
                anonymized_texts - texts where given names are anonymized

        """
        names = self._format_names(names)
        n = len(names)

        replacers = self.init_generator.generate(n)
        anonymized_texts = []
        for text in texts:
            if not consistent_replacement:
                # Generate new replacements for each text
                replacers = self.init_generator.generate(n)
            anonymized_text = self.anonymize_text(text, names, replacers)
            anonymized_texts.append(anonymized_text)

        return anonymized_texts
