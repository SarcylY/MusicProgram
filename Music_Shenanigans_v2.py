# Takes Pieces, which are lists of note objects, and inputs them into musescore.
# There are a few unimplemented scenarios which are not accounted for
# and would therefore result in slight errors(see further comments)

import time  # allows various time based functions

import pyautogui as pg  # allows python to access mouse
from pynput.keyboard import Key, Controller  # allows python to access keyboard

from MusicStructures import Note

keyboard = Controller()


def click_dur(note: Note) -> None:
    """
clicks on the area of the musescore page which changes the type of note inputted
0.5 = eighth
1 = quarter
2 = half
4 = whole
    :param note: current note object
    """
    if note.dur == 0.5:
        pg.click(x=420, y=162)
    if note.dur == 1:
        pg.click(x=505, y=162)
    if note.dur == 2:
        pg.click(x=570, y=162)
    if note.dur == 4:
        pg.click(x=645, y=162)


def note_movement(before_note: Note, current_note: Note) -> Note:
    """
    given note before and current note, give us the name + pitch of note MuseScore will move to
    (the important thing is pitch)
    :return: MuseScore_note - the note that MuseScore will move to (only gives valid .name and .pitch properties)
    """
    global musescore_note
    if before_note.name == current_note.name:
        # if it's the same name, no movement
        musescore_note = Note(current_note.name, 'filler', before_note.pitch)
        return musescore_note
    else:
        note_list = ['c', 'd', 'e', 'f', 'g', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'a']
        before_note_list_number = 0
        while before_note.name != note_list[before_note_list_number]:
            before_note_list_number = before_note_list_number + 1
        current_note_list_number = before_note_list_number + 1
        while note_list[current_note_list_number] != current_note.name:
            current_note_list_number = current_note_list_number + 1
        # ^figures out if movement is up or down
        if current_note_list_number - before_note_list_number < 4:
            # movement is Up, figuring out which .pitch it'll end up as
            if 'b' in note_list[before_note_list_number: current_note_list_number]:
                musescore_note = Note(current_note.name, 'filler', before_note.pitch + 1)
            else:
                musescore_note = Note(current_note.name, 'filler', before_note.pitch)
            return musescore_note
        else:
            # movement is Down, see above
            revised_current_note_list_number = 0
            while note_list[revised_current_note_list_number] != current_note.name:
                revised_current_note_list_number = revised_current_note_list_number + 1
            revised_before_note_list_number = revised_current_note_list_number + 1
            while before_note.name != note_list[revised_before_note_list_number]:
                revised_before_note_list_number = revised_before_note_list_number + 1
            if 'c' in note_list[revised_current_note_list_number + 1: revised_before_note_list_number + 1]:
                musescore_note = Note(current_note.name, 'filler', before_note.pitch - 1)
            else:
                musescore_note = Note(current_note.name, 'filler', before_note.pitch)
            return musescore_note


def first_note_modifier(first_note: Note) -> Note:
    """
    specialized note_movement function(see above) for the first note, which does not have a "before_note"
    first_note is an instance of the note object
    once again, will output MuseScore_note via nm()
    """
    if first_note.name == "c" or "d" or "e":
        before_note = Note(first_note.name, 'filler', 5)
        return note_movement(before_note, first_note)
    else:
        before_note = Note(first_note.name, 'filler', 4)
        return note_movement(before_note, first_note)


def octave_adjusting(octave_difference: int) -> None:
    """
    adjusts note by octaves
    :param octave_difference: amount and type of octave adjustment
    0 = no diff
    >0 = adjust up
    <0 = adjust down
    """
    if octave_difference > 0:
        for i in range(octave_difference):
            with keyboard.pressed(Key.ctrl):
                keyboard.press(Key.up)
    if octave_difference < 0:
        i = 0
        while i < -octave_difference:
            with keyboard.pressed(Key.ctrl):
                keyboard.press(Key.down)
            i = i + 1


def accidental_adjustment(adjust: int) -> None:
    """
    adjusts note based on accidentals
    :param adjust: integer of adujstment
    if pos, adjust up
    if neg, adjust down
    """
    if adjust > 0:
        for i in range(adjust):
            time.sleep(0.05)
            keyboard.press(Key.up)
    elif adjust < 0:
        i = 0
        while i < -adjust:
            time.sleep(0.05)
            keyboard.press(Key.down)
            i = i + 1


def measure_calcs(piece: list[Note], beats_per_measure: float) -> list[list[int]]:
    """
    outputs measure, a list of lists, with the inner lists representing the measure bars/number
    the numbers will be indicative of the note number (aka i+1)
    :param piece: whole piece, list of note objects
    :param beats_per_measure: number of "beats" in a measure, with a quarter note being 1 beat
    P.S. ties and upbeats are impossible
    """
    i = 0
    dur_tracker = 0
    measure_barrier = 1
    global measure
    measure = []
    while i < len(piece):
        dur_tracker = dur_tracker + piece[i].dur
        if dur_tracker >= beats_per_measure:
            dur_tracker = dur_tracker - beats_per_measure
            notes_in_measure = list(range(measure_barrier, i + 2))
            measure.append(notes_in_measure)
            measure_barrier = i + 2
        i = i + 1
        if i == len(piece) and dur_tracker > 0:
            notes_in_measure = list(range(measure_barrier, i + 1))
            measure.append(notes_in_measure)
    return measure


def run_piece(piece: list[Note], beats_per_measure: float) -> None:
    """
    runs the actual piece
    each specific section is commented off and separated by a small time delay
    :param piece: piece which consists of list of note objects
    :param beats_per_measure: see bpm param for measure_calcs()
    """
    i = 0
    while i < len(piece):
        click_dur(piece[i])
        time.sleep(0.05)  # above: selects duration of note
        keyboard.press(piece[i].name)
        time.sleep(0.05)  # above: enters actual note
        if i == 0:
            first_note_modifier(piece[i])
        else:
            note_movement(piece[i - 1], piece[i])
        octave_misalignment = piece[i].pitch - musescore_note.pitch
        octave_adjusting(octave_misalignment)
        time.sleep(0.05)  # above: readjusts notes via octave changing
        measure_calcs(piece, beats_per_measure)
        note_number = i + 1
        measure_number = 0
        while note_number not in measure[measure_number]:
            measure_number = measure_number + 1
        note_in_measure = 0
        while note_number != measure[measure_number][note_in_measure]:
            note_in_measure = note_in_measure + 1
        # calculates exact measure and how far along the note is within the measure for the given current note
        if note_in_measure != 0:
            found_match = False
            while note_in_measure != 0:
                if piece[i].name == piece[measure[measure_number][note_in_measure - 1] - 1].name and piece[i].pitch == \
                        piece[measure[measure_number][note_in_measure - 1] - 1].pitch:
                    accidental_list = ['b', 'n', '#']
                    acci_type_before = 0
                    while piece[measure[measure_number][note_in_measure - 1] - 1].accidental != accidental_list[
                        acci_type_before]:
                        acci_type_before = acci_type_before + 1
                    acci_type_after = 0
                    while piece[i].accidental != accidental_list[acci_type_after]:
                        acci_type_after = acci_type_after + 1
                    acci_change = acci_type_after - acci_type_before
                    accidental_adjustment(acci_change)
                    found_match = True
                    note_in_measure = 1
                note_in_measure = note_in_measure - 1
            if not found_match:
                if piece[i].accidental == "#":
                    accidental_adjustment(1)
                if piece[i].accidental == "b":
                    accidental_adjustment(-1)
        else:
            if piece[i].accidental == "#":
                accidental_adjustment(1)
            if piece[i].accidental == "b":
                accidental_adjustment(-1)
        time.sleep(0.05)  # above: readjusts notes via accidentals
        i = i + 1
