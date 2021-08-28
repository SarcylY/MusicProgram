# Chord namer/beginning of RCM harmony shenanigans

import copy

from src.Music.MusicStructures import *


# enables deepcopying

# enables stdev


def chord_scale_namer(chord_or_scale: ChordOrScale,
                      root_name: str,
                      root_acci: str,
                      chord_type: str,
                      num_notes: int) -> list[str]:
    """
    Given a chord or scale, root name of the note (str), root accidental applied (str: "x", "#", 'n', 'b', "bb"),
    the number of notes (3/4 for chord, 7 for scale), and type (see dictionary), outputs a chord or scale (as a str, not
    as note objects)
    """
    # outputs a chord or scale with the appropriate named notes (check dictionary in function for "type")
    # returns a final list which has the notes listed as strings
    root_list = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    root_number = root_list.index(root_name)
    bass_notes = []
    note_increment = 0
    if chord_or_scale == ChordOrScale.Chord:
        while note_increment < num_notes:
            bass_notes.append(root_list[(root_number + note_increment * 2) % 7])
            note_increment += 1
    else:
        while note_increment < num_notes:
            bass_notes.append(root_list[(root_number + note_increment) % 7])
            note_increment += 1
    # ^figures out the names of the "root notes" (aka bass notes) (eg. A C E G) based on primitive white key only list
    full_list = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
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
        "maj": [0, 4, 7],
        'min': [0, 3, 7],
        "aug": [0, 4, 8],
        "dim": [0, 3, 6],
        "maj7": [0, 4, 7, 11],
        "dom7": [0, 4, 7, 10],
        "min_maj7": [0, 3, 7, 11],
        "min7": [0, 3, 7, 10],
        "half_dim7": [0, 3, 6, 10],
        "dim7": [0, 3, 6, 9],  # ^ all above are chords, all below are scales
        "major": [0, 2, 4, 5, 7, 9, 11],
        'nat_minor': [0, 2, 3, 5, 7, 8, 10],
        "har_minor": [0, 2, 3, 5, 7, 8, 11],
        "mel_minor": [0, 2, 3, 5, 7, 9, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "phrygian": [0, 1, 3, 5, 7, 8, 10],
        "lydian": [0, 2, 4, 6, 7, 9, 11],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
        "locrian": [0, 1, 3, 5, 6, 8, 10]
    }
    i = 0
    while i < len(add_by_dict[chord_type]):
        full_list_numbers.append((real_root_number + (add_by_dict[chord_type])[i]) % 12)
        i += 1
    # ^adds the numbers of the other notes in the chord based on the chord type given
    bass_notes_in_full_list = []
    for note in bass_notes:
        i = 0
        while note != full_list[i]:
            i += 1
        bass_notes_in_full_list.append(i)
    # ^figures out the numbers of the original bass notes (based on the full 0-11 list)

    result_list = []
    i = 0
    while i < num_notes:
        acci_diff = full_list_numbers[i] - bass_notes_in_full_list[i]
        if acci_diff in [1, -11]:
            result_list.append(bass_notes[i] + "#")
        elif acci_diff in [2, -10]:
            result_list.append(bass_notes[i] + "x")
        elif acci_diff in [-1, 11]:
            result_list.append(bass_notes[i] + "b")
        elif acci_diff in [-2, 10]:
            result_list.append(bass_notes[i] + "bb")
        else:
            result_list.append(bass_notes[i])
        i += 1
    # ^based on the slight semitone differences, add the appropriate accidentals
    return result_list


def chords_of_scale(root_name: str, root_acci: str, chord_type: str) -> list[list[str]]:
    """
    given a scale, finds all the chords (diatonic) built off scale degrees (returns as a list of lists)
    """
    result_list = chord_scale_namer(ChordOrScale.Scale, root_name, root_acci, chord_type, 7)
    chords_list = []
    i = 0
    while i < 7:
        current_chord = [result_list[i], result_list[(i + 2) % 7], result_list[(i + 4) % 7]]
        chords_list.append(current_chord)
        i += 1
    if chord_type == "nat_minor":
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


def find_bass_chord(root_name: str, root_acci: str, fig_bass: FigBass) -> list[str]:
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
        elif post_slash(fig_bass.numeral) in ['i', 'iio', 'III', 'iv', 'V', 'VI', 'VII']:
            scale_needed_post = "nat_minor"
        else:
            raise Exception("Invalid chord/scale")

        scale_to_substitute_post = chord_scale_namer(ChordOrScale.Scale, upd_root_name, upd_root_acci,
                                                     scale_needed_post, 7)
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
    else:
        raise Exception("Invalid chord")

    if pre_slash(fig_bass.numeral)[-1] in ["o", "+"]:  # specific instructions for dim and aug chords
        temp_chord = pre_slash(fig_bass.numeral)[0:-1].lower()
    else:
        temp_chord = pre_slash(fig_bass.numeral).lower()

    scale_to_substitute_pre = chord_scale_namer(ChordOrScale.Scale, upd_root_name, upd_root_acci, scale_needed_pre, 7)

    scale_degree_minus_one_pre = numeral_list.index(temp_chord)

    upd_root_name = scale_to_substitute_pre[scale_degree_minus_one_pre][0]
    upd_root_acci = scale_to_substitute_pre[scale_degree_minus_one_pre][1:]

    if upd_root_acci == "":
        upd_root_acci = "n"

    if fig_bass.inversion in ["", "6", "6/4"]:
        if pre_slash(fig_bass.numeral) in ["I", "II", "III", "IV", "V", "VI", "VII"]:
            return chord_scale_namer(ChordOrScale.Chord, upd_root_name, upd_root_acci, "maj", 3)
        elif pre_slash(fig_bass.numeral) in ["i", "ii", "iii", "iv", "v", "vi", "vii"]:
            return chord_scale_namer(ChordOrScale.Chord, upd_root_name, upd_root_acci, "min", 3)
        elif pre_slash(fig_bass.numeral) in ["I+", "II+", "III+", "IV+", "V+", "VI+", "VII+"]:
            return chord_scale_namer(ChordOrScale.Chord, upd_root_name, upd_root_acci, "aug", 3)
        elif pre_slash(fig_bass.numeral) in ["io", "iio", "iiio", "ivo", "vo", "vio", "viio"]:
            return chord_scale_namer(ChordOrScale.Chord, upd_root_name, upd_root_acci, "dim", 3)

    elif fig_bass.inversion in ["7", "6/5", "4/3", "4/2"]:
        if pre_slash(fig_bass.numeral) in ["I", "III", "IV", "VI"]:  # maj7
            return chord_scale_namer(ChordOrScale.Chord, upd_root_name, upd_root_acci, "maj7", 4)
        elif pre_slash(fig_bass.numeral) in ["V"]:  # dom7
            return chord_scale_namer(ChordOrScale.Chord, upd_root_name, upd_root_acci, "dom7", 4)
        elif pre_slash(fig_bass.numeral) in ["i", "ii", "iii", "iv", "v", "vi"]:  # min7
            return chord_scale_namer(ChordOrScale.Chord, upd_root_name, upd_root_acci, "half_dim7", 4)
        elif pre_slash(fig_bass.numeral) == "vii0":  # half-dim
            return chord_scale_namer(ChordOrScale.Chord, upd_root_name, upd_root_acci, "half_dim7", 4)
        elif pre_slash(fig_bass.numeral) in ["iio", "viio"]:  # dim7
            return chord_scale_namer(ChordOrScale.Chord, upd_root_name, upd_root_acci, "dim7", 4)
    raise RuntimeError("Should never be reached")


def pre_slash(string: str) -> str:
    """
    Returns a string that comes before the slash in the given string; returns the original string if there is no slash
    """
    temp_array = string.split("/")
    if len(temp_array) <= 1:
        return string
    return temp_array[0]


def post_slash(string):
    """
    Returns a string that comes after the slash in the given string; returns the original string if there is no slash
    """
    temp_array = string.split("/", 1)
    if len(temp_array) <= 1:
        return string
    return temp_array[1]


def interval_calc(lower_note: Note, upper_note: Note) -> int:
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


def all_possible_notes(list_of_note_objects: list[Note], lower_bound_note: Note, upper_bound_note: Note) -> list[Note]:
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
            new_note = Note(list_of_note_objects[i].name, list_of_note_objects[i].accidental, pitch)
            lit_all.append(new_note)
        i += 1
    # ^creates literally ALL possible notes

    all_poss_notes = []
    for current_note in lit_all:
        movement_result1 = note_movement(lower_bound_note, current_note)
        movement_result2 = note_movement(upper_bound_note, current_note)
        if movement_result1 != MovementDirection.Down and movement_result2 != MovementDirection.Up:
            all_poss_notes.append(current_note)
    return all_poss_notes
    # ^filters out by upper and lower bound


def all_chord_configs(root_name: str, root_acci: str, fig_bass: FigBass, doubled_note: DoubledNote) -> list[Chord]:
    """
    """
    bass_chord = find_bass_chord(root_name, root_acci, fig_bass)
    bass_chord_plus_doubled = copy.deepcopy(bass_chord)
    if len(bass_chord) == 3:
        if doubled_note == DoubledNote.Root:
            bass_chord_plus_doubled.append(bass_chord_plus_doubled[0])
        elif doubled_note == DoubledNote.Third:
            bass_chord_plus_doubled.append(bass_chord_plus_doubled[1])
        elif doubled_note == DoubledNote.Fifth:
            bass_chord_plus_doubled.append(bass_chord_plus_doubled[2])
    # ^makes full_chord_name list of name of notes

    list_of_note_objects = [Note.note_from_string(string) for string in bass_chord]
    all_bass_notes = all_possible_notes(list_of_note_objects, Note('C', 'n', 2), Note('E', 'n', 4))
    all_tenor_notes = all_possible_notes(list_of_note_objects, Note('C', 'n', 3), Note('G', 'n', 4))
    all_alto_notes = all_possible_notes(list_of_note_objects, Note('G', 'n', 3), Note('D', 'n', 5))
    all_soprano_notes = all_possible_notes(list_of_note_objects, Note('G', 'n', 4), Note('C', 'n', 6))

    all_notes = [note if note[0] != note[-1] else note + "n" for note in bass_chord_plus_doubled]

    chord_configs = []
    for bass_note in all_bass_notes:
        for tenor_note in all_tenor_notes:
            current_chord = Chord(bass_note, tenor_note, None, None)
            chord_configs.append(current_chord)
    # ^creates all possible notes for each of the voices and all possible mergings of bass and tenor notes

    filtered_chords = []
    for cur_chord in chord_configs:
        movement_result = note_movement(cur_chord.bass, cur_chord.tenor)
        if movement_result != MovementDirection.Down:
            filtered_chords.append(cur_chord)
    chord_configs = copy.deepcopy(filtered_chords)
    # ^filters chords based on tenor needs to be >= to bass

    filtered_chords = []
    for cur_chord in chord_configs:
        note_list = [cur_chord.bass.name + cur_chord.bass.accidental,
                     cur_chord.tenor.name + cur_chord.tenor.accidental]
        result = set(mark_duplicate(note_list)).issubset(mark_duplicate(all_notes))
        if result:
            filtered_chords.append(cur_chord)
    chord_configs = copy.deepcopy(filtered_chords)
    # ^filters based on if the bass and tenor notes are a possible config of the full chord name

    filtered_chords = []
    for cur_chord in chord_configs:
        interval_result = get_bass_interval(cur_chord.bass, cur_chord.tenor)
        if interval_result <= 12:
            filtered_chords.append(cur_chord)
    chord_configs = copy.deepcopy(filtered_chords)
    # ^filters based on interval between bass and tenor must be <= to a 12th

    updated_configs = []
    for each_chord in chord_configs:
        for alto_note in all_alto_notes:
            current_chord = Chord(each_chord.bass, each_chord.tenor, alto_note, None)
            updated_configs.append(current_chord)
    chord_configs = copy.deepcopy(updated_configs)
    # ^adds in all possibilities with alto notes

    filtered_chords = []
    for cur_chord in chord_configs:
        note_list = [cur_chord.bass.name + cur_chord.bass.accidental,
                     cur_chord.tenor.name + cur_chord.tenor.accidental,
                     cur_chord.alto.name + cur_chord.alto.accidental]
        result = set(mark_duplicate(note_list)).issubset(mark_duplicate(all_notes))
        if result:
            filtered_chords.append(cur_chord)
    chord_configs = copy.deepcopy(filtered_chords)
    # ^filters based on if the bass, tenor, and alto notes are a possible config of the full chord name

    filtered_chords = []
    for cur_chord in chord_configs:
        movement_result = note_movement(cur_chord.tenor, cur_chord.alto)
        if movement_result != MovementDirection.Down:
            filtered_chords.append(cur_chord)
    chord_configs = copy.deepcopy(filtered_chords)
    # ^filters if alto is >= to tenor

    filtered_chords = []
    for cur_chord in chord_configs:
        interval_result = get_bass_interval(cur_chord.tenor, cur_chord.alto)
        if interval_result <= 8:
            filtered_chords.append(cur_chord)
    chord_configs = copy.deepcopy(filtered_chords)
    # ^filters if alto and tenor interval exceeds 8

    updated_configs = []
    for each_chord in chord_configs:
        for soprano_note in all_soprano_notes:
            current_chord = Chord(each_chord.bass, each_chord.tenor, each_chord.alto, soprano_note)
            updated_configs.append(current_chord)
    chord_configs = copy.deepcopy(updated_configs)
    # ^incorporates soprano notes

    filtered_chords = []
    for cur_chord in chord_configs:
        note_list = [cur_chord.bass.name + cur_chord.bass.accidental,
                     cur_chord.tenor.name + cur_chord.tenor.accidental,
                     cur_chord.alto.name + cur_chord.alto.accidental,
                     cur_chord.soprano.name + cur_chord.soprano.accidental]
        result = set(mark_duplicate(note_list)).issubset(mark_duplicate(all_notes))
        if result:
            filtered_chords.append(cur_chord)
    chord_configs = copy.deepcopy(filtered_chords)
    # ^filters based on chord name

    filtered_chords = []
    for cur_chord in chord_configs:
        interval_result = get_bass_interval(cur_chord.alto, cur_chord.soprano)
        if interval_result <= 8:
            filtered_chords.append(cur_chord)
    chord_configs = copy.deepcopy(filtered_chords)
    # ^filters on alto and soprano interval being <= to 8th

    filtered_chords = []
    for cur_chord in chord_configs:
        movement_result = note_movement(cur_chord.alto, cur_chord.soprano)
        if movement_result != MovementDirection.Down:
            filtered_chords.append(cur_chord)
    chord_configs = copy.deepcopy(filtered_chords)
    print("final number of chords: " + str(len(chord_configs)))
    # ^filters on soprano being >= alto
    return chord_configs


def mark_duplicate(note_list: list[str]) -> list[str]:
    """
    marks a duplicate value in a list of notes (written as strings) by appending a "d"
    """
    for note in note_list:
        if note_list.count(note) != 1:
            note_list[(len(note_list) - 1) - list(reversed(note_list)).index(note)] = \
                note_list[(len(note_list) - 1) - list(reversed(note_list)).index(note)] + "d"
    return note_list


def lock_bass(chord_configurations: list[Chord], lock: str, bass_chord: list[str]) -> list[Chord]:
    """
    Refactoring note: lock is one of "root", "third", "fifth" or "seventh"
    filters a list of chords (chord configurations) and returns only those that have the ("root", "third", or "fifth")
    in the bass
    """
    filtered_chords = []
    for each_chord in chord_configurations:
        if lock == "root":
            if each_chord.bass.accidental == "n":
                if each_chord.bass.name == bass_chord[0]:
                    filtered_chords.append(each_chord)
            else:
                if each_chord.bass.name + each_chord.bass.accidental == bass_chord[0]:
                    filtered_chords.append(each_chord)
        elif lock == "third":
            if each_chord.bass.accidental == "n":
                if each_chord.bass.name == bass_chord[1]:
                    filtered_chords.append(each_chord)
            else:
                if each_chord.bass.name + each_chord.bass.accidental == bass_chord[1]:
                    filtered_chords.append(each_chord)
        elif lock == "fifth":
            if each_chord.bass.accidental == "n":
                if each_chord.bass.name == bass_chord[2]:
                    filtered_chords.append(each_chord)
            else:
                if each_chord.bass.name + each_chord.bass.accidental == bass_chord[2]:
                    filtered_chords.append(each_chord)
        elif lock == "seventh":
            if each_chord.bass.accidental == "n":
                if each_chord.bass.name == bass_chord[3]:
                    filtered_chords.append(each_chord)
            else:
                if each_chord.bass.name + each_chord.bass.accidental == bass_chord[3]:
                    filtered_chords.append(each_chord)

    return filtered_chords


def is_valid_progression(first_chord: Chord, second_chord: Chord) -> (bool, str):
    """
    Given two chords, returns a bool (validity) which tells us if the chord progression is valid or not. Currently
    checks for tenor and alto voice crossing (S and B can't voice cross), parallel fifths between all combinations of
    voices and parallel eighths between all combinations of voices.
    (yet to do: check to direct/open fifths/eights)
    """
    if note_movement(first_chord.tenor, second_chord.bass) == MovementDirection.Up:
        return False, "bass voice crosses"
    elif note_movement(first_chord.bass, second_chord.tenor) == MovementDirection.Down or \
            note_movement(first_chord.alto, second_chord.tenor) == MovementDirection.Up:
        return False, "tenor voice crosses"
    elif note_movement(first_chord.tenor, second_chord.alto) == MovementDirection.Down or \
            note_movement(first_chord.soprano, second_chord.alto) == MovementDirection.Up:
        return False, "alto voice crosses"
    elif note_movement(first_chord.alto, second_chord.soprano) == MovementDirection.Down:
        return False, "soprano voice crosses"
    # ^checks for voice crossings

    if precise_interval_calc(first_chord.bass, first_chord.tenor) in ["P1", "P5", "P8", "P12"] and \
            precise_interval_calc(second_chord.bass, second_chord.tenor) == precise_interval_calc(first_chord.bass,
                                                                                                  first_chord.tenor):
        return False, "parallel movement between bass and tenor"
    elif precise_interval_calc(first_chord.tenor, first_chord.alto) in ["P1", "P5", "P8", "P12"] and \
            precise_interval_calc(second_chord.tenor, second_chord.alto) == precise_interval_calc(first_chord.tenor,
                                                                                                  first_chord.alto):
        return False, "parallel movement between tenor and alto"
    elif precise_interval_calc(first_chord.alto, first_chord.soprano) in ["P1", "P5", "P8", "P12"] and \
            precise_interval_calc(second_chord.alto, second_chord.soprano) == \
            precise_interval_calc(first_chord.alto, first_chord.soprano):
        return False, "parallel movement between alto and soprano"
    elif precise_interval_calc(first_chord.bass, first_chord.alto) in ["P1", "P5", "P8", "P12"] and \
            precise_interval_calc(second_chord.bass, second_chord.alto) == precise_interval_calc(first_chord.bass,
                                                                                                 first_chord.alto):
        return False, "parallel movement between bass and alto"
    elif precise_interval_calc(first_chord.bass, first_chord.soprano) in ["P1", "P5", "P8", "P12"] and \
            precise_interval_calc(second_chord.bass, second_chord.soprano) == \
            precise_interval_calc(first_chord.bass, first_chord.soprano):
        return False, "parallel movement between bass and soprano"
    elif precise_interval_calc(first_chord.tenor, first_chord.soprano) in ["P1", "P5", "P8", "P12"] and \
            precise_interval_calc(second_chord.tenor, second_chord.soprano) == \
            precise_interval_calc(first_chord.tenor, first_chord.soprano):
        return False, "parallel movement between tenor and soprano"
    # ^checks for parallel movement between the chords

    return True, "valid"


def find_progression_priority(first_chord: Chord, second_chord: Chord) -> int:
    """
    given two chords, returns how "good" the progression is. Currently calculated through crude methods (lists the
    distance each voice moves from first_chord to second_chord). The smaller the progression_prio, the better the
    movement (in theory)
    """
    voice_list = ["bass", "tenor", "alto", "soprano"]

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

        program = "if note_movement(first_chord." + voice_list[i] + ", second_chord." + voice_list[i] + ") == 'Up':" + \
                  "\n\t" + voice_list[i] + "_movement = bass_interval(first_chord." + voice_list[i] \
                  + ", second_chord." + voice_list[i] + ")" + "\nelse:" + \
                  "\n\t" + voice_list[i] + "_movement = bass_interval(second_chord." + voice_list[i] \
                  + ", first_chord." + voice_list[i] + ")"

        exec(program, globals(), local_dict)

        bass_movement = local_dict['bass_movement']
        tenor_movement = local_dict['tenor_movement']
        alto_movement = local_dict['alto_movement']
        soprano_movement = local_dict['soprano_movement']
        i += 1

    progression_prio = bass_movement + tenor_movement + alto_movement + soprano_movement - 4
    return progression_prio


def full_progression_prio(chord_list: list[int]) -> int:
    """
    gives a priority based on how the entire progression looks
    includes how nice each chord looks as well through spacing and chord_prios
    the lower the priority, the better
    """
    i = 0
    priority = 0
    while i < len(chord_list) - 1:
        priority = priority + find_progression_priority(ALL_chord_configs[i][chord_list[i]],
                                                        ALL_chord_configs[i + 1][chord_list[i + 1]])
        i = i + 1
    # finds the sum of the progression priorities between every chord movement

    i = 0
    while i < len(chord_list):
        priority = priority + ALL_chord_configs[i][chord_list[i]].priority
        i = i + 1
    # add factor of how spaced out the chords are and chord prio calculations (based on soft caps)

    return priority


def find_best_progression(root_name: str,
                          root_acci: str,
                          list_of_figured_basses: list[FigBass]) -> (list[list[list[int]]], list[list[Chord]]):
    """
    takes in a list of fig_bass objects, along with a root_name and root_acci, and outputs the "best" chord progression
    best is deemed through a minimal amount of movement

    deal with doubling rules later
    """
    global ALL_chord_configs
    ALL_chord_configs = []

    for fig in list_of_figured_basses:
        bass_chord = find_bass_chord(root_name, root_acci, fig)
        chord_configs = all_chord_configs(root_name, root_acci, fig, DoubledNote.Root)
        if fig.inversion in ["", "7"]:
            bass_locked_chord_configs = lock_bass(chord_configs, "root", bass_chord)
            print(len(bass_locked_chord_configs))
        elif fig.inversion in ["6", "6/5"]:
            bass_locked_chord_configs = lock_bass(chord_configs, "third", bass_chord)
            print(len(bass_locked_chord_configs))
        elif fig.inversion in ["6/4", "4/3"]:
            bass_locked_chord_configs = lock_bass(chord_configs, "fifth", bass_chord)
            print(len(bass_locked_chord_configs))
        elif fig.inversion == "4/2":
            bass_locked_chord_configs = lock_bass(chord_configs, "seventh", bass_chord)
            print(len(bass_locked_chord_configs))
        else:
            raise Exception("Invalid LUL")

        for each_chord in bass_locked_chord_configs:
            each_chord.update_priority()
        # ^updates the chord priorities for each of the chords that will eventually make up ALL_chord_configs

        ALL_chord_configs.append(bass_locked_chord_configs)
    # creates list of lists (embedded lists are instances of all_chord_configs of each of the figured basses)

    final_list = []

    size_list = []

    for x in range(len(ALL_chord_configs[0])):
        for y in range(len(ALL_chord_configs[1])):

            if is_valid_progression(ALL_chord_configs[0][x], ALL_chord_configs[1][y])[0]:
                size_list.append([x, y])

    sorted_size_list = sorted(size_list, key=full_progression_prio)

    final_list.append(sorted_size_list)
    # ^ sets up the first two chords in their prog_rep

    chord_number_index = 2
    while chord_number_index < len(list_of_figured_basses):
        new_size_list = []
        for prog_rep in final_list[chord_number_index - 2]:
            for x in range(len(ALL_chord_configs[chord_number_index])):
                new_prog_rep = copy.deepcopy(prog_rep) + [x]
                if is_valid_progression(ALL_chord_configs[chord_number_index - 1][new_prog_rep[-2]],
                                        ALL_chord_configs[chord_number_index][new_prog_rep[-1]])[0]:
                    new_size_list.append(new_prog_rep)

        new_sorted_size_list = sorted(new_size_list, key=full_progression_prio)

        final_list.append(new_sorted_size_list)
        chord_number_index = chord_number_index + 1

    print(len(final_list))
    # repeats for all the other figured basses

    for number_of_progs_outputted in range(10):
        prog = final_list[-1][number_of_progs_outputted]
        for x in range(len(prog)):
            print(ALL_chord_configs[x][prog[x]].get_readable_spread())
        print(full_progression_prio(prog))
        print("next")

    # print out the top 10 full chord progs
    return final_list, ALL_chord_configs


if __name__ == '__main__':
    testfig1 = FigBass("I", "")
    testfig2 = FigBass("V/ii", '7')
    testfig3 = FigBass("ii", '')
    testfig4 = FigBass("V", '')
    testfig5 = FigBass("vi", "6/4")

    testlist1 = [testfig1, testfig2]

    progression = find_best_progression("C", "n", testlist1)


# TODO: implementation of secondary doms
# TODO: implementation of doubling rules
# TODO: implementation of open/direct 5ths and 8ths
# TODO: max number of chords used for next generation (maybe use R to check viability of that)
# TODO: filtering final chord list via specific notes (do it before generation to reduce time)
# TODO: try and figure out if the sd thing is the best way of checking spread/ how it affects movement between chords
# TODO: fix 9 warnings

# fixed issubset shenanigans with extra function mark_duplicate
