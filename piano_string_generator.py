#!/usr/bin/env python3
import argparse

A4_FREQUENCY = 440  # CPS or hertz
NOTES_IN_OCTAVE = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
NOTE_FREQ_OF_PIANO = {
    **{f"{note}0": None for note in ["A", "A#", "B"]},
    **{f"{note}{octave}": None for octave in range(1, 8) for note in NOTES_IN_OCTAVE},
    **{"C8": None}
}  # {A0, A#0, B0, C1, ... A7, A#7, B7, C8}, All frequencies are initialized to None

# - Assuming equal tempermant.
# - There are twelve semitone in an octave.
# - The frequency of a note an octave higher is double.
# - The frequence of a note an octave lower is half.
# - The number you multiple by itself 12 times in order to reach twice the frequency is the twelveth root of 2
# - The number you multiple by itself 12 times in order to reach half the frequency is the twelveth root of one half.
# - Nth root of X is equivalent to X to the 1 over N
# Therefore:
# - To move a semi tone up, we use this:
SEMITONE_UP = lambda freq : freq * 2 ** (1/12)
# - To move a semi tone down, we use this:
SEMITONE_DOWN = lambda freq : freq * (1/2) ** (1/12)
# - To move an arbitrary number of semitones up or down from a starting frequency, we use this:
SEMITONE_OFFSET = lambda freq, offset : freq * 2 ** (offset / 12)


A4_idx = list(NOTE_FREQ_OF_PIANO.keys()).index("A4")

for idx, note in enumerate(NOTE_FREQ_OF_PIANO.keys()):
    NOTE_FREQ_OF_PIANO[note] = SEMITONE_OFFSET(A4_FREQUENCY, idx - A4_idx)


def main() -> None:
    for note, freq in NOTE_FREQ_OF_PIANO.items():
        print(f"{note}: {freq:.2f}")
    print(f"UP: {SEMITONE_UP(440)}")
    print(f"DOWN: {SEMITONE_DOWN(440)}")

if __name__ == "__main__":
    main()
