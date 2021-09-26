# enables deep copying
from copy import deepcopy
from statistics import *

# enables simple stats calculations
from scipy import stats as s

# allows for spearman correlation
from src.Music_Shenanigans import *

_arbitrary_high_value: int = 1000000000


# checking the viability of find_best_progression from here + all classes needed


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

    average_priority: list[int] = []
    # for every progression of length correlation_from, finds the priority of all future iterations and puts them in
    # future_iteration_priority_list
    for progression_index in list_of_chord_indices[correlation_from - 2]:
        future_iteration_priority_list = []
        for future_progression in list_of_chord_indices[correlation_from - 1]:
            if is_future_iteration(progression_index, future_progression):
                future_iteration_priority_list.append(full_progression_priority(future_progression))
        # Finds the average of the future_iteration_priority_list for the current progression
        # and puts it into average_priority so the order of which priorities appear in average_priority
        # is the same order as the already sorted original progressions of length correlation_from
        # If no elements exist, append arbitrarily large number to deal with ones with 0 matches
        # since they stop producing valid progressions and cannot be used, thus put at the end
        if len(future_iteration_priority_list) == 0:
            average_priority.append(_arbitrary_high_value)
        else:
            average_priority.append(mean(future_iteration_priority_list))

    # print(average_priority)
    average_priority_copy = sorted(deepcopy(average_priority))
    # print(average_priority_copy)

    # creates average_priority_copy and sorts based on how good the progression is

    failed_progression_indices = []
    times_seen = 0
    for i in range(len(average_priority)):
        if average_priority[i] == _arbitrary_high_value:
            failed_progression_indices.append(average_priority_copy.index(average_priority[i]) + 1 + times_seen)
            times_seen += 1
        else:
            average_priority[i] = average_priority_copy.index(average_priority[i]) + 1
    # reassigns average_priority list based on indices in average_priority_copy
    # (but makes it stay in the same order to create sample_two)
    # print(average_priority)
    #
    # print(failed_progression_indices)

    failed_progression_indices_mean = mean(failed_progression_indices)
    sample_two = []
    for reassigned_prog in average_priority:
        if reassigned_prog == _arbitrary_high_value:
            sample_two.append(mean(failed_progression_indices))
        else:
            sample_two.append(reassigned_prog)
    # reassigns failed progressions at the end (makes sample_two)
    # print(sample_one)
    # print(sample_two)
    # print(sorted(sample_two))

    # outputs Spearman correlation value based on sample_one and sample_two list
    return s.spearmanr(sample_one, sample_two)


if __name__ == "__main__":
    # Setup
    testlist1 = [FigBass("I", ""), FigBass("IV", ""), FigBass("V", "")]
    (test_list_of_chord_indices, ALL_chord_configs) = find_best_progression("C", Accidental.Sharp, testlist1)

    print(correlation(test_list_of_chord_indices, 2))
