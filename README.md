# pianoStringCalculator
The purpose of this is to figure out what gague strings one should use on a piano when replacing all the piano strings.

This is basically an implementation of the Mersenne-Taylor formula.

“The frequency equals 1 divided by twice the length all multiplied by the square root of the tension divided by the mass per unit length”.

The relationships:

- for a string under constant tension, frequency varies inversely as the length
- for a string of constant length, frequency is proportional to the square root of the tension
- for given length and constant tension, frequency varies inversely as the square root of the mass/unit length

We would like to calculate ideal, as well as, practical string guage for each string given:
- The frquency which produces the correct note of the string(s)
- The mass of the string material
- The length of the string (fixed)
- The ideal range of tension. Assuming 160 - 220 lbs ... I only have rough understanding of this.

We distinguish ideal and practical string guage as follows:
- ideal: the guage if we could manuafacture any diameter of string easily.
- practical: the AWG guages redily available for purchase. 12-21, in 1/2 guage increments.

We would like to optimize for the following:
- least variance of tension across the strings
    - NOTE: I am assuming pianos were designed to expect consistent force across breadth of the harp.
- possibly the highest reasonable tension.
    - According to https://en.wikipedia.org/wiki/Piano_acoustics#Inharmonicity_and_piano_size, the bending
      force of the string material acts as a force which increases the frequency of the harmonics produced.
      One of the strategies for dealing with this is, "... increasing the tension force so that it stays 
      much bigger than the bending force."
