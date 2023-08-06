#! /usr/bin/env python3

""" Ogham script converter

If no optional argument is passed, the script converts to Ogham Script.
The typing scheme is as follows:

    | b           ᚁ | l           ᚂ | w           ᚃ | s           ᚄ 
    | n           ᚅ | j           ᚆ | h           ᚆ | d           ᚇ 
    | t           ᚈ | k           ᚉ | kw          ᚊ | c           ᚉ 
    | cw          ᚊ | m           ᚋ | g           ᚌ | gw          ᚍ 
    | S           ᚎ | r           ᚏ | a           ᚐ | o           ᚑ 
    | u           ᚒ | e           ᚓ | i           ᚔ | ,ear,       ᚕ 
    | ,or,        ᚖ | ,uilleann,  ᚗ | ,ifin,      ᚘ | ,eam,       ᚙ 
    | ,peith,     ᚚ | >           ᚛ | <           ᚜

"""

def alpha_to_ogham(input):
    output = input

    output = output.replace(",ear,", "ᚕ")
    output = output.replace(",or,", "ᚖ")
    output = output.replace(",uilleann,", "ᚗ")
    output = output.replace(",ifin,", "ᚘ")
    output = output.replace(",eam,", "ᚙ")
    output = output.replace(",peith, ", "ᚚ")

    output = output.replace("b", "ᚁ")
    output = output.replace("l", "ᚂ")
    output = output.replace("w", "ᚃ")
    output = output.replace("s", "ᚄ")
    output = output.replace("n", "ᚅ")
    output = output.replace("j", "ᚆ")
    output = output.replace("h", "ᚆ")
    output = output.replace("d", "ᚇ")
    output = output.replace("t", "ᚈ")
    output = output.replace("kw ", "ᚊ")
    output = output.replace("k", "ᚉ")
    output = output.replace("cw ", "ᚊ")
    output = output.replace("c", "ᚉ")
    output = output.replace("m", "ᚋ")
    output = output.replace("gw ", "ᚍ")
    output = output.replace("g", "ᚌ")
    output = output.replace("S", "ᚎ")
    output = output.replace("r", "ᚏ")
    output = output.replace("a", "ᚐ")
    output = output.replace("o", "ᚑ")
    output = output.replace("u", "ᚒ")
    output = output.replace("e", "ᚓ")
    output = output.replace("i", "ᚔ")
    output = output.replace(">", "᚛")
    output = output.replace("<", "᚜")

    return output


if __name__ == "__main__":
       a = """
       >sean<
       >lielugnaedonmaccimenueh<
         """
       b = alpha_to_ogham(a)
       print(b)
