class Note:
    def __init__(self, name, acci, pitch, dur: float = 1):
        self.name = name
        self.acci = acci
        self.pitch = pitch
        self.dur: float = dur

    def __str__(self):
        return self.name + "," + self.acci + "," + str(self.pitch) + "," + str(self.dur)

    def __repr__(self):
        return self.name + "," + self.acci + "," + str(self.pitch) + "," + str(self.dur)


class FigBass:
    """
    Declares figured bass notation, using roman numerals and inversion notation (both using strings)
    """

    def __init__(self, numeral, inversion):
        self.numeral = numeral
        self.inver = inversion


class Chord:
    """
    Declares class "chord", composed of 4 note objects (SATB) and a "priority" (defaulted to 0), a numerical indication
    of how "good" the chord is (in SATB)
    """

    def __init__(self, bass, tenor, alto, soprano, priority=0):
        self.bass = bass
        self.tenor = tenor
        self.alto = alto
        self.soprano = soprano
        self.prio = priority
