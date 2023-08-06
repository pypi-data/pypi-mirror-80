#!/usr/bin/env python3

""" Greek script converter

This scripts allows the user to convert between the latinized transliteration
of Greek and the Armenian Script itself with (almost) simple rules.

Usage
-----
pieoffice greek <text>

The transliteration scheme follows the TLG Betacode Manual, using the
implementation of Matias Grioni's betacode module.
This script only implements the terminal based application and a couple more
letters:

    s4    Ϡ
    *s4     ϡ
    s5       ϻ
    *s5       Ϻ
"""

from betacode.conv import beta_to_uni

def alpha_to_greek(input):
    """ Converts text in Latin Alphabet to Greek Script

    Each syllable should be separated by a sing dash, each word by a space.

    Parameters
    ----------
    input : str
        Text input with syllables separated by dashes and words by spaces.

    Returns
    -------
    output : str
        Transliterated text in Greek Script

    Usage
    -----
    
    > alpha_to_greek("<++>")
    + 

    """
    # print(input.translate(script))

    output = beta_to_uni(input)

    output = output.replace("σ4", "Ϡ")
    output = output.replace("Σ4", "ϡ")
    output = output.replace("σ5", "ϻ")
    output = output.replace("Σ5", "Ϻ")

    return output


if __name__ == "__main__":
       a = """
       a)/s5 *s4
       """
       b = alpha_to_greek(a)
       print(b)
