import re

def capitalise(inp):
    # capitalise the first letter of each word in a string
    out = []
    for word in inp.split(" "):
        out.append(word[0].upper() + word[1:].lower())
    
    return " ".join(out)

def ukCoordsToSectorFile(inA, inB):
    # convert from XXXXXX.XXN to NXXX.XX.XX.XXX etc
    if re.match(r"[0-9]{6}(?:\.[0-9]{2}|)[N|S]", inA) is None or re.match(r"[0-9]{7}(?:\.[0-9]{2}|)[E|W]", inB) is None:
        raise ValueError(f"Invalid coordinates provided: {inA}, {inB}")
    outA = inA[-1] + "0" + inA[:2] + "." + inA[2:4] + "." + inA[4:6] + "." + inA[7:9].ljust(3, '0')
    outB = inB[-1] + inB[:3] + "." + inB[3:5] + "." + inB[5:7] + "." + inB[8:10].ljust(3, '0')
    return (outA, outB)  # probably should be a tuple
