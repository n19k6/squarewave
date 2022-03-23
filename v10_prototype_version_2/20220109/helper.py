import re

def junk(s):
    return not (re.match("^[01]+$", s) is None) and len(s) == 144

def peaks(s):
    fe = re.compile("10") # fe = falling edge
    if s[0] == "0" and s[-1] == "1":
        return len(fe.split(s))
    else:
        return len(fe.split(s))-1

def shift(s, n):
    l = len(s)
    n = n % l
    return s[l-n:]+s[0:l-n]

def suppress(s, p1, p2, p3, p4):
    #print(s)
    l = len(s)
    m = 0
    n = s[0] == "1" and s[-1] == "0"
    if not n:
        m = "".join(reversed(s)).find("0")
        s = shift(s, m)
    #print(s)
    fe = re.compile("10") # fe = falling edge
    parts = fe.split(s)
    last_part = parts[-1]
    parts = [x+"10" for x in parts]
    parts[-1] = last_part
    if not p1:
        parts[0] = parts[0].replace("1", "0")
    if not p2:
        parts[1] = parts[1].replace("1", "0")
    if not p3:
        parts[2] = parts[2].replace("1", "0")
    if not p4:
        parts[3] = parts[3].replace("1", "0")
    #print(''.join(parts))
    s = ''.join(parts)
    if not n:
        s = shift(s, l-m)
    #print(s)
    return s





if __name__ == "__main__":
    
    # testing junk
    assert junk("100011") == False
    assert junk("1100"*34+"0000"+"000") == False
    assert junk("1100"*34+"0000"+"0000") == True
    assert junk("1100"*34+"0000"+"00000") == False
    assert junk("1100"*34+"0000"+"00A0") == False
            
    # testing peaks
    assert peaks("00010010010") == 3
    assert peaks("00010010001") == 3
    assert peaks("00000000000") == 0
    assert peaks("11111111111") == 0
    assert peaks("11111011111") == 1
    
    # testing shift
    assert shift("i love my dog",0) == "i love my dog"
    assert shift("i love my dog",-1) == " love my dogi"
    assert shift("i love my dog",2) == "ogi love my d"
    assert shift("i love my dog",-1000922) == "i love my dog"
    assert shift("i love my dog",-1000921) == "gi love my do"
    
    # testing suppress
    signal_a = "0011100100110100"
    signal_b = "00111001001010"
    signal_c = "00111001011001"
    signal_d = "10111001011001"
    assert peaks(signal_a) == 4
    assert peaks(signal_b) == 4
    assert peaks(signal_c) == 4
    assert peaks(signal_d) == 4
    assert suppress(signal_a, True, True, True, True) == "0011100100110100"
    assert suppress(signal_a, False, False, True, True) == "0000000000110100"
    assert suppress(signal_a, False, False, False, False) == "0000000000000000"
    assert suppress(signal_d, False, True, True, True) == "00111001011000"
    assert suppress(signal_d, True, False, True, True) == "10000001011001"
    assert suppress(signal_d, True, True, False, True) == "10111000011001"
    assert suppress(signal_d, True, True, True, False) == "10111001000001"
    assert suppress(signal_d, False, True, False, True) == "00111000011000"
    