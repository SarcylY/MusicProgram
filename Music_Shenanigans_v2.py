# Takes Pieces, which are lists of note objects, and inputs them into musescore.
# There are a few unimplemented scenarios which are not accounted for and would therefore result in slight errors(see further comments)

import time  # allows various time based functions

import pyautogui as pg  # allows python to access mouse
from pynput.keyboard import Key, Controller  # allows python to access keyboard

from Song_List import Note

keyboard = Controller()


# TODO Fix 3 warnings


def click_dur(note):
    """
clicks on the area of the musescore page which changes the type of note inputted
0.5 = eighth
1 = quarter
2 = half
4 = whole
    :param note: current note object
    """
    if note.dur == 0.5:
        pg.click(x = 420, y = 162)
    if note.dur == 1:
        pg.click(x = 505, y = 162)
    if note.dur == 2:
        pg.click(x = 570, y = 162)
    if note.dur == 4:
        pg.click(x = 645 , y = 162)

def nm(before_note, current_note):
    """
aka note_movement
given note before and current note, give us the name + pitch of note musescore will move to (the important thing is pitch)
note params have to be objects
    :return: musescore_note - the note that musescore will move to (only gives valid .name and .pitch properties)
    """
    global musescore_note
    if before_note.name == current_note.name:
        #if it's the same name, no movement
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
            #movement is Up, figuring out which .pitch it'll end up as
            if 'b' in note_list[before_note_list_number: current_note_list_number]:
                musescore_note = Note(current_note.name, 'filler', before_note.pitch + 1)
            else:
                musescore_note = Note(current_note.name, 'filler', before_note.pitch)
            return musescore_note
        else:
            #movement is Down, see above
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

def first_note_modifier(first_note):
    """
specialized nm function(see above) for the first note, which does not have a "before_note"
first_note is an instance of the note object
once again, will output musescore_note via nm()
    """
    if first_note.name == "c" or "d" or "e":
        before_note = Note(first_note.name, 'filler', 5)
        nm(before_note, first_note)
    else:
        before_note = Note(first_note.name, 'filler', 4)
        nm(before_note, first_note)

def octave_adjusting(octave_difference):
    """
adjusts note by octaves
    :param octave_difference: amount and type of octave adjustment
    0 = no diff
    >0 = adujst up
    <0 = adjust down
    """
    i = 0
    if octave_difference > 0:
        while i < octave_difference:
            with keyboard.pressed(Key.ctrl):
                keyboard.press(Key.up)
            i = i + 1
    if octave_difference < 0:
        while i < -octave_difference:
            with keyboard.pressed(Key.ctrl):
                keyboard.press(Key.down)
            i = i + 1

def acci_adjustment(adjust):
    """
adjusts note based on accidentals
    :param adjust: integer of adujstment
    if pos, adjust up
    if neg, adjust down
    """
    i = 0
    if adjust > 0:
        while i < adjust:
            time.sleep(0.05)
            keyboard.press(Key.up)
            i = i + 1
    elif adjust < 0:
        while i < -adjust:
            time.sleep(0.05)
            keyboard.press(Key.down)
            i = i + 1

def measure_calcs(piece, beats_per_measure):
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
            notes_in_measure = list(range(measure_barrier, i+2))
            measure.append(notes_in_measure)
            measure_barrier = i + 2
        i = i + 1
        if i == len(piece) and dur_tracker > 0:
            notes_in_measure = list(range(measure_barrier, i+1))
            measure.append(notes_in_measure)
    return measure

def run_piece(piece, beats_per_measure):
    """
runs the actual piece
each specific section is commented off and separated by a small time delay
    :param piece: piece which consists of list of note objects
    :param beats_per_measure: see bpm param for measure_calcs()
    """
    i = 0
    while i < len(piece):
        click_dur(piece[i])
        time.sleep(0.05)#above: selects duration of note
        keyboard.press(piece[i].name)
        time.sleep(0.05)#above: enters actual note
        if i == 0:
            first_note_modifier(piece[i])
        else:
            nm(piece[i-1], piece[i])
        octave_misalignment = piece[i].pitch - musescore_note.pitch
        octave_adjusting(octave_misalignment)
        time.sleep(0.05)#above: readjusts notes via octave changing
        measure_calcs(piece, beats_per_measure)
        note_number = i + 1
        measure_number = 0
        while note_number not in measure[measure_number]:
            measure_number = measure_number + 1
        note_in_measure = 0
        while note_number != measure[measure_number][note_in_measure]:
            note_in_measure = note_in_measure + 1
        #calculates exact measure and how far along the note is within the measure for the given current note
        if note_in_measure != 0:
            found_match = False
            while note_in_measure != 0:
                if piece[i].name == piece[measure[measure_number][note_in_measure - 1] - 1].name and piece[i].pitch == piece[measure[measure_number][note_in_measure - 1] - 1].pitch:
                    accidental_list = ['b', 'n', '#']
                    acci_type_before = 0
                    while piece[measure[measure_number][note_in_measure - 1] - 1].acci != accidental_list[acci_type_before]:
                        acci_type_before = acci_type_before + 1
                    acci_type_after = 0
                    while piece[i].acci != accidental_list[acci_type_after]:
                        acci_type_after = acci_type_after + 1
                    acci_change = acci_type_after - acci_type_before
                    acci_adjustment(acci_change)
                    found_match = True
                    note_in_measure = 1
                note_in_measure = note_in_measure - 1
            if found_match == False:
                if piece[i].acci == "#":
                    acci_adjustment(1)
                if piece[i].acci == "b":
                    acci_adjustment(-1)
        else:
            if piece[i].acci == "#":
                acci_adjustment(1)
            if piece[i].acci == "b":
                acci_adjustment(-1)
        time.sleep(0.05)#above: readjusts notes via accidentals
        i = i + 1

