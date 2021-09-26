from copy import deepcopy
from statistics import *

from scipy import stats as s

from src.Music_Shenanigans import *

_arbitrary_high_value: int = 1000000000


def is_future_iteration(shorter_chord_progression: list[int], larger_chord_progression: list[int]) -> bool:
    """
    outputs True if the larger_chord_progression is a future iteration of the shorter_chord_progression
    (all integers except the ending ones are the same)
    """
    assert len(shorter_chord_progression) != 0 and len(larger_chord_progression) != 0, "one of the lists is empty"
    assert len(larger_chord_progression) > len(shorter_chord_progression), "larger_chord_progression is not longer"
    return larger_chord_progression[0: len(shorter_chord_progression)] == shorter_chord_progression


def correlation(list_of_chord_indices: list[list[list[int]]], correlation_from: int) -> float:
    # Sequence of numbers from 1 to the number of progressions of length correlation_from
    sample_one: range = range(1, len(list_of_chord_indices[correlation_from - 2]) + 1)
    average_priority: list[int] = list(map(lambda x: _arbitrary_high_value if len(x) == 0 else mean(x),
                                           map(lambda y: list(map(full_progression_priority,
                                                                  filter(lambda z: is_future_iteration(y, z),
                                                                         list_of_chord_indices[correlation_from - 1]))),
                                               list_of_chord_indices[correlation_from - 2])))
    average_priority_copy = sorted(deepcopy(average_priority))
    try:
        failed_progression_indices_mean = average_priority_copy.index(_arbitrary_high_value) + 1 + \
                                          ((average_priority_copy.count(_arbitrary_high_value) - 1) / 2)
    except ValueError:
        failed_progression_indices_mean = _arbitrary_high_value
    average_priority = list(
        map(lambda x: x if x == _arbitrary_high_value else average_priority_copy.index(x) + 1, average_priority))
    sample_two = list(
        map(lambda x: failed_progression_indices_mean if x == _arbitrary_high_value else x, average_priority))
    return s.spearmanr(sample_one, sample_two)


if __name__ == "__main__":
    # Setup
    testlist1 = [FigBass("I", ""), FigBass("IV", ""), FigBass("V", "")]
    (test_list_of_chord_indices, ALL_chord_configs) = find_best_progression("C", Accidental.Sharp, testlist1)

    print(correlation(test_list_of_chord_indices, 2))
