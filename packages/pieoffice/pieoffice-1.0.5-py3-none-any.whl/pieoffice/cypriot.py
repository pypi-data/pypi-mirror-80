#! /usr/bin/env python3

""" Cypriot script converter

If no optional argument is passed, the script converts to Cypriot Script.
The typing scheme is as follows:

-----------------------------------------------------------------------------
| a       𐠀   |   e       𐠁   |   i       𐠂   |    o       𐠃  |   u       𐠄 |
| wa      𐠲   |   we      𐠳   |   wi      𐠴   |    wo      𐠵  |             |
| za      𐠼   |               |               |    zo      𐠿  |             |
| ja      𐠅   |               |               |    jo      𐠈  |             |
| ka      𐠊   |   ke      𐠋   |   ki      𐠌   |    ko      𐠍  |   ku      𐠎 |
| la      𐠏   |   le      𐠐   |   li      𐠑   |    lo      𐠒  |   lu      𐠓 |
| ma      𐠔   |   me      𐠕   |   mi      𐠖   |    mo      𐠗  |   mu      𐠘 |
| na      𐠙   |   ne      𐠚   |   ni      𐠛   |    no      𐠜  |   nu      𐠝 |
| pa      𐠞   |   pe      𐠟   |   pi      𐠠   |    po      𐠡  |   pu      𐠢 |
| ra      𐠣   |   re      𐠤   |   ri      𐠥   |    ro      𐠦  |   ru      𐠧 |
| sa      𐠨   |   se      𐠩   |   si      𐠪   |    so      𐠫  |   su      𐠬 |
| ta      𐠭   |   te      𐠮   |   ti      𐠯   |    to      𐠰  |   tu      𐠱 |
| ksa     𐠷   |   kse     𐠸   |               |               |             |
-----------------------------------------------------------------------------

This conversion scheme supports Aegean numbers and measurements.

"""

from pieoffice.tools import get_key, aegean_numbers

def alpha_to_cypriot(input, numbers=True):
    output = input.replace("-","")

    output = output.replace("wa", "𐠲")
    output = output.replace("we", "𐠳")
    output = output.replace("wi", "𐠴")
    output = output.replace("wo", "𐠵")
    output = output.replace("za", "𐠼")
    output = output.replace("zo", "𐠿")
    output = output.replace("ja", "𐠅")
    output = output.replace("jo", "𐠈")
    output = output.replace("ka", "𐠊")
    output = output.replace("ke", "𐠋")
    output = output.replace("ki", "𐠌")
    output = output.replace("ko", "𐠍")
    output = output.replace("ku", "𐠎")
    output = output.replace("la", "𐠏")
    output = output.replace("le", "𐠐")
    output = output.replace("li", "𐠑")
    output = output.replace("lo", "𐠒")
    output = output.replace("lu", "𐠓")
    output = output.replace("ma", "𐠔")
    output = output.replace("me", "𐠕")
    output = output.replace("mi", "𐠖")
    output = output.replace("mo", "𐠗")
    output = output.replace("mu", "𐠘")
    output = output.replace("na", "𐠙")
    output = output.replace("ne", "𐠚")
    output = output.replace("ni", "𐠛")
    output = output.replace("no", "𐠜")
    output = output.replace("nu", "𐠝")
    output = output.replace("ksa", "𐠷")
    output = output.replace("kse", "𐠸")
    output = output.replace("pa", "𐠞")
    output = output.replace("pe", "𐠟")
    output = output.replace("pi", "𐠠")
    output = output.replace("po", "𐠡")
    output = output.replace("pu", "𐠢")
    output = output.replace("ra", "𐠣")
    output = output.replace("re", "𐠤")
    output = output.replace("ri", "𐠥")
    output = output.replace("ro", "𐠦")
    output = output.replace("ru", "𐠧")
    output = output.replace("sa", "𐠨")
    output = output.replace("se", "𐠩")
    output = output.replace("si", "𐠪")
    output = output.replace("so", "𐠫")
    output = output.replace("su", "𐠬")
    output = output.replace("ta", "𐠭")
    output = output.replace("te", "𐠮")
    output = output.replace("ti", "𐠯")
    output = output.replace("to", "𐠰")
    output = output.replace("tu", "𐠱")
    output = output.replace("a", "𐠀")
    output = output.replace("e", "𐠁")
    output = output.replace("i", "𐠂")
    output = output.replace("o", "𐠃")
    output = output.replace("u", "𐠄")

    output = output.replace("V", "𐄾")
    output = output.replace("M", "𐄸")
    output = output.replace("N", "𐄹")
    output = output.replace("T", "𐄼")
    output = output.replace("P", "𐄺")
    output = output.replace("Q", "𐄻")
    output = output.replace("L", "𐄷")
    output = output.replace("S", "𐄽")
    output = output.replace("Z", "𐄿")

    output = output.split()
    if numbers:
        for i in range(len(output)):
            if output[i].isnumeric():
                num_out = ""
                num = [int(j) for j in output[i]]
                tens = [10**n for n in range(len(num)-1,-1,-1)]
                for j in range(len(tens)):
                    num_out = num_out + aegean_numbers[str(num[j]*tens[j])]
                output[i] = num_out

    return " ".join(output)


if __name__ == "__main__":
       a = """
        si-se
        o-na-si-la-o 22 P
         """
       b = alpha_to_cypriot(a)
       print(b)
