#! /usr/bin/env python3

""" Lycian converter

The transliteration scheme is as follows

    -------------------------------------------------------
    | a    𐊀 | b    𐊂 | g    𐊄 | d    𐊅 | i    𐊆 | w    𐊇 |
    | z    𐊈 | h    𐊛 | th   𐊉 | j    𐊊 | y    𐊊 | k    𐊋 |
    | l    𐊍 | m    𐊎 | n    𐊏 | u    𐊒 | p    𐊓 | k    𐊔 |
    | r    𐊕 | s    𐊖 | t    𐊗 | e    𐊁 | ã    𐊙 | ẽ    𐊚 |
    | M    𐊐 | N    𐊑 | T    𐊘 | q    𐊌 | B    𐊃 | x    𐊜 |
    -------------------------------------------------------

"""

def alpha_to_lycian(input):
    """ 
    Parameters
    ----------
    input : str
        Text input with syllables separated by dashes and words by spaces.

    Returns
    -------
    output : str
        Transliterated text in Lycian Script
    """
    # print(input.translate(script))

    output = input
    output = output.replace("a", "𐊀")
    output = output.replace("b", "𐊂")
    output = output.replace("g", "𐊄")
    output = output.replace("d", "𐊅")
    output = output.replace("i", "𐊆")
    output = output.replace("w", "𐊇")
    output = output.replace("z", "𐊈")
    output = output.replace("h", "𐊛")
    output = output.replace("j", "𐊊")
    output = output.replace("y", "𐊊")
    output = output.replace("k", "𐊋")
    output = output.replace("l", "𐊍")
    output = output.replace("m", "𐊎")
    output = output.replace("n", "𐊏")
    output = output.replace("u", "𐊒")
    output = output.replace("p", "𐊓")
    output = output.replace("k", "𐊔")
    output = output.replace("r", "𐊕")
    output = output.replace("s", "𐊖")
    output = output.replace("t", "𐊗")
    output = output.replace("e", "𐊁")
    output = output.replace("ã", "𐊙")
    output = output.replace("ẽ", "𐊚")
    output = output.replace("M", "𐊐")
    output = output.replace("N", "𐊑")
    output = output.replace("T", "𐊘")
    output = output.replace("q", "𐊌")
    output = output.replace("B", "𐊃")
    output = output.replace("x", "𐊜")
    output = output.replace("th","𐊉")

    return output


if __name__ == "__main__":
       a = """
       esbe
       """
       b = alpha_to_lycian(a)
       print(b)
