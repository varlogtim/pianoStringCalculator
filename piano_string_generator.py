#!/usr/bin/env python3
import argparse
import math

from collections import namedtuple

# Formulas:
# - Volume of cylinder: pi * r^2 * h
#
#
# Mersenne-Taylor formula
#
# https://en.wikipedia.org/wiki/Mersenne%27s_laws#Equations
# http://pianomaker.co.uk/technical/string_formulae/
#
# “The frequency equals 1 divided by twice the length all multiplied by the square root of the tension divided by the mass per unit length”
# 
# - freq = (1 / (2 * length)) * sqrt(tension / mass)
#   - length expressed in 
#   - tension expressed in dynes. One dyne is 980.62 gram force.
#       - 1 lbf = 444,822.168 dyn (even though the article specifies something different.
#   
# - mass = (pi * d ^ 2 * r) / 4
#   - mass measured in grams
#   - pi :eyes:
#   - d is the diameter of the string in centimeters
#   - r (rho) is relative density in grams per cubic centimeter.
#
# So, we need to combine the mass and freq formulas.
# ... :sqwinting_face:
# 


#
# OK, I am just taking the pianomaker website at their word about this following formulas.
# XXX TODO: Seriously, spend the time to algebra this out on paper so that you understand.
#
# t = (fld)**2/K
# d = sqrt(Kt)/fl
#
LBF_DYNES = 444_822.168
# K is a constant defined by dividing our conversation factor (pounds force to dynes, 444,822.168) by pi * r
#


#
# XXX NOTE: Ideal piano string tension is 160 - 200 flbs.



#######################################################################

#
# Defining Frequency and Note list of 88 key Piano.
#

# - Assuming equal tempermant.
# - There are twelve semitone in an octave.
# - The frequency of a note an octave higher is double.
# - The frequence of a note an octave lower is half.
# - The number you multiple by itself 12 times in order to reach twice the frequency is the twelveth root of 2
# - The number you multiple by itself 12 times in order to reach half the frequency is the twelveth root of one half.
# - The Nth relative semitone is equal to the product of N 12th roots of 2.
# - Nth root of X is equivalent to X to the 1 over N
# Therefore:
# - To move a semi tone up, we use this:
SEMITONE_UP = lambda freq : freq * 2 ** (1/12)
# - To move a semi tone down, we use this:
SEMITONE_DOWN = lambda freq : freq * (1/2) ** (1/12)   # XXX this could also be: freq * 2 ** (-1/12). I don't quite understand these negative powers... Think on it.
# - To move an arbitrary number of semitones up or down from a starting frequency, we use this:
SEMITONE_OFFSET = lambda freq, offset : freq * 2 ** (offset / 12)

A4_FREQUENCY = 440  # CPS or hertz
NOTES_IN_OCTAVE = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
NOTE_FREQ_OF_PIANO = {
    **{f"{note}0": None for note in ["A", "A#", "B"]},
    **{f"{note}{octave}": None for octave in range(1, 8) for note in NOTES_IN_OCTAVE},
    **{"C8": None}
}  # {A0, A#0, B0, C1, ... A7, A#7, B7, C8}, All frequencies are initialized to None

NOTE_OFFSET_OF_PIANO = [note for note in NOTE_FREQ_OF_PIANO.keys()]
# XXX I probably could combine this with the dict comprehension above
A4_idx = list(NOTE_FREQ_OF_PIANO.keys()).index("A4")
for idx, note in enumerate(NOTE_FREQ_OF_PIANO.keys()):
    NOTE_FREQ_OF_PIANO[note] = SEMITONE_OFFSET(A4_FREQUENCY, idx - A4_idx)



#
# Roslau Steel Wire for Piano Strings
#
# https://www.roeslau-draht.com/fileadmin/user_upload/PDF/Datenblaetter/EN/Overview_of_important_parameters.pdf
#
#
WireSpec = namedtuple("WireSpec", ["size", "diameter_mm", "weight_kg_km"])

ROSLAU_WIRES = [
    WireSpec(size=12,   diameter_mm=0.725, weight_kg_km=3.24),
    WireSpec(size=12.5, diameter_mm=0.750, weight_kg_km=3.46),
    WireSpec(size=13,   diameter_mm=0.775, weight_kg_km=3.70),
    WireSpec(size=13.5, diameter_mm=0.800, weight_kg_km=3.94),
    WireSpec(size=14,   diameter_mm=0.825, weight_kg_km=4.19),
    WireSpec(size=14.5, diameter_mm=0.850, weight_kg_km=4.45),
    WireSpec(size=15,   diameter_mm=0.875, weight_kg_km=4.72),
    WireSpec(size=15.5, diameter_mm=0.900, weight_kg_km=4.99),
    WireSpec(size=16,   diameter_mm=0.925, weight_kg_km=5.27),
    WireSpec(size=16.5, diameter_mm=0.950, weight_kg_km=5.56),
    WireSpec(size=17,   diameter_mm=0.975, weight_kg_km=5.86),
    WireSpec(size=17.5, diameter_mm=1.000, weight_kg_km=6.16),
    WireSpec(size=18,   diameter_mm=1.025, weight_kg_km=6.47),
    WireSpec(size=18.5, diameter_mm=1.050, weight_kg_km=6.79),
    WireSpec(size=19,   diameter_mm=1.075, weight_kg_km=7.12),
    WireSpec(size=19.5, diameter_mm=1.100, weight_kg_km=7.45),
    WireSpec(size=20,   diameter_mm=1.125, weight_kg_km=7.80),
    WireSpec(size=20.5, diameter_mm=1.150, weight_kg_km=8.15),
    WireSpec(size=21,   diameter_mm=1.175, weight_kg_km=8.50),
    WireSpec(size=21.5, diameter_mm=1.200, weight_kg_km=8.87),
    WireSpec(size=22,   diameter_mm=1.225, weight_kg_km=9.25),
]
ROSLAU_RELATIVE_DENSITY = 7.84  # grams per cubic cm
IDEAL_TENSION = 180  # foot pounds

PianoHarpString = namedtuple("PianoString", ["speaking_length_cm", "note"])

START_OF_PLAIN_STRINGS = 26
PIANO_HARP_STRINGS = [
    *[None for _ in range(START_OF_PLAIN_STRINGS)],  # these are the covered strings.
    PianoHarpString(speaking_length_cm=113.9825, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS]),
    PianoHarpString(speaking_length_cm=112.0775, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 1]),
    PianoHarpString(speaking_length_cm=109.5375, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 2]),
    PianoHarpString(speaking_length_cm=106.6800, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 3]),
    PianoHarpString(speaking_length_cm=103.5050, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 4]),
    PianoHarpString(speaking_length_cm=99.3775, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 5]),
    PianoHarpString(speaking_length_cm=95.8850, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 6]),
    PianoHarpString(speaking_length_cm=91.7575, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 7]),
    PianoHarpString(speaking_length_cm=87.3125, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 8]),
    PianoHarpString(speaking_length_cm=82.8675, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 9]),
    PianoHarpString(speaking_length_cm=78.1050, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 10]),
    PianoHarpString(speaking_length_cm=73.3425, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 11]),
    PianoHarpString(speaking_length_cm=69.2150, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 12]),
    PianoHarpString(speaking_length_cm=65.4050, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 13]),
    PianoHarpString(speaking_length_cm=62.2300, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 14]),
    PianoHarpString(speaking_length_cm=59.0550, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 15]),
    PianoHarpString(speaking_length_cm=56.1975, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 16]),
    PianoHarpString(speaking_length_cm=53.0225, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 17]),
    PianoHarpString(speaking_length_cm=50.4825, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 18]),
    PianoHarpString(speaking_length_cm=47.9425, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 19]),
    PianoHarpString(speaking_length_cm=45.4025, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 20]),
    PianoHarpString(speaking_length_cm=43.1800, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 21]),
    PianoHarpString(speaking_length_cm=40.9575, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 22]),
    PianoHarpString(speaking_length_cm=39.0525, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 23]),
    PianoHarpString(speaking_length_cm=37.1475, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 24]),
    PianoHarpString(speaking_length_cm=35.5600, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 25]),
    PianoHarpString(speaking_length_cm=34.2900, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 26]),
    PianoHarpString(speaking_length_cm=33.6550, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 27]),
    PianoHarpString(speaking_length_cm=32.3850, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 28]),
    PianoHarpString(speaking_length_cm=30.7975, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 29]),
    PianoHarpString(speaking_length_cm=29.2100, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 30]),
    PianoHarpString(speaking_length_cm=27.6225, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 31]),
    PianoHarpString(speaking_length_cm=26.0350, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 32]),
    PianoHarpString(speaking_length_cm=24.4475, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 33]),
    PianoHarpString(speaking_length_cm=22.8600, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 34]),
    PianoHarpString(speaking_length_cm=21.5900, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 35]),
    PianoHarpString(speaking_length_cm=20.3200, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 36]),
    PianoHarpString(speaking_length_cm=18.7325, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 37]),
    PianoHarpString(speaking_length_cm=17.7800, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 38]),
    PianoHarpString(speaking_length_cm=16.8275, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 39]),
    PianoHarpString(speaking_length_cm=15.7162, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 40]),
    PianoHarpString(speaking_length_cm=14.9225, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 41]),
    PianoHarpString(speaking_length_cm=14.2875, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 42]),
    PianoHarpString(speaking_length_cm=13.6525, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 43]),
    PianoHarpString(speaking_length_cm=13.0175, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 44]),
    PianoHarpString(speaking_length_cm=11.4300, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 45]),
    PianoHarpString(speaking_length_cm=10.9537, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 46]),
    PianoHarpString(speaking_length_cm=10.6362, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 47]),
    PianoHarpString(speaking_length_cm=10.1600, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 48]),
    PianoHarpString(speaking_length_cm=9.8425, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 49]),
    PianoHarpString(speaking_length_cm=9.2075, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 50]),
    PianoHarpString(speaking_length_cm=8.8900, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 51]),
    PianoHarpString(speaking_length_cm=8.4137, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 52]),
    PianoHarpString(speaking_length_cm=8.0962, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 53]),
    PianoHarpString(speaking_length_cm=7.6200, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 54]),
    PianoHarpString(speaking_length_cm=7.3025, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 55]),
    PianoHarpString(speaking_length_cm=6.9850, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 56]),
    PianoHarpString(speaking_length_cm=6.6675, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 57]),
    PianoHarpString(speaking_length_cm=6.3500, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 58]),
    PianoHarpString(speaking_length_cm=6.0325, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 59]),
    PianoHarpString(speaking_length_cm=5.7150, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 60]),
    PianoHarpString(speaking_length_cm=5.3975, note=NOTE_OFFSET_OF_PIANO[START_OF_PLAIN_STRINGS + 61]),
]


def find_conversion_factor(relative_density_g_cm3):
    return LBF_DYNES / (relative_density_g_cm3 * math.pi)

def find_ideal_diameter_cm(string: PianoHarpString):
    k = LBF_DYNES / (ROSLAU_RELATIVE_DENSITY * math.pi)
    d = math.sqrt(k * IDEAL_TENSION) / (NOTE_FREQ_OF_PIANO[string.note] * string.speaking_length_cm)
    return d

# Finding relative density of Rosleau steal piano wire.
def find_relative_density(string: WireSpec):  # yields r (rho)
    weight_g_cm = string.weight_kg_km / 100  # 100,000 (cm in km) over 1000 (g in kg)
    radius_cm = (string.diameter_mm / 10) / 2
    volume_cm3 = math.pi * radius_cm ** 2  # one cm long
    relative_density_g_cm3 = weight_g_cm / volume_cm3
    # print(f"size: {string.size}, volume_cm3: {volume_cm3}, weight_g_cm: {weight_g_cm}, relative_density_g_cm3: {relative_density_g_cm3}, K={find_conversion_factor(relative_density_g_cm3)}")
    # The average is 7.84 +-0.005 grams per cubic centimeter... so.
    return relative_density_g_cm3


# OK, need to define all put all the strings



def main() -> None:
    for idx, (note, freq) in enumerate(NOTE_FREQ_OF_PIANO.items()):
        print(f"{idx}: {note}: {freq:.2f}")
    # print(f"UP: {SEMITONE_UP(440)}")
    # print(f"DOWN: {SEMITONE_DOWN(440)}")

if __name__ == "__main__":
    main()
    for wire in ROSLAU_WIRES:
        find_relative_density(wire)
    for string in PIANO_HARP_STRINGS:
        print(f"{string}: {find_ideal_diameter_cm(string)}")
