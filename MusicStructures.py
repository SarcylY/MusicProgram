from enum import Enum


class ChordOrScale(Enum):
    Chord = 0
    Scale = 1


class Note:
    def __init__(self, name: str, accidental: str, pitch: int, dur: float = 1):
        self.name = name
        self.accidental = accidental
        self.pitch = pitch
        self.dur: float = dur

    def __str__(self):
        return self.name + "," + self.accidental + "," + str(self.pitch) + "," + str(self.dur)

    def __repr__(self):
        return self.name + "," + self.accidental + "," + str(self.pitch) + "," + str(self.dur)


class FigBass:
    """
    Declares figured bass notation, using roman numerals and inversion notation (both using strings)
    """

    def __init__(self, numeral: str, inversion: str):
        self.numeral = numeral
        self.inversion = inversion


class Chord:
    """
    Declares class "chord", composed of 4 note objects (SATB) and a "priority" (defaulted to 0), a numerical indication
    of how "good" the chord is (in SATB)
    """

    def __init__(self, bass: Note, tenor: Note, alto: Note, soprano: Note, priority: int = 0):
        self.bass = bass
        self.tenor = tenor
        self.alto = alto
        self.soprano = soprano
        self.priority = priority
