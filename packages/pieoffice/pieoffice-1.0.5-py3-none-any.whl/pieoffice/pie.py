#! /usr/bin/env python3

""" PIE converter

The transliteration scheme is close to the Harvard-Kyoto for Sanskrit:

      -----------------------------------------------
      | A	ā   |   I	 ī   |  U	ū   |
      | R	r̥   |   RR	 r̥̄   |  lR	l̥   |
      | lRR     l̥̄   |   A/	 ā́   |  I/	ī́   |
      | U/	ū́   |   R/       ŕ̥   |  RR/     r̥̄́   |
      | lR/     ĺ̥   |   lRR/     l̥̄́   |  c	k̑   |
      | cw	k̑ʷ  |   kw	 kʷ  |  j	ĝ   |
      | jw	gʷ  |   bh	 bʰ  |  dh	dʰ  |
      | jh	ĝʰ  |   gh	 gʰ  |  gw	gʷ  |
      | gwh     gʷʰ |   h1	 h₁  |  h2	h₂  |
      | h3	h₃  |   y	 i̯   |  w	u̯   |
      | E	ē   |   O	 ō   |  E/	ḗ   |
      | É	ḗ   |   O/	 ṓ   |  Ó	ṓ   |
      | M	m̥   |   N	 n̥   |              |
      -----------------------------------------------

"""

def alpha_to_pie(input):
    """ 
    Parameters
    ----------
    input : str
        Text input with syllables separated by dashes and words by spaces.

    Returns
    -------
    output : str
        Transliterated text in Avestan Script
    """
    # print(input.translate(script))

    output = input
    output = output.replace("A/", "ā́")
    output = output.replace("A", "ā")
    output = output.replace("I/", "ī́")
    output = output.replace("I", "ī")
    output = output.replace("U/", "ū́")
    output = output.replace("U", "ū")
    output = output.replace("lRR/", "l̥̄́")
    output = output.replace("lRR", "l̥̄")
    output = output.replace("lR/", "ĺ̥")
    output = output.replace("lR", "l̥")
    output = output.replace("RR/", "r̥̄́")
    output = output.replace("RR", "r̥̄")
    output = output.replace("R/", "ŕ̥")
    output = output.replace("R", "r̥")
    output = output.replace("cw", "k̑ʷ")
    output = output.replace("c", "k̑")
    output = output.replace("kw", "kʷ")
    output = output.replace("jw", "ĝʷ")
    output = output.replace("j", "ĝ")
    output = output.replace("bh", "bʰ")
    output = output.replace("dh", "dʰ")
    output = output.replace("jh", "ĝʰ")
    output = output.replace("gwh", "gʷʰ")
    output = output.replace("gh", "gʰ")
    output = output.replace("gw", "gʷ")
    output = output.replace("h1", "h₁")
    output = output.replace("h2", "h₂")
    output = output.replace("h3", "h₃")
    output = output.replace("y", "i̯")
    output = output.replace("w", "u̯")
    output = output.replace("E/", "ḗ")
    output = output.replace("O", "ō")
    output = output.replace("É", "ḗ")
    output = output.replace("O/", "ṓ")
    output = output.replace("E", "ē")
    output = output.replace("Ó", "ṓ")
    output = output.replace("M", "m̥")
    output = output.replace("N", "n̥")
    return output


if __name__ == "__main__":
       a = """
       wókw-M
       """
       b = alpha_to_pie(a)
       print(b)
