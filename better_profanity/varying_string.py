# -*- coding: utf-8 -*-

from itertools import product


class VaryingString:
    """Represents a string with varying character representations."""

    @staticmethod
    def _create_variants(combos):
        """
        Args:
            combos (list): List of lists of character.
        """
        return tuple("".join(pattern) for pattern in product(*combos))

    def __init__(self, string, char_map={}, variant_thres=10000):
        """
        Args:
            string (str): String to generate variants of.
            char_mappings (dict): Maps characters to substitute characters.
            variant_thres (int): Maximum number of variants to store in a batch.
        """
        self._original = string
        self._sliced_variants = []
        slice_combos = []
        num_slice_variants = 1
        for i, char in enumerate(iter(string)):
            if char in char_map:
                chars = char_map[char]
                num_slice_variants *= len(chars)
                if num_slice_variants > variant_thres:
                    # Finalize slice.
                    variants = VaryingString._create_variants(slice_combos)
                    self._sliced_variants.append(variants)

                    # Move to a new slice.
                    slice_combos = [chars]
                    num_slice_variants = 1
                else:
                    slice_combos.append(chars)
            else:
                slice_combos.append((char,))
        # Finalize final slice.
        variants = VaryingString._create_variants(slice_combos)
        self._sliced_variants.append(variants)
        # There is not necessarily a single length for all of this string's variants.
        # Some character substitutions may include more than one character or empty
        # substitutions.
        self._min_len = 0
        self._max_len = 0
        for slices in self._sliced_variants:
            slice_min = None
            slice_max = None
            for s in slices:
                ls = len(s)
                if slice_min is None:
                    slice_min = ls
                    slice_max = ls
                else:
                    if ls < slice_min:
                        slice_min = ls
                    if ls > slice_max:
                        slice_max = ls
            self._min_len += slice_min
            self._max_len += slice_max

    def __str__(self):
        return self._original

    def __eq__(self, other):
        if self is other:
            return True
        elif other.__class__ == VaryingString:
            # We have no use case for this yet.
            raise NotImplementedError
        elif other.__class__ == str:
            len_other = len(other)
            if len_other < self._min_len or len_other > self._max_len:
                return False
            other_slice = other
            for var_slice in self._sliced_variants:
                match_found = False
                for variant in var_slice:
                    len_var = len(variant)
                    if len(other_slice) >= len_var:
                        if variant == other_slice[:len_var]:
                            other_slice = other_slice[len_var:]
                            match_found = True
                if not match_found:
                    return False
            if other_slice:
                return False
            else:
                return True
        else:
            return False
