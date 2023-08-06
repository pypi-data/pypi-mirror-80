#! /usr/bin/env python3

""" Avestan script converter

If no optional argument is passed, the script converts to Avestan Script.
Else, you can pass the optional argument translit for converting to
latin script with macrons and diacritics for Avestan.
The typing scheme is as follows:

--------------------------------------------------------------------------
| a   a   𐬀  | A   ā   𐬁  ||  á   å  𐬂  | Á ā̊  𐬃  || ã  ą  𐬄 | ãã  ą̇   𐬅 |
| æ   ə   𐬆  | Æ   ə̄   𐬇  ||  e   e  𐬈  | E ē  𐬉  || o  o  𐬊 | O   ō   𐬋 |
| i   i   𐬌  | I   ī   𐬍  ||  u   u  𐬎  | U ū  𐬏  || k  k  𐬐 | x   x   𐬑 |
| X   x́   𐬒  | xw  x   𐬓  ||  g   g  𐬔  | G ġ  𐬕  || gh γ  𐬖 | c   č   𐬗 |
| j   ǰ   𐬘  | t   t   𐬙  ||  th  ϑ  𐬚  | d d  𐬛  || dh δ  𐬜 | T   t̰   𐬝 |
| p   p   𐬞  | f   f   𐬟  ||  b   b  𐬠  | B β  𐬡  || ng ŋ  𐬢 | ngh ŋ́   𐬣 |
| ngw ŋ   𐬤  | n   n   𐬥  ||  ñ   ń  𐬦  | N ṇ  𐬧  || m  m  𐬨 | M   m̨   𐬩 |
| Y   ẏ   𐬪  | y   y   𐬫  ||  v   v  𐬬  | r r  𐬭  || s  s  𐬯 | z   z   𐬰 |
| sh  š   𐬱  | zh  ž   𐬲  ||  shy š́  𐬳  | S ṣ̌  𐬴  || h  h  𐬵 |           |
--------------------------------------------------------------------------

"""

def alpha_to_avestan(input):
    """ Converts text in Latin Alphabet to Avestan Script

    Each syllable should be separated by a sing dash, each word by a space.

    Parameters
    ----------
    input : str
        Text input with syllables separated by dashes and words by spaces.

    Returns
    -------
    output : str
        Transliterated text in Avestan Script

    Usage
    -----
    
    > alpha_to_avestan("<++>")
    + 

    """
    # print(input.translate(script))

    output = input
    output = output.replace("A", "𐬁")
    output = output.replace("aa", "𐬀")
    output = output.replace("a", "𐬀")
    output = output.replace("Á", "𐬃")
    output = output.replace("áá", "𐬂")
    output = output.replace("á", "𐬂")
    output = output.replace("ãã", "𐬅")
    output = output.replace("ã", "𐬄")
    output = output.replace("ææ", "𐬆")
    output = output.replace("æ", "𐬆")
    output = output.replace("Æ", "𐬇")
    output = output.replace("ee", "𐬈")
    output = output.replace("e", "𐬈")
    output = output.replace("E", "𐬉")
    output = output.replace("oo", "𐬊")
    output = output.replace("o", "𐬊")
    output = output.replace("O", "𐬋")
    output = output.replace("i", "𐬌")
    output = output.replace("I", "𐬍")
    output = output.replace("u", "𐬎")
    output = output.replace("U", "𐬏")
    output = output.replace("k", "𐬐")
    output = output.replace("X", "𐬒")
    output = output.replace("xw", "𐬓")
    output = output.replace("x", "𐬑")
    output = output.replace("c", "𐬗")
    output = output.replace("j", "𐬘")
    output = output.replace("th", "𐬚")
    output = output.replace("t", "𐬙")
    output = output.replace("dh", "𐬜")
    output = output.replace("d", "𐬛")
    output = output.replace("T", "𐬝")
    output = output.replace("p", "𐬞")
    output = output.replace("f", "𐬟")
    output = output.replace("b", "𐬠")
    output = output.replace("B", "𐬡")
    output = output.replace("ngh", "𐬣")
    output = output.replace("ngw", "𐬤")
    output = output.replace("ng", "𐬢")
    output = output.replace("gh", "𐬖")
    output = output.replace("g", "𐬔")
    output = output.replace("G", "𐬕")
    output = output.replace("ñ", "𐬦")
    output = output.replace("n", "𐬥")
    output = output.replace("N", "𐬧")
    output = output.replace("m", "𐬨")
    output = output.replace("M", "𐬩")
    output = output.replace("Y", "𐬪")
    output = output.replace("y", "𐬫")
    output = output.replace("v", "𐬬")
    output = output.replace("r", "𐬭")
    output = output.replace("sh", "𐬱")
    output = output.replace("zh", "𐬲")
    output = output.replace("shy", "𐬳")
    output = output.replace("S", "𐬴")
    output = output.replace("s", "𐬯")
    output = output.replace("z", "𐬰")
    output = output.replace("h", "𐬵")

    return output


def alpha_to_avestan_trans(input):
    output = input
    output = output.replace("A", "ā")
    output = output.replace("aa", "ā")
    output = output.replace("Á", "ā̊")
    output = output.replace("áá", "ā̊")
    output = output.replace("á", "å")
    output = output.replace("Ã", "ą̇")
    output = output.replace("ãã", "ą̇")
    output = output.replace("ã", "ą")
    output = output.replace("ææ", "ə̄")
    output = output.replace("æ", "ə")
    output = output.replace("Æ", "ə̄")
    output = output.replace("ee", "ē")
    output = output.replace("E", "ē")
    output = output.replace("oo", "ō")
    output = output.replace("O", "ō")
    output = output.replace("I", "ī")
    output = output.replace("U", "ū")
    output = output.replace("X", "x́")
    output = output.replace("xw", "xᵛ")
    output = output.replace("c", "č")
    output = output.replace("j", "ǰ")
    output = output.replace("th", "ϑ")
    output = output.replace("dh", "δ")
    output = output.replace("T", "t̰")
    output = output.replace("B", "β")
    output = output.replace("ngh", "ŋ́")
    output = output.replace("ngw", "ŋᵛ")
    output = output.replace("ng", "ŋ")
    output = output.replace("gh", "γ")
    output = output.replace("G", "ġ")
    output = output.replace("ñ", "ń")
    output = output.replace("N", "ṇ")
    output = output.replace("m", "m")
    output = output.replace("M", "m̨")
    output = output.replace("Y", "ẏ")
    output = output.replace("sh", "š")
    output = output.replace("zh", "ž")
    output = output.replace("shy", "š́")
    output = output.replace("S", "ṣ̌")
    

    return output


if __name__ == "__main__":
       a = """
       paoiriiáá dasa xshpanoo
       spitama zarathushtra
       tishtrioo raeeuuáá xwarænangwháá
       """
       b = alpha_to_avestan(a)
       print(b)
