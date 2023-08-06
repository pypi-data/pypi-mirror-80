#!/usr/bin/env python3

""" Armenian script converter

This scripts allows the user to convert between the latinized transliteration
of Armenian and the Armenian Script itself with (almost) simple rules.

Usage
-----
pieoffice armenian <text>
    ----------------------------------------------------------------
    | a 	 ա | b	    բ | g	 գ | d	    դ | e	 ե |
    | ye	 ե | z      զ | ee	 է | e'     ը | t'	 թ | 
    | zh	 ժ | i	    ի | l	 լ | x	    խ | c	 ծ | 
    | k 	 կ | h      հ | j	 ձ | g.     ղ | l.	 ղ |
    | ch.	 ճ | m      մ | y	 յ | n      ն | sh	 շ |
    | o 	 ո | ch     չ | p	 պ | jh     ջ | r.	 ռ | 
    | s	         ս | v	    վ | t        տ | r	    ր | c'	 ց |
    | w          ւ | p'     փ | k'       ք | o'     օ | f 	 ֆ |
    | u	         ու| ev     և | ?	 ՞ | .      ։ | .'	 ՝ |
    | ;          ՟ | ;'     ՛ | !	 ՜ | ``     « | ''	 » |
    ----------------------------------------------------------------

"""

def alpha_to_armenian(input):
    """ Converts text in Latin Alphabet to Armenian Script

    Each syllable should be separated by a sing dash, each word by a space.

    Parameters
    ----------
    input : str
        Text input with syllables separated by dashes and words by spaces.

    Returns
    -------
    output : str
        Transliterated text in Armenian Script

    Usage
    -----
    
    > alpha_to_armenian("<++>")
    + 

    """
    # print(input.translate(script))

    output = input

    output = output.replace("ye", "ե")
    output = output.replace("YE", "Ե")
    output = output.replace("Ye", "Ե")
    output = output.replace("ee", "է")
    output = output.replace("EE", "Է")
    output = output.replace("ev", "և")
    output = output.replace("e'", "ը")
    output = output.replace("E'", "Ը")

    output = output.replace("e", "ե")
    output = output.replace("E", "Ե")

    output = output.replace("zh", "ժ")
    output = output.replace("ch", "չ")
    output = output.replace("ch.", "ճ")
    output = output.replace("sh", "շ")
    output = output.replace("jh", "ջ")
    output = output.replace("ZH", "Ժ")
    output = output.replace("CH.", "Ճ")
    output = output.replace("SH", "Շ")
    output = output.replace("CH", "Չ")
    output = output.replace("JH", "Ջ")

    output = output.replace("t'", "թ")
    output = output.replace("p'", "փ")
    output = output.replace("k'", "ք")
    output = output.replace("o'", "օ")
    output = output.replace("c'", "ց")
    output = output.replace("P'", "Փ")
    output = output.replace("C'", "Ց")
    output = output.replace("K'", "Ք")
    output = output.replace("O'", "Օ")
    output = output.replace("T'", "Թ")

    output = output.replace("g.", "ղ")
    output = output.replace("l.", "ղ")
    output = output.replace("r.", "ռ")
    output = output.replace("V.", "Վ")
    output = output.replace("R.", "Ռ")
    output = output.replace("G.", "Ղ")


    output = output.replace("I", "Ի")
    output = output.replace("L", "Լ")
    output = output.replace("X", "Խ")
    output = output.replace("C", "Ծ")
    output = output.replace("K", "Կ")
    output = output.replace("J", "Ձ")
    output = output.replace("M", "Մ")
    output = output.replace("Y", "Յ")
    output = output.replace("N", "Ն")
    output = output.replace("O", "Ո")
    output = output.replace("P", "Պ")
    output = output.replace("S", "Ս")
    output = output.replace("T", "Տ")
    output = output.replace("R", "Ր")
    output = output.replace("W", "Ւ")
    output = output.replace("F", "Ֆ")
    output = output.replace("U", "Սւ")
    output = output.replace("a", "ա")
    output = output.replace("b", "բ")
    output = output.replace("g", "գ")
    output = output.replace("d", "դ")
    output = output.replace("z", "զ")
    output = output.replace("i", "ի")
    output = output.replace("l", "լ")
    output = output.replace("x", "խ")
    output = output.replace("c", "ծ")
    output = output.replace("k", "կ")
    output = output.replace("j", "ձ")
    output = output.replace("m", "մ")
    output = output.replace("y", "յ")
    output = output.replace("n", "ն")
    output = output.replace("o", "ո")
    output = output.replace("p", "պ")
    output = output.replace("s", "ս")
    output = output.replace("v", "վ")
    output = output.replace("t", "տ")
    output = output.replace("r", "ր")
    output = output.replace("w", "ւ")
    output = output.replace("f", "ֆ")
    output = output.replace("u", "ու")
    output = output.replace("A", "Ա")
    output = output.replace("B", "Բ")
    output = output.replace("G", "Գ")
    output = output.replace("D", "Դ")
    output = output.replace("Z", "Զ")

    output = output.replace("h", "հ")
    output = output.replace("H", "Հ")


    output = output.replace("?", "՞")
    output = output.replace(".", "։")
    output = output.replace(".'", "՝")
    output = output.replace(";", "՟")
    output = output.replace(";'", "՛")
    output = output.replace("!", "՜")
    output = output.replace("``", "«")
    output = output.replace("''", "»")

    return output


if __name__ == "__main__":
       a = """
       Erkneer erkin erkneer erkir
       Erkneer ev covn cirani
       Erkn i covown owneer
       zkarmirkn el.egnik

       E'nd el.egan p'ol. cowx elaneer
       E'nd el.egan p'ol. boc' elaneer
       Ew i boc'oyn vazeer
       Xarteash patanekik

       na howr her owneer
       boc' owneer mawrows
       Ew achk'ownk'n eein aregakownk'
       """
       b = alpha_to_armenian(a)
       print(b)
