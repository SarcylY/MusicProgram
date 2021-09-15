from __future__ import annotations

import statistics as stats
#enables sd
from enum import Enum
from typing import Union


class MovementDirection(Enum):
    Down = -1
    Constant = 0
    Up = 1


class DoubledNote(Enum):
    Root = 1
    Third = 3
    Fifth = 5


class ChordOrScale(Enum):
    Chord = 0
    Scale = 1


class Accidental(Enum):
    DoubleSharp = "x"
    Sharp = "#"
    Natural = "n"
    Flat = "b"
    DoubleFlat = "bb"


class Note:
    def __init__(self, name: str, accidental: Accidental, pitch: int, dur: float = 1):
        self.name = name
        self.accidental = accidental
        self.pitch = pitch
        self.dur: float = dur

    def __str__(self):
        return self.name + "," + str(self.accidental.value) + "," + str(self.pitch) + "," + str(self.dur)

    def __repr__(self):
        return self.name + "," + str(self.accidental.value) + "," + str(self.pitch) + "," + str(self.dur)

    def __copy__(self):
        return self.copy()

    def fix_blank_accidental(self) -> None:
        if self.accidental.value == '':
            self.accidental = Accidental.Natural

    def get_readable_version(self) -> str:
        return self.name + str(self.accidental.value) + str(self.pitch)

    def copy(self) -> Note:
        return Note(self.name, self.accidental.value, self.pitch, self.dur)

    @classmethod
    def note_from_string(cls, string: str) -> Note:
        result = Note(string[0],
                      Accidental.Natural if string[1:-1] == "" and string[-1].isdigit()
                      else Accidental.Natural if string[1:] == "" and not string[-1].isdigit()
                      else Accidental(string[1:-1]) if string[-1].isdigit()
                      else Accidental(string[1:]),
                      int(string[-1]) if string[-1].isdigit() else 100)
        return result


def precise_interval_calc(lower_note: Note, upper_note: Note) -> str:
    """
    given lower and upper note object, returns the true interval as string (includes extensions above an octave)
    (does produce a diminished 1 interval if the notes are not ordered properly)
    """
    root_list = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    lower_number = root_list.index(lower_note.name)
    upper_number = root_list.index(upper_note.name)
    bass_interval = (upper_number - lower_number) + 1
    octave_diff = upper_note.pitch - lower_note.pitch
    bass_interval = bass_interval + (octave_diff * 7)
    # ^calculates the bass interval

    full_list = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B',
                 'C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
    lower_number_in_full = full_list.index(lower_note.name)
    if lower_note.accidental == Accidental.DoubleFlat:
        true_lower_number = lower_number_in_full - 2
    elif lower_note.accidental == Accidental.Flat:
        true_lower_number = lower_number_in_full - 1
    elif lower_note.accidental == Accidental.Natural:
        true_lower_number = lower_number_in_full
    elif lower_note.accidental == Accidental.Sharp:
        true_lower_number = lower_number_in_full + 1
    elif lower_note.accidental == Accidental.DoubleSharp:
        true_lower_number = lower_number_in_full + 2
    else:
        raise Exception("Invalid accidental")
    # ^finds the true lower number value based on name and accidental (can go all the way down to -2)

    if true_lower_number in [-1, -2]:
        upper_number_in_full = full_list.index(upper_note.name)
    else:
        updated_full_list = full_list[true_lower_number:]
        upper_number_in_full = updated_full_list.index(upper_note.name)
    # ^modifies the full_list based on the true lower number

    if upper_note.accidental == Accidental.DoubleFlat:
        true_upper_number = upper_number_in_full - 2
    elif upper_note.accidental == Accidental.Flat:
        true_upper_number = upper_number_in_full - 1
    elif upper_note.accidental == Accidental.Natural:
        true_upper_number = upper_number_in_full
    elif upper_note.accidental == Accidental.Sharp:
        true_upper_number = upper_number_in_full + 1
    elif upper_note.accidental == Accidental.DoubleSharp:
        true_upper_number = upper_number_in_full + 2
    else:
        raise Exception("Invalid accidental")
    if true_lower_number in [-1, -2]:
        true_diff = true_upper_number - true_lower_number
    else:
        true_diff = true_upper_number % 12
    # ^calculates the actual difference between lower and upper note (in units of semitones)

    if bass_interval % 7 == 1:
        expected_diff = 0
    elif bass_interval % 7 == 2:
        expected_diff = 2
    elif bass_interval % 7 == 3:
        expected_diff = 4
    elif bass_interval % 7 == 4:
        expected_diff = 5
    elif bass_interval % 7 == 5:
        expected_diff = 7
    elif bass_interval % 7 == 6:
        expected_diff = 9
    elif bass_interval % 7 == 0:
        expected_diff = 11
    else:
        raise Exception("Should never reach this point - check precise_interval_calc")
    # ^sets the expected semitone difference for the major/perfect versions of the intervals
    
    if true_diff - expected_diff == -2:
        quality = "d"
    elif true_diff - expected_diff == -1:
        if bass_interval in [1, 4, 5]:
            quality = "d"
        else:
            quality = "m"
    elif true_diff - expected_diff == 0:
        if bass_interval in [1, 4, 5]:
            quality = "P"
        else:
            quality = "M"
    elif true_diff - expected_diff == 1:
        quality = "a"
    else:
        raise Exception("Should never reach this point - can't find quality in precise_interval_calc")
    # ^based on the differences of the true and expected semitone differences, gives the bass interval a quality

    true_interval = quality + str(bass_interval)
    return true_interval


def note_movement(first_note: Note, second_note: Note) -> MovementDirection:
    """
    returns movement direction ("Up", "Down", or "None")
    """
    if first_note.name == second_note.name and \
            first_note.accidental == second_note.accidental and \
            first_note.pitch == second_note.pitch:
        # if it's the same name, no movement
        return MovementDirection.Constant
    if second_note.pitch > first_note.pitch:
        return MovementDirection.Up
    if first_note.pitch > second_note.pitch:
        return MovementDirection.Down
    full_list = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
    first_note_number = full_list.index(first_note.name)
    second_note_number = full_list.index(second_note.name)
    if second_note_number > first_note_number:
        return MovementDirection.Up
    if first_note_number > second_note_number:
        return MovementDirection.Down
    if first_note.accidental == Accidental.DoubleFlat:
        first_acci = -2
    elif first_note.accidental == Accidental.Flat:
        first_acci = -1
    elif first_note.accidental == Accidental.Sharp:
        first_acci = 1
    elif first_note.accidental == Accidental.DoubleSharp:
        first_acci = 2
    else:
        first_acci = 0
    if second_note.accidental == Accidental.DoubleFlat:
        second_acci = -2
    elif second_note.accidental == Accidental.Flat:
        second_acci = -1
    elif second_note.accidental == Accidental.Sharp:
        second_acci = 1
    elif second_note.accidental == Accidental.DoubleSharp:
        second_acci = 2
    else:
        second_acci = 0
    if second_acci > first_acci:
        return MovementDirection.Up
    if first_acci > second_acci:
        return MovementDirection.Down
    return MovementDirection.Constant


def get_bass_interval(lower_note: Note, upper_note: Note) -> int:
    """
    given a lower and upper note object, returns the bass interval (not including the quality)
    """
    return int(precise_interval_calc(lower_note, upper_note)[1:])


class FigBass:
    """
    Declares figured bass notation, using roman numerals and inversion notation (both using strings)
    """

    def __init__(self, numeral: str, inversion: str):
        self.numeral = numeral
        self.inversion = inversion

    def __copy__(self) -> FigBass:
        return FigBass(self.numeral, self.inversion)

    def copy(self) -> FigBass:
        return self.__copy__()


class Chord:
    """
    Declares class "chord", composed of 4 note objects (SATB) and a "priority" (defaulted to 0), a numerical indication
    of how "good" the chord is (in SATB)
    """

    def __init__(self, bass: Note, tenor: Note, alto: Union[Note, None], soprano: Union[Note, None], priority: int = 0):
        self.bass = bass
        self.tenor = tenor
        self.alto = alto
        self.soprano = soprano
        self.priority = priority

    def __copy__(self) -> Chord:
        return Chord(self.bass.copy(), self.tenor.copy(),
                     self.alto.copy() if self.alto is not None else None,
                     self.soprano.copy() if self.soprano is not None else None,
                     self.priority)

    def copy(self):
        return self.__copy__()

    def update_priority(self) -> None:
        """
        increases the priority count of the given chord based on the soft caps for the ranges in the bass and soprano
        also now includes calculation of how evenly spread the notes are in the chord, the more even they are, the
        better the chord (adds a simple sd of all the intervals)
        Returns the same chord, now with their .priority updated
        The lower the priority, the better the chord (the more soft caps it violates)
        """
        self.priority = 0

        bass_lower_bound = Note("F", Accidental.Natural, 3)
        bass_upper_bound = Note('C', Accidental.Natural, 4)
        lower_result = note_movement(bass_lower_bound, self.bass)
        upper_result = note_movement(bass_upper_bound, self.bass)
        if lower_result == MovementDirection.Down:
            self.priority += 1
        if upper_result == MovementDirection.Up:
            self.priority += 1
        # ^lowers priority based on soft caps in the bass

        soprano_lower_bound = Note("C", Accidental.Natural, 4)
        soprano_upper_bound = Note('G', Accidental.Natural, 5)
        lower_result = note_movement(soprano_lower_bound, self.soprano)
        upper_result = note_movement(soprano_upper_bound, self.soprano)
        if lower_result == MovementDirection.Down:
            self.priority += 1
        if upper_result == MovementDirection.Up:
            self.priority += 1
        # ^lowers priority based on soft caps in the soprano

        interval_list = [get_bass_interval(self.bass, self.tenor),
                         get_bass_interval(self.tenor, self.alto),
                         get_bass_interval(self.alto, self.soprano)]
        self.priority = self.priority + round(stats.stdev(interval_list), 3)
        # ^increases priority based on how good/bad the notes in the chord are spread out

    def get_readable_spread(self) -> list[str]:
        """
        Returns a list which is a readable version of the chord
        [bass, tenor, alto, soprano] (plus chord prio just in case)
        """
        return [self.bass.get_readable_version(),
                self.tenor.get_readable_version(),
                self.alto.get_readable_version(),
                self.soprano.get_readable_version(),
                str(self.priority)]
