import copy
# enables deepcopying
from statistics import *
#enables simple stats calculations
from scipy import stats as s
#allows for spearman correlation
from src.Music_Shenanigans import *
#checking the viability of find_best_progression from here + all classes needed
ALL_chord_configs = []
# defining global variables

testfig1 = FigBass("I", "")
testfig2 = FigBass("IV", '')
testfig3 = FigBass("V", '')

testlist1 = [testfig1, testfig2, testfig3]

test_list_of_chord_indices = find_best_progression("C", Accidental.Sharp, testlist1)[0]
ALL_chord_configs = find_best_progression("C", Accidental.Sharp, testlist1)[1]
#set up

print("viability check")

def is_future_iteration(shorter_chord_prog: list[int], larger_chord_prog: list[int]) -> bool:
    """
    outputs True if the larger_chord_prog is a future iteration of the shorter_chord_prog
    (all intergers except the ending ones are the same)
    """
    assert len(shorter_chord_prog) != 0 and len(larger_chord_prog) != 0, "one of the lists is empty"
    assert len(larger_chord_prog) > len(shorter_chord_prog), "larger_chord_prog is not longer"
    return larger_chord_prog[0: len(shorter_chord_prog)] == shorter_chord_prog

def corre(list_of_chord_indices: list[list[list[int]]], corre_from: int) -> float:
    corre1 = range(1, len(list_of_chord_indices[corre_from - 2]) + 1)
    #makes corre1, sequence of numbers from 1 to the number of progressions of length corre_from

    ave_prio = []
    for progression in list_of_chord_indices[corre_from - 2]:
        future_iteration_priority_list = []
        i = 0
        while i < len(list_of_chord_indices[corre_from - 1]):
            future_progression = list_of_chord_indices[corre_from - 1][i]
            if is_future_iteration(progression, future_progression):
                future_iteration_priority_list.append(full_progression_priority(future_progression))
            i = i + 1
    #for every progression of length corre_from, finds the priority of all future iterations and puts them in
    # future_iteration_priority_list

        if len(future_iteration_priority_list) == 0:
            ave_prio.append(1000000000)
    #appends arbitrarily large number (a billion) to deal with ones with 0 matches (basically they stop producing valid
    # progressions and cannot be used, thus would be put at the end.)
        else:
            ave_prio.append(mean(future_iteration_priority_list))
    #finds the average of the future_iteration_priority_list for the current progression and puts it into ave_prio
    # so the order of which prios appear in ave_prio is the same order as the already sorted original progressions of
    # length corre_from

    # print(ave_prio)
    #
    ave_prio_copy = copy.deepcopy(ave_prio)
    ave_prio_copy = sorted(ave_prio_copy)
    # print(ave_prio_copy)

    #creates ave_prio_copy and sorts based on how good the progression is

    failed_progression_indices = []
    times_seen = 0
    i = 0
    while i < len(ave_prio):
        if ave_prio[i] == 1000000000:
            failed_progression_indices.append(ave_prio_copy.index(ave_prio[i]) + 1 + times_seen)
            times_seen = times_seen + 1
        else:
            ave_prio[i] = ave_prio_copy.index(ave_prio[i]) + 1
        i = i + 1
    #reassigns ave_prio list based on indices in ave_prio_copy (but makes it stay in the same order to create corre2)
    # print(ave_prio)
    #
    # print(failed_progression_indices)

    corre2 = []
    for reassigned_prog in ave_prio:
        if reassigned_prog == 1000000000:
            corre2.append(mean(failed_progression_indices))
        else:
            corre2.append(reassigned_prog)
    #reassigns failed progressions at the end (makes corre2)
    # print(corre1)
    # print(corre2)
    # print(sorted(corre2))

    return s.spearmanr(corre1, corre2)
    #outputs Spearman correlation value based on corre1 and corre2 list

spearman_corre = corre(test_list_of_chord_indices, 2)
print(spearman_corre)

