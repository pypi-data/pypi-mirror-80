#! /usr/bin/env python3

""" Lydian converter

The transliteration scheme is as follows

    -----------------------------------------------------------------------
    | a     𐤠 | b,p   𐤡 | g     𐤢 | d     𐤣 | e     𐤤 | v,w   𐤥 | i     𐤦 |
    | y     𐤧 | k     𐤨 | l     𐤩 | m     𐤪 | n     𐤫 | o     𐤬 | r     𐤭 |
    | S,ś   𐤮 | t     𐤯 | u     𐤰 | f     𐤱 | q     𐤲 | s,sh  𐤳 | T     𐤴 |
    | ã     𐤵 | A     𐤵 | ẽ     𐤶 | E     𐤶 | L     𐤷 | N     𐤸 | c     𐤹 |
    | .      |         |         |         |         |         |         |
    -----------------------------------------------------------------------

"""

def alpha_to_lydian(input):
    """ 
    Parameters
    ----------
    input : str
        Text input with syllables separated by dashes and words by spaces.

    Returns
    -------
    output : str
        Transliterated text in Lydian Script
    """
    # print(input.translate(script))

    output = input
    output = output.replace("a", "𐤠")
    output = output.replace("b", "𐤡")
    output = output.replace("p", "𐤡")
    output = output.replace("g", "𐤢")
    output = output.replace("d", "𐤣")
    output = output.replace("e", "𐤤")
    output = output.replace("v", "𐤥")
    output = output.replace("w", "𐤥")
    output = output.replace("i", "𐤦")
    output = output.replace("y", "𐤧")
    output = output.replace("k", "𐤨")
    output = output.replace("l", "𐤩")
    output = output.replace("m", "𐤪")
    output = output.replace("n", "𐤫")
    output = output.replace("o", "𐤬")
    output = output.replace("r", "𐤭")
    output = output.replace("S", "𐤮")
    output = output.replace("ś", "𐤮")
    output = output.replace("t", "𐤯")
    output = output.replace("u", "𐤰")
    output = output.replace("f", "𐤱")
    output = output.replace("q", "𐤲")
    output = output.replace("s", "𐤳")
    output = output.replace("sh","𐤳")
    output = output.replace("T", "𐤴")
    output = output.replace("ã", "𐤵")
    output = output.replace("A", "𐤵")
    output = output.replace("ẽ", "𐤶")
    output = output.replace("E", "𐤶")
    output = output.replace("L", "𐤷")
    output = output.replace("N", "𐤸")
    output = output.replace("c", "𐤹")
    output = output.replace(".", "")

    return output


if __name__ == "__main__":
       a = """
       oraL islL bakillL est mrud eśśk 
       """
       b = alpha_to_lydian(a)
       print(b)
