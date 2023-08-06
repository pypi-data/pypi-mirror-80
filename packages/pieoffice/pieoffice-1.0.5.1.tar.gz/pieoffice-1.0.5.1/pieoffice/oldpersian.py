#! /usr/bin/env python3

""" Old Persian converter

The transliteration scheme is as follows:

    -----------------------------------------------------------------
    | a    𐎠 | i    𐎡 | u    𐎢 | k    𐎣 | ku   𐎤 | x    𐎧 | xi   𐎧  |
    | xu   𐎧 | g    𐎥 | gu   𐎦 | c    𐎨 | ç    𐏂 | j    𐎩 | ji   𐎪  |
    | t    𐎫 | ti   𐎫 | tu   𐎬 | th   𐎰 | d    𐎭 | di   𐎮 | du   𐎯  |
    | p    𐎱 | f    𐎳 | b    𐎲 | n    𐎴 | ni   𐎴 | nu   𐎵 | m    𐎶  |
    | mi   𐎷 | mu   𐎸 | y    𐎹 | v    𐎺 | vi   𐎻 | r    𐎼 | ri   𐎽  |
    | l    𐎾 | s    𐎿 | z    𐏀 | š    𐏁 | sh   𐏁 | h    𐏃           |
    -----------------------------------------------------------------

    ----------------------------------------------------
    | ahuramazda1  𐏈 | ahuramazda2  𐏉 | ahuramazda3 𐏊  |
    | xshayathia   𐏋 | dahyaus1     𐏌 | dahyaus2    𐏌  |
    | baga         𐏎 | bumis        𐏏 |                |
    ----------------------------------------------------

"""

def alpha_to_oldpersian(input):
    """ 
    Parameters
    ----------
    input : str
        Text input with syllables separated by dashes and words by spaces.

    Returns
    -------
    output : str
        Transliterated text in Old Persian Script
    """
    # print(input.translate(script))

    output = input.replace("-","")
    output = output.replace("ahuramazda1", "𐏈")
    output = output.replace("ahuramazda2", "𐏉")
    output = output.replace("ahuramazda3", "𐏊")
    output = output.replace("xshayathia", "𐏋")
    output = output.replace("dahyaus1", "𐏌")
    output = output.replace("dahyaus2", "𐏌")
    output = output.replace("baga", "𐏎")
    output = output.replace("bumis", "𐏏")
    output = output.replace("mi", "𐎷")
    output = output.replace("mu", "𐎸")
    output = output.replace("ku", "𐎤")
    output = output.replace("xi", "𐎧")
    output = output.replace("gu", "𐎦")
    output = output.replace("xu", "𐎧")
    output = output.replace("ji", "𐎪")
    output = output.replace("ti", "𐎫")
    output = output.replace("tu", "𐎬")
    output = output.replace("th", "𐎰")
    output = output.replace("di", "𐎮")
    output = output.replace("du", "𐎯")
    output = output.replace("ni", "𐎴")
    output = output.replace("nu", "𐎵")
    output = output.replace("vi", "𐎻")
    output = output.replace("ri", "𐎽")
    output = output.replace("sh", "𐏁")
    output = output.replace("a", "𐎠")
    output = output.replace("i", "𐎡")
    output = output.replace("u", "𐎢")
    output = output.replace("k", "𐎣")
    output = output.replace("x", "𐎧")
    output = output.replace("g", "𐎥")
    output = output.replace("c", "𐎨")
    output = output.replace("ç", "𐏂")
    output = output.replace("j", "𐎩")
    output = output.replace("t", "𐎫")
    output = output.replace("d", "𐎭")
    output = output.replace("p", "𐎱")
    output = output.replace("f", "𐎳")
    output = output.replace("b", "𐎲")
    output = output.replace("n", "𐎴")
    output = output.replace("m", "𐎶")
    output = output.replace("y", "𐎹")
    output = output.replace("v", "𐎺")
    output = output.replace("r", "𐎼")
    output = output.replace("l", "𐎾")
    output = output.replace("s", "𐎿")
    output = output.replace("z", "𐏀")
    output = output.replace("š", "𐏁")
    output = output.replace("h", "𐏃")

    return output


if __name__ == "__main__":
       a = """
       ahuramazda1
       """
       b = alpha_to_oldpersian(a)
       print(b)
