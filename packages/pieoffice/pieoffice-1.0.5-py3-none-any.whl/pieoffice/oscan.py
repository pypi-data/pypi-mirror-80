#! /usr/bin/env python3

""" Oscan converter

The transliteration scheme is as follows

    ---------------------------------------------
    | a 𐌀 | b 𐌁 | g,k 𐌂 | d 𐌃 | e 𐌄 | v 𐌅 | z 𐌆 |
    | h 𐌇 | i 𐌉 | l   𐌋 | m 𐌌 | n 𐌍 | p 𐌐 | ś 𐌑 |
    | r 𐌓 | s 𐌔 | t   𐌕 | u 𐌖 | f 𐌚 | ú 𐌞 | í 𐌝 |
    ---------------------------------------------

"""

def alpha_to_oscan(input):
    """ 
    Parameters
    ----------
    input : str
        Text input with syllables separated by dashes and words by spaces.

    Returns
    -------
    output : str
        Transliterated text in Oscan Script
    """
    # print(input.translate(script))

    output = input
    output = output.replace("a","𐌀")
    output = output.replace("b","𐌁")
    output = output.replace("g","𐌂")
    output = output.replace("k","𐌂")
    output = output.replace("d","𐌃")
    output = output.replace("e","𐌄")
    output = output.replace("v","𐌅")
    output = output.replace("z","𐌆")
    output = output.replace("h","𐌇")
    output = output.replace("i","𐌉")
    output = output.replace("l","𐌋")
    output = output.replace("m","𐌌")
    output = output.replace("n","𐌍")
    output = output.replace("p","𐌐")
    output = output.replace("ś","𐌑")
    output = output.replace("r","𐌓")
    output = output.replace("s","𐌔")
    output = output.replace("t","𐌕")
    output = output.replace("u","𐌖")
    output = output.replace("f","𐌚")
    output = output.replace("ú","𐌞")
    output = output.replace("í","𐌝")
    return output


if __name__ == "__main__":
       a = """
       puklu
       """
       b = alpha_to_oscan(a)
       print(b)
