#! /usr/bin/env python3

""" Gothic converter

The transliteration scheme is as follows

    -----------------------------------------------------------------------
    | a     𐌰 | b     𐌱 | g     𐌲 | d     𐌳 | e     𐌴 | q     𐌵 | z     𐌶 |
    | h     𐌷 | th    𐌸 | i     𐌹 | k     𐌺 | l     𐌻 | m     𐌼 | n     𐌽 |
    | j     𐌾 | u     𐌿 | p     𐍀 | q'    𐍁 | r     𐍂 | s     𐍃 | t     𐍄 |
    | w     𐍅 | f     𐍆 | x     𐍇 | hw    𐍈 | o     𐍉 | z'    𐍊 |         |
    -----------------------------------------------------------------------

"""

def alpha_to_gothic(input):
    """ 
    Parameters
    ----------
    input : str
        Text input with syllables separated by dashes and words by spaces.

    Returns
    -------
    output : str
        Transliterated text in Gothic Script
    """
    # print(input.translate(script))

    output = input
    output = output.replace("th", "𐌸")
    output = output.replace("q'", "𐍁")
    output = output.replace("z'", "𐍊")
    output = output.replace("hw", "𐍈")
    output = output.replace("a", "𐌰")
    output = output.replace("b", "𐌱")
    output = output.replace("g", "𐌲")
    output = output.replace("d", "𐌳")
    output = output.replace("e", "𐌴")
    output = output.replace("q", "𐌵")
    output = output.replace("z", "𐌶")
    output = output.replace("h", "𐌷")
    output = output.replace("i", "𐌹")
    output = output.replace("k", "𐌺")
    output = output.replace("l", "𐌻")
    output = output.replace("m", "𐌼")
    output = output.replace("n", "𐌽")
    output = output.replace("j", "𐌾")
    output = output.replace("u", "𐌿")
    output = output.replace("p", "𐍀")
    output = output.replace("r", "𐍂")
    output = output.replace("s", "𐍃")
    output = output.replace("t", "𐍄")
    output = output.replace("w", "𐍅")
    output = output.replace("f", "𐍆")
    output = output.replace("x", "𐍇")
    output = output.replace("o", "𐍉")
    

    return output


if __name__ == "__main__":
       a = """
       wulfila
       """
       b = alpha_to_gothic(a)
       print(b)
