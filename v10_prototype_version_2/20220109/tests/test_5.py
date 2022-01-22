import helper

signal_a = "100101010001111"
helper.suppress(signal_a, False, False, True, True)


#print(helper.peaks("00011101"))
#import re


# case trailing 00-x
#       0      1    2       3
# |----__-----__---__------__---|
#    0     1     2     3       4
# case trailing 10-x
#       0      1    2       3
# |----__-----__---__------__|
#    0     1     2     3       4=''
# case trailing 1-0
#       0      1    2       3
# |----__-----__---__------__---|
#    0     1     2     3       4
# case trailing 1-1
#       0      1    2       3
# |----__-----__---__------|
#    0     1     2     3       4=''

#def suppress(s, p1, p2, p3, p4):
#    print(s)

    
#    # print("s: "+s)
#    #print("o1: "+str(o1))
#    #print("o2: "+str(o2))
#    #print("o3: "+str(o3))
#    #print("o4: "+str(o4))
#    #return ([s, o1, o2, o3, o4])
#    fe = re.compile("10") # fe = falling edge
#    if s[-1] == "0":
#        parts = fe.split(s)
#        gaps = ["10", "10", "10", "10"]
#        params = [p1, p2, p3, p4]
#        for i in range(len(params)):
#            if params[i]:
#                parts[i] = parts[i].replace("1", "0")
#                gaps[i] = "00"
#    
#    print(parts[0]+gaps[0]+parts[1]+gaps[1]+parts[2]+gaps[2]+parts[3]+gaps[3]+parts[4])
#    return "alf"



#suppress(signal_a, False, True, False, True)

#print(signal_a)

#zeros = re.compile("0+")
#ones = re.compile("1+")

#list_zeros = ones.split(signal_a)
#list_ones = zeros.split(signal_a)

#print(str(list_zeros)+" "+str(len(list_zeros)))
#print(str(list_ones)+" "+str(len(list_ones)))


#a = ''
#if list_ones[0] == '':
#    for i in range(len(list_ones)):
#        a = a+list_ones[i]
#        a = a+list_zeros[i]
#else:
#    for i in range(len(list_ones)):
#        a = a+list_zeros[i]
#        a = a+list_ones[i]#

#print(a)



