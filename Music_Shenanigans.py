#Chord namer/beginning of RCM harmony shenanigans
from Song_List import note
# imports note class from Song_List
import copy
# enables deepcopying
import statistics as stats
#enables stdev

class fig_bass:
    """
    Declares figured bass notation, using roman numerals and inversion notation (both using strings)
    """
    def __init__(self, numeral, inversion):
        self.numeral = numeral
        self.inver = inversion
class chord:
    """
    Declares class "chord", composed of 4 note objects (SATB) and a "priority" (defaulted to 0), a numerical indication
    of how "good" the chord is (in SATB)
    """
    def __init__(self, bass, tenor, alto, soprano, priority = 0):
        self.bass = bass
        self.tenor = tenor
        self.alto = alto
        self.soprano = soprano
        self.prio = priority

def note_names_to_objects(list_of_note_names):
    """
    Takes in a list of note names (strings) and converts them into a list of note objects, returning the newly made
    list of note objects
    """
    list_of_note_objects = []
    for note_name in list_of_note_names:
        new_note = note(note_name[0], note_name[1:], None)
        if new_note.acci == '':
            new_note.acci = 'n'
        list_of_note_objects.append(new_note)
    return list_of_note_objects

def chord_scale_namer(chord_or_scale, root_name, root_acci, type, num_notes):
    """
    Given a "chord" or "scale", root name of the note (str), root accidental applied (str: "x", "#", 'n', 'b', "bb"),
    the number of notes (3/4 for chord, 7 for scale), and type (see dictionary), outputs a chord or scale (as a str, not
    as note objects)
    """
    #outputs a chord or scale with the appropriate named notes (check dictionary in function for "type")
    #returns a final list which has the notes listed as strings
    root_list = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    root_number = root_list.index(root_name)
    bass_notes = []
    note_increment = 0
    if chord_or_scale == "chord":

        while note_increment < num_notes:
            bass_notes.append(root_list[(root_number + note_increment * 2) % 7])
            note_increment += 1
    elif chord_or_scale == "scale":

        while note_increment < num_notes:
            bass_notes.append(root_list[(root_number + note_increment) % 7])
            note_increment += 1
    # ^figures out the names of the "root notes" (aka bass notes) (eg. A C E G) based on primitive white key only list
    full_list = ['C', 'C#/Db', 'D', 'D#/Eb','E','F','F#/Gb','G','G#/Ab','A','A#/Bb','B']
    real_root_number = full_list.index(root_name)
    if root_acci == '#':
        real_root_number += 1
    elif root_acci == 'x':
        real_root_number += 2
    elif root_acci == 'b':
        real_root_number -= 1
    elif root_acci == 'bb':
        real_root_number -= 2
    if real_root_number < 0 or real_root_number > 11:
        real_root_number = (real_root_number + 12) % 12
    # ^figures out the number of the root of the chord (0-11)
    full_list_numbers = []
    add_by_dict = {
        "maj" : [0, 4, 7],
        'min' : [0, 3, 7],
        "aug" : [0, 4, 8],
        "dim" : [0, 3, 6],
        "maj7" : [0, 4, 7, 11],
        "dom7" : [0, 4, 7, 10],
        "min_maj7" : [0, 3, 7, 11],
        "min7" : [0, 3, 7, 10],
        "half_dim7" : [0, 3, 6, 10],
        "dim7" : [0, 3, 6, 9], #^ all above are chords, all below are scales
        "major": [0, 2, 4, 5, 7, 9, 11],
        'nat_minor': [0, 2, 3, 5, 7, 8, 10],
        "har_minor": [0, 2, 3, 5, 7, 8, 11],
        "mel_minor": [0, 2, 3, 5, 7, 9, 11],
        "dorian" : [0, 2, 3, 5, 7, 9, 10],
        "phrygian" : [0, 1, 3, 5, 7, 8, 10],
        "lydian" : [0, 2, 4, 6, 7, 9, 11],
        "mixolydian" : [0, 2, 4, 5, 7, 9, 10],
        "locrian" : [0, 1, 3, 5, 6, 8, 10]
    }
    i = 0
    while i < len(add_by_dict[type]):
        full_list_numbers.append((real_root_number + (add_by_dict[type])[i]) % 12)
        i += 1
    # ^adds the numbers of the other notes in the chord based on the chord type given
    bass_notes_in_full_list = []
    for note in bass_notes:
        i = 0
        while note != full_list[i]:
            i += 1
        bass_notes_in_full_list.append(i)
    # ^figures out the numbers of the original bass notes (based on the full 0-11 list)

    final_list = []
    i = 0
    while i < num_notes:
        acci_diff = full_list_numbers[i] - bass_notes_in_full_list[i]
        if acci_diff in [1, -11]:
            final_list.append(bass_notes[i] + "#")
        elif acci_diff in [2, -10]:
            final_list.append(bass_notes[i] + "x")
        elif acci_diff in [-1, 11]:
            final_list.append(bass_notes[i] + "b")
        elif acci_diff in [-2, 10]:
            final_list.append(bass_notes[i] + "bb")
        else:
            final_list.append(bass_notes[i])
        i += 1
    # ^based on the slight semitone differences, add the appropriate accidentals
    return final_list

def chords_of_scale(root_name, root_acci, type):
    """
    given a scale, finds all the chords (diatonic) built off scale degrees (returns as a list of lists)
    """
    final_list = chord_scale_namer("scale", root_name, root_acci, type)
    chords_list = []
    i = 0
    while i < 7:
        current_chord = []
        current_chord.append(final_list[i])
        current_chord.append(final_list[(i + 2) % 7])
        current_chord.append(final_list[(i + 4) % 7])
        chords_list.append(current_chord)
        i += 1
    if type == "nat_minor":
        if 'bb' in chords_list[4][1]:
            chords_list[4][1] = chords_list[4][1][0] + 'b'
        elif 'b' in chords_list[4][1]:
            chords_list[4][1] = chords_list[4][1][0]
        elif '#' in chords_list[4][1]:
            chords_list[4][1] = chords_list[4][1][0] + 'x'
        else:
            chords_list[4][1] = chords_list[4][1][0] + '#'
    # ^raised 7th for V chord in minor scale adjustment
    return chords_list

def note_movement(first_note, second_note):
    """
    returns movement direction ("Up", "Down", or "None")
    """
    if first_note.name == second_note.name and \
        first_note.acci == second_note.acci and \
        first_note.pitch == second_note.pitch:
        #if it's the same name, no movement
        movement = "None"
    else:
        if second_note.pitch > first_note.pitch:
            movement = "Up"
        elif first_note.pitch > second_note.pitch:
            movement = "Down"
        else:
            full_list = ['C', 'C#/Db', 'D', 'D#/Eb','E','F','F#/Gb','G','G#/Ab','A','A#/Bb','B']
            first_note_number = full_list.index(first_note.name)
            second_note_number = full_list.index(second_note.name)
            if second_note_number > first_note_number:
                movement = "Up"
            elif first_note_number > second_note_number:
                movement = "Down"
            else:
                if first_note.acci == 'bb':
                    first_acci = -2
                elif first_note.acci == 'b':
                    first_acci = -1
                elif first_note.acci == '#':
                    first_acci = 1
                elif first_note.acci == 'x':
                    first_acci = 2
                else:
                    first_acci = 0
                if second_note.acci == 'bb':
                    second_acci = -2
                elif second_note.acci == 'b':
                    second_acci = -1
                elif second_note.acci == '#':
                    second_acci = 1
                elif second_note.acci == 'x':
                    second_acci = 2
                else:
                    second_acci = 0
                if second_acci > first_acci:
                    movement = "Up"
                elif first_acci > second_acci:
                    movement = "Down"

    return movement

def find_bass_chord(root_name, root_acci, fig_bass):
    """
    Given a scale (with a root_name, root_acci and type), produces the chord that is used for the SATB chord (using the
    figured bass notation of numeral and inversion)
    7ths still kinda fucked?
    """
    numeral_list = ["i", "ii", "iii", "iv", "v", "vi", "vii"]

    upd_root_name = root_name
    upd_root_acci = root_acci

    if post_slash(fig_bass.numeral) != fig_bass.numeral:

        if post_slash(fig_bass.numeral) in ["I", "ii", "iii", "IV", "V", 'vi', 'viio']:
            scale_needed_post = "major"
        if post_slash(fig_bass.numeral) in ['i', 'iio', 'III', 'iv', 'V', 'VI', 'VII']:
            scale_needed_post = "nat_minor"

        scale_to_substitute_post = chord_scale_namer("scale", upd_root_name, upd_root_acci, scale_needed_post, 7)
        scale_degree_minus_one_post = numeral_list.index(post_slash(fig_bass.numeral).lower())

        upd_root_name = scale_to_substitute_post[scale_degree_minus_one_post][0]
        upd_root_acci = scale_to_substitute_post[scale_degree_minus_one_post][1:]

        if upd_root_acci == "":
            upd_root_acci = "n"
    # ^adjusts by secondary (dominant) if necessary

    if pre_slash(fig_bass.numeral) in ["I", "ii", "iii", "IV", "V", 'vi', 'viio']:
        scale_needed_pre = "major"
    elif pre_slash(fig_bass.numeral) in ['i', 'iio', 'III', 'iv', 'V', 'VI', 'VII']:
        scale_needed_pre = "nat_minor"

    if pre_slash(fig_bass.numeral)[-1] in ["o", "+"]: #specific instructions for dim and aug chords
        temp_chord = pre_slash(fig_bass.numeral)[0:-1].lower()
    else:
        temp_chord = pre_slash(fig_bass.numeral).lower()

    scale_to_substitute_pre = chord_scale_namer("scale", upd_root_name, upd_root_acci, scale_needed_pre, 7)

    scale_degree_minus_one_pre = numeral_list.index(temp_chord)

    upd_root_name = scale_to_substitute_pre[scale_degree_minus_one_pre][0]
    upd_root_acci = scale_to_substitute_pre[scale_degree_minus_one_pre][1:]

    if upd_root_acci == "":
        upd_root_acci = "n"


    if fig_bass.inver in ["", "6", "6/4"]:
        if pre_slash(fig_bass.numeral) in ["I", "II", "III", "IV", "V", "VI", "VII"]:
            bass_chord = chord_scale_namer("chord", upd_root_name, upd_root_acci, "maj", 3)
        elif pre_slash(fig_bass.numeral) in ["i", "ii", "iii", "iv", "v", "vi", "vii"]:
            bass_chord = chord_scale_namer("chord", upd_root_name, upd_root_acci, "min", 3)
        elif pre_slash(fig_bass.numeral) in ["I+", "II+", "III+", "IV+", "V+", "VI+", "VII+"]:
            bass_chord = chord_scale_namer("chord", upd_root_name, upd_root_acci, "aug", 3)
        elif pre_slash(fig_bass.numeral) in ["io", "iio", "iiio", "ivo", "vo", "vio", "viio"]:
            bass_chord = chord_scale_namer("chord", upd_root_name, upd_root_acci, "dim", 3)

    elif fig_bass.inver in ["7", "6/5", "4/3", "4/2"]:
        if pre_slash(fig_bass.numeral) in ["I", "III", "IV", "VI"]: #maj7
            bass_chord = chord_scale_namer("chord", upd_root_name, upd_root_acci, "maj7", 4)
        elif pre_slash(fig_bass.numeral) in ["V"]: #dom7
            bass_chord = chord_scale_namer("chord", upd_root_name, upd_root_acci, "dom7", 4)
        elif pre_slash(fig_bass.numeral) in ["i", "ii", "iii", "iv", "v", "vi"]: #min7
            bass_chord = chord_scale_namer("chord", upd_root_name, upd_root_acci, "half_dim7", 4)
        elif pre_slash(fig_bass.numeral) == "vii0": #half-dim
            bass_chord = chord_scale_namer("chord", upd_root_name, upd_root_acci, "half_dim7", 4)
        elif pre_slash(fig_bass.numeral) in ["iio", "viio"]: # dim7
            bass_chord = chord_scale_namer("chord", upd_root_name, upd_root_acci, "dim7", 4)


    return bass_chord

def pre_slash(string):
    """
    Returns a string that comes before the slash in the given string; returns the original string if there is no slash
    """
    try:
        slash_index = string.index("/")
        return string[:slash_index]
    except:
        return string

def post_slash(string):
    """
    Returns a string that comes after the slash in the given string; returns the original string if there is no slash
    """
    try:
        slash_index = string.index("/")
        return string[slash_index + 1: ]
    except:
        return string

def is_subset(parent_list, sub_list):
    while len(sub_list) != 0:
        i = 0
        while i < len(sub_list):
            j = 0
            removed = False
            while j < len(parent_list):
                if sub_list[i] == parent_list[j]:
                    sub_list.remove(sub_list[i])
                    parent_list.remove(parent_list[j])
                    removed = True
                    j = len(parent_list)
                else:
                    j += 1
            if removed == True:
                pass
            else:
                return False
    return True

def interval_calc(lower_note, upper_note):
    """
    given a lower note object and an upper note object, returns the bass interval (no major, minor etc)
    of the two notes (includes extensions above an octave)
    """
    root_list = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    lower_number = root_list.index(lower_note.name)
    upper_number = root_list.index(upper_note.name)
    interval = (upper_number - lower_number) + 1
    octave_diff = upper_note.pitch - lower_note.pitch
    interval = interval + (octave_diff * 7)
    return interval

def all_possible_notes(list_of_note_objects, lower_bound_note, upper_bound_note):
    """
    given a list of note objects, a lower bound note object and an upper bound note object (inclusive), determines
    all possible notes with the same note names from the ones in the list that can exist in the given bracket
    returns a list of all possible notes
    """
    lit_all = []
    pitch_range = range(lower_bound_note.pitch, upper_bound_note.pitch + 1)
    i = 0
    while i < len(list_of_note_objects):
        for pitch in pitch_range:
            new_note = note(list_of_note_objects[i].name, list_of_note_objects[i].acci, pitch)
            lit_all.append(new_note)
        i += 1
    # ^creates literally ALL possible notes

    all_poss_notes = []
    for current_note in lit_all:
        movement_result1 = note_movement(lower_bound_note, current_note)
        movement_result2 = note_movement(upper_bound_note, current_note)
        if movement_result1 == "Down" or movement_result2 == "Up":
            pass
        else:
            all_poss_notes.append(current_note)
    return all_poss_notes
    # ^filters out by upper and lower bound

def all_chord_configs(root_name, root_acci, fig_bass, doubled_note):

    bass_chord = find_bass_chord(root_name, root_acci, fig_bass)
    bass_chord_plus_doubled = copy.deepcopy(bass_chord)
    if len(bass_chord) == 3:
        if doubled_note == "root":
            bass_chord_plus_doubled.append(bass_chord_plus_doubled[0])
        elif doubled_note == "third":
            bass_chord_plus_doubled.append(bass_chord_plus_doubled[1])
        elif doubled_note == "fifth":
            bass_chord_plus_doubled.append(bass_chord_plus_doubled[2])
    # ^makes full_chord_name list of name of notes

    list_of_note_objects = note_names_to_objects(bass_chord)
    all_bass_notes = all_possible_notes(list_of_note_objects, note('C', 'n', 2), note('E', 'n', 4))
    all_tenor_notes = all_possible_notes(list_of_note_objects, note('C', 'n', 3), note('G', 'n', 4))
    all_alto_notes = all_possible_notes(list_of_note_objects, note('G', 'n', 3), note('D', 'n', 5))
    all_soprano_notes = all_possible_notes(list_of_note_objects, note('G', 'n', 4), note('C', 'n', 6))

    chord_configs = []
    for bass_note in all_bass_notes:
        for tenor_note in all_tenor_notes:
            current_chord = chord(bass_note, tenor_note, None, None)
            chord_configs.append(current_chord)
    # ^creates all possible notes for each of the voices and all possible mergings of bass and tenor notes

    filtered_chords = []
    for cur_chord in chord_configs:
        movement_result = note_movement(cur_chord.bass, cur_chord.tenor)
        if movement_result == "Up" or movement_result == "None":
            filtered_chords.append(cur_chord)
    chord_configs = copy.deepcopy(filtered_chords)
    # ^filters chords based on tenor needs to be >= to bass

    filtered_chords = []
    for cur_chord in chord_configs:
        note_list = [cur_chord.bass.name, cur_chord.tenor.name]
        all_notes = copy.deepcopy(bass_chord_plus_doubled)
        i = 0
        bass_all_notes = []
        while i < len(all_notes):
            bass_all_notes.append(all_notes[i][0])
            i += 1
        result = is_subset(bass_all_notes, note_list)
        if result == True:
            filtered_chords.append(cur_chord)
    chord_configs = copy.deepcopy(filtered_chords)

    # ^filters based on if the bass and tenor notes are a possible config of the full chord name

    filtered_chords = []
    for cur_chord in chord_configs:
        interval_result = interval_calc(cur_chord.bass, cur_chord.tenor)
        if interval_result <= 12:
            filtered_chords.append(cur_chord)
    chord_configs = copy.deepcopy(filtered_chords)
    # ^filters based on interval between bass and tenor must be <= to a 12th

    updated_configs = []
    for each_chord in chord_configs:
        for alto_note in all_alto_notes:
            current_chord = chord(each_chord.bass, each_chord.tenor, alto_note, None)
            updated_configs.append(current_chord)
    chord_configs = copy.deepcopy(updated_configs)
    # ^adds in all possibilities with alto notes

    filtered_chords = []
    for cur_chord in chord_configs:
        note_list = [cur_chord.bass.name, cur_chord.tenor.name, cur_chord.alto.name]
        all_notes = copy.deepcopy(bass_chord_plus_doubled)
        i = 0
        bass_all_notes = []
        while i < len(all_notes):
            bass_all_notes.append(all_notes[i][0])
            i += 1
        result = is_subset(bass_all_notes, note_list)
        if result == True:
            filtered_chords.append(cur_chord)
    chord_configs = copy.deepcopy(filtered_chords)
    # ^filters based on if the bass, tenor, and alto notes are a possible config of the full chord name

    filtered_chords = []
    for cur_chord in chord_configs:
        movement_result = note_movement(cur_chord.tenor, cur_chord.alto)
        if movement_result == "Up" or movement_result == "None":
            filtered_chords.append(cur_chord)
    chord_configs = copy.deepcopy(filtered_chords)
    # ^filters if alto is >= to tenor

    filtered_chords = []
    for cur_chord in chord_configs:
        interval_result = interval_calc(cur_chord.tenor, cur_chord.alto)
        if interval_result <= 8:
            filtered_chords.append(cur_chord)
    chord_configs = copy.deepcopy(filtered_chords)
    # ^filters if alto and tenor interval exceeds 8

    updated_configs = []
    for each_chord in chord_configs:
        for soprano_note in all_soprano_notes:
            current_chord = chord(each_chord.bass, each_chord.tenor, each_chord.alto, soprano_note)
            updated_configs.append(current_chord)
    chord_configs = copy.deepcopy(updated_configs)
    # ^incorporates soprano notes

    filtered_chords = []
    for cur_chord in chord_configs:
        note_list = [cur_chord.bass.name, cur_chord.tenor.name, cur_chord.alto.name, cur_chord.soprano.name]
        all_notes = copy.deepcopy(bass_chord_plus_doubled)
        i = 0
        bass_all_notes = []
        while i < len(all_notes):
            bass_all_notes.append(all_notes[i][0])
            i += 1
        result = is_subset(bass_all_notes, note_list)
        if result == True:
            filtered_chords.append(cur_chord)
    chord_configs = copy.deepcopy(filtered_chords)
    # ^filters based on chord name

    filtered_chords = []
    for cur_chord in chord_configs:
        interval_result = interval_calc(cur_chord.alto, cur_chord.soprano)
        if interval_result <= 8:
            filtered_chords.append(cur_chord)
    chord_configs = copy.deepcopy(filtered_chords)
    # ^filters on alto and soprano interval being <= to 8th

    filtered_chords = []
    for cur_chord in chord_configs:
        movement_result = note_movement(cur_chord.alto, cur_chord.soprano)
        if movement_result == "Up" or movement_result == "None":
            filtered_chords.append(cur_chord)
    chord_configs = copy.deepcopy(filtered_chords)
    print("final number of chords: " + str(len(chord_configs)))
    # ^filters on soprano being >= alto
    return chord_configs

def chord_priority_updates(chord):
    """
    increases the priority count of the given chord based on the soft caps for the ranges in the bass and soprano
    also now includes calculation of how evenly spread the notes are in the chord, the more even they are, the better
    the chord (adds a simple sd of all the intervals)
    Returns the same chord, now with their .prio updated
    The lower the priority, the better the chord (the more soft caps it violates)
    """
    priority = 0

    bass_lower_bound = note("F", 'n', 3)
    bass_upper_bound = note('C', 'n', 4)
    lower_result = note_movement(bass_lower_bound, chord.bass)
    upper_result = note_movement(bass_upper_bound, chord.bass)
    if lower_result == "Down":
        priority += 1
    if upper_result == "Up":
        priority += 1
    # ^lowers priority based on soft caps in the bass

    soprano_lower_bound = note("C", 'n', 4)
    soprano_upper_bound = note('G', 'n', 5)
    lower_result = note_movement(soprano_lower_bound, chord.soprano)
    upper_result = note_movement(soprano_upper_bound, chord.soprano)
    if lower_result == "Down":
        priority += 1
    if upper_result == "Up":
        priority += 1
    # ^lowers priority based on soft caps in the soprano

    interval_list = [interval_calc(chord.bass, chord.tenor),
                     interval_calc(chord.tenor, chord.alto),
                     interval_calc(chord.alto, chord.soprano)]
    priority = priority + round(stats.stdev(interval_list), 3)
    # ^increases priority based on how good/bad the notes in the chord are spread out

    chord.prio = priority

def lock_bass(chord_configurations, lock, bass_chord):
    """
    filters a list of chords (chord configurations) and returns only those that have the ("root", "third", or "fifth")
    in the bass
    """
    filtered_chords = []
    for each_chord in chord_configurations:
        if lock == "root":
            if each_chord.bass.acci == "n":
                if each_chord.bass.name == bass_chord[0]:
                    filtered_chords.append(each_chord)
            else:
                if each_chord.bass.name + each_chord.bass.acci == bass_chord[0]:
                        filtered_chords.append(each_chord)
        elif lock == "third":
            if each_chord.bass.acci == "n":
                if each_chord.bass.name == bass_chord[1]:
                    filtered_chords.append(each_chord)
            else:
                if each_chord.bass.name + each_chord.bass.acci == bass_chord[1]:
                    filtered_chords.append(each_chord)
        elif lock == "fifth":
            if each_chord.bass.acci == "n":
                if each_chord.bass.name == bass_chord[2]:
                    filtered_chords.append(each_chord)
            else:
                if each_chord.bass.name + each_chord.bass.acci == bass_chord[2]:
                    filtered_chords.append(each_chord)
        elif lock == "seventh":
            if each_chord.bass.acci == "n":
                if each_chord.bass.name == bass_chord[3]:
                    filtered_chords.append(each_chord)
            else:
                if each_chord.bass.name + each_chord.bass.acci == bass_chord[3]:
                    filtered_chords.append(each_chord)

    return filtered_chords

def is_valid_progression(first_chord, second_chord):
    """
    Given two chords, returns a bool (validity) which tells us if the chord progression is valid or not. Currently
    checks for tenor and alto voice crossing (S and B can't voice cross), parallel fifths between all combinations of
    voices and parallel eighths between all combinations of voices.
    (yet to do: check to direct/open fifths/eights)
    """
    global reason #actually needed, the main return is validity

    validity = True
    reason = ""


    fifths_and_octaves_list = [[5, 12, 19, 26, 33], [1, 8, 15, 23, 30, 37]]
    all_pairs = [['bass', 'tenor'],
                 ['bass', 'alto'],
                 ['bass', 'soprano'],
                 ['tenor', 'alto'],
                 ['tenor', 'soprano'],
                 ['alto', 'soprano']]

    if note_movement(first_chord.tenor, second_chord.bass) == "Up":
        validity = False
        reason = "bass voice crosses"
    elif note_movement(first_chord.bass, second_chord.tenor) == "Down" or \
            note_movement(first_chord.alto, second_chord.tenor) == "Up":
        validity = False
        reason = "tenor voice crosses"
    elif note_movement(first_chord.tenor, second_chord.alto) == "Down" or \
            note_movement(first_chord.soprano, second_chord.alto) == "Up":
        validity = False
        reason = "alto voice crosses"
    elif note_movement(first_chord.alto, second_chord.soprano) == "Down":
        validity = False
        reason = "soprano voice crosses"

    list_number = 0
    all_pairs_num = 0
    real_val = False
    while validity:
        locals()['validity'] = True
        local_dict = copy.deepcopy(locals())
        program = "if interval_calc(first_chord." + all_pairs[all_pairs_num][0] + ", " +\
                                   "first_chord." + all_pairs[all_pairs_num][1] + ")" +\
                                   " in " + str(fifths_and_octaves_list[list_number]) + \
                      " and interval_calc(second_chord." + all_pairs[all_pairs_num][0] + ", " +\
                                   "second_chord." + all_pairs[all_pairs_num][1] + ")" + \
                                   " in " + str(fifths_and_octaves_list[list_number]) + ":" + \
                  "\n\tvalidity = False" +\
                  "\n\treason = 'parallel 5th/8ths between " + all_pairs[all_pairs_num][0] + " and " + all_pairs[all_pairs_num][1] + "'"

        #print(program)

        exec(program, globals(), local_dict)
        validity = local_dict['validity']

        if validity:
            if list_number == 0:
                list_number += 1
            else:
                list_number = 0
                if all_pairs_num < 5:
                    all_pairs_num += 1
                else:
                    validity = False
                    real_val = True
    validity = copy.deepcopy(real_val)

    return validity

def find_progression_priority(first_chord, second_chord):
    """
    given two chords, returns how "good" the progression is. Currently calculated through crude methods (lists the
    distance each voice moves from first_chord to second_chord). The smaller the progression_prio, the better the
    movement (in theory)
    """
    list = ["bass", "tenor", "alto", "soprano"]

    bass_movement = 0
    tenor_movement = 0
    alto_movement = 0
    soprano_movement = 0

    i = 0
    while i < 4:
        locals()['bass_movement'] = 0
        locals()['tenor_movement'] = 0
        locals()['alto_movement'] = 0
        locals()['soprano_movement'] = 0
        local_dict = copy.deepcopy(locals())

        program = "if note_movement(first_chord." + list[i] + ", second_chord." + list[i] + ") == 'Up':" +\
            "\n\t" + list[i] + "_movement = interval_calc(first_chord." + list[i] + ", second_chord." + list[i] +")" +\
            "\nelse:" +\
            "\n\t" + list[i] + "_movement = interval_calc(second_chord." + list[i] + ", first_chord." + list[i] + ")"

        exec(program, globals(), local_dict)

        bass_movement = local_dict['bass_movement']
        tenor_movement = local_dict['tenor_movement']
        alto_movement = local_dict['alto_movement']
        soprano_movement = local_dict['soprano_movement']
        i += 1

    progression_prio = bass_movement + tenor_movement + alto_movement + soprano_movement - 4
    return progression_prio

def full_progression_prio(list):
    """
    gives a priority based on how the entire progression looks
    includes how nice each chord looks as well through spacing and chord_prios
    the lower the priority, the better
    """
    i = 0
    priority = 0
    while i < len(list) - 1:
        priority = priority + find_progression_priority(ALL_chord_configs[i][list[i]],
                                                        ALL_chord_configs[i + 1][list[i + 1]])
        i = i + 1
    #finds the sum of the progression priorities between every chord movement

    i = 0
    while i < len(list):
        priority = priority + ALL_chord_configs[i][list[i]].prio
        i = i + 1
    #add factor of how spaced out the chords are and chord prio calculations (based on soft caps)

    return priority

def find_best_progression(root_name, root_acci, list_of_figured_basses):
    """
    takes in a list of fig_bass objects, along with a root_name and root_acci, and outputs the "best" chord progression
    best is deemed through a minimal amount of movement

    deal with doubling rules later
    """
    global ALL_chord_configs
    ALL_chord_configs = []

    for fig in list_of_figured_basses:
        bass_chord = find_bass_chord(root_name, root_acci, fig)
        chord_configs = all_chord_configs(root_name, root_acci, fig, 'root')
        if fig.inver in ["", "7"]:
            bass_locked_chord_configs = lock_bass(chord_configs, "root", bass_chord)
            print(len(bass_locked_chord_configs))
        elif fig.inver in ["6", "6/5"]:
            bass_locked_chord_configs = lock_bass(chord_configs, "third", bass_chord)
            print(len(bass_locked_chord_configs))
        elif fig.inver in ["6/4", "4/3"]:
            bass_locked_chord_configs = lock_bass(chord_configs, "fifth", bass_chord)
            print(len(bass_locked_chord_configs))
        elif fig.inver == "4/2":
            bass_locked_chord_configs = lock_bass(chord_configs, "fifth", bass_chord)
            print(len(bass_locked_chord_configs))

        for each_chord in bass_locked_chord_configs:
            chord_priority_updates(each_chord)
        # ^updates the chord priorities for each of the chords that will eventually make up ALL_chord_configs

        ALL_chord_configs.append(bass_locked_chord_configs)
    #creates list of lists (embedded lists are instances of all_chord_configs of each of the figured basses)

    global final_list
    final_list = []

    size_list = []

    for x in range(len(ALL_chord_configs[0])):
        for y in range(len(ALL_chord_configs[1])):

            if is_valid_progression(ALL_chord_configs[0][x], ALL_chord_configs[1][y]):
                size_list.append([x, y])

    sorted_size_list = sorted(size_list, key = full_progression_prio)

    final_list.append(sorted_size_list)
    #^ sets up the first two chords in their prog_rep

    chord_number_index = 2
    while chord_number_index < len(list_of_figured_basses):
        new_size_list = []
        for prog_rep in final_list[chord_number_index - 2]:
            for x in range(len(ALL_chord_configs[chord_number_index])):
                new_prog_rep = copy.deepcopy(prog_rep) + [x]
                if is_valid_progression(ALL_chord_configs[chord_number_index - 1][new_prog_rep[-2]],
                                        ALL_chord_configs[chord_number_index][new_prog_rep[-1]]):
                    new_size_list.append(new_prog_rep)

        new_sorted_size_list = sorted(new_size_list, key = full_progression_prio)

        final_list.append(new_sorted_size_list)
        chord_number_index = chord_number_index + 1

    print(len(final_list))
    #repeats for all the other figured basses

    number_of_progs_outputted = 0
    while number_of_progs_outputted < 10:
        prog = final_list[-1][number_of_progs_outputted]
        for x in range(len(prog)):
            print(chord_spread(ALL_chord_configs[x][prog[x]]))
        print(full_progression_prio(prog))
        print("next")
        number_of_progs_outputted = number_of_progs_outputted + 1

    #print out the top 10 full chord progs

def chord_spread(chord):
    """
    given a chord, returns a list which is a readable version of the chord
    [bass, tenor, alto, soprano] (plus chord prio just in case)
    """
    readable_spread = [chord.bass.name + chord.bass.acci + str(chord.bass.pitch),
            chord.tenor.name + chord.tenor.acci + str(chord.tenor.pitch),
            chord.alto.name + chord.alto.acci + str(chord.alto.pitch),
            chord.soprano.name + chord.soprano.acci + str(chord.soprano.pitch),
            chord.prio]
    return readable_spread


#if __name__ == '__main__':

testfig1 = fig_bass("I", "")
testfig2 = fig_bass("V/ii", '7')
testfig3 = fig_bass("ii", '')
testfig4 = fig_bass("V/V", '4/2')
testfig5 = fig_bass("V/iii", '4/3')
testfig6 = fig_bass("V", '4/2')
testfig7 = fig_bass("I", '6')

testlist1 = [testfig1, testfig2, testfig3, testfig4, testfig5, testfig6, testfig7]

find_best_progression("C", "n", testlist1)

#things to work on next:
#implementation of secondary doms
#implementation of doubling rules
#max number of chords used for next generation (maybe use R to check viability of that)
#filtering final chord list via specific notes (do it before generation to reduce time)
#try and figure out if the sd thing is the best way of checking spread/ how it affects movement between chords