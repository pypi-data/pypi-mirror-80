#! /usr/bin/env python3

""" Carian converter

The transliteration scheme is as follows

    -------------------------------------------------------------------
    | a      𐊠 | b      𐊡 | d      𐊢 | l      𐊣 | y      𐊤 | y2     𐋐 |
    | r      𐊥 | L      𐊦 | L2     𐋎 | A2     𐊧 | q      𐊨 | b      𐊩 |
    | m      𐊪 | o      𐊫 | D2     𐊬 | t      𐊭 | sh     𐊮 | sh2    𐊯 |
    | s      𐊰 | 18     𐊱 | u      𐊲 | N      𐊳 | c      𐊴 | n      𐊵 |
    | T2     𐊶 | p      𐊷 | 's,ś   𐊸 | i      𐊹 | e      𐊺 | ý,'y   𐊻 |
    | k      𐊼 | k2     𐊽 | dh     𐊾 | w      𐊿 | G      𐋀 | G2     𐋁 |
    | z2     𐋂 | z      𐋃 | ng     𐋄 | j      𐋅 | 39     𐋆 | T      𐋇 |
    | y3     𐋈 | r2     𐋉 | mb     𐋊 | mb2    𐋋 | mb3    𐋌 | mb4    𐋍 |
    | e2     𐋏 |                                                      |
    -------------------------------------------------------------------

"""

def alpha_to_carian(input):
    """ 
    Parameters
    ----------
    input : str
        Text input with syllables separated by dashes and words by spaces.

    Returns
    -------
    output : str
        Transliterated text in Carian Script
    """
    # print(input.translate(script))

    output = input
    output = output.replace("a", "𐊠")
    output = output.replace("e2", "𐋏")
    output = output.replace("r2", "𐋉")
    output = output.replace("z2", "𐋂")
    output = output.replace("b", "𐊡")
    output = output.replace("d", "𐊢")
    output = output.replace("l", "𐊣")
    output = output.replace("y3", "𐋈")
    output = output.replace("y2", "𐋐")
    output = output.replace("ý", "𐊻")
    output = output.replace("'y", "𐊻")
    output = output.replace("y", "𐊤")
    output = output.replace("r", "𐊥")
    output = output.replace("L2", "𐋎")
    output = output.replace("L", "𐊦")
    output = output.replace("A2", "𐊧")
    output = output.replace("q", "𐊨")
    output = output.replace("b", "𐊩")
    output = output.replace("m", "𐊪")
    output = output.replace("o", "𐊫")
    output = output.replace("D2", "𐊬")
    output = output.replace("t", "𐊭")
    output = output.replace("sh2", "𐊯")
    output = output.replace("sh", "𐊮")
    output = output.replace("'s", "𐊸")
    output = output.replace("ś", "𐊸")
    output = output.replace("s", "𐊰")
    output = output.replace("18", "𐊱")
    output = output.replace("u", "𐊲")
    output = output.replace("N", "𐊳")
    output = output.replace("c", "𐊴")
    output = output.replace("n", "𐊵")
    output = output.replace("T2", "𐊶")
    output = output.replace("p", "𐊷")
    output = output.replace("i", "𐊹")
    output = output.replace("e", "𐊺")
    output = output.replace("k2", "𐊽")
    output = output.replace("k", "𐊼")
    output = output.replace("dh", "𐊾")
    output = output.replace("w", "𐊿")
    output = output.replace("G2", "𐋁")
    output = output.replace("G", "𐋀")
    output = output.replace("z", "𐋃")
    output = output.replace("ng", "𐋄")
    output = output.replace("j", "𐋅")
    output = output.replace("39", "𐋆")
    output = output.replace("T", "𐋇")
    output = output.replace("mb2", "𐋋")
    output = output.replace("mb3", "𐋌")
    output = output.replace("mb4", "𐋍")
    output = output.replace("mb", "𐋊")

    return output


if __name__ == "__main__":
       a = """
       esbe
       """
       b = alpha_to_carian(a)
       print(b)
