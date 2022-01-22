# written for MicroPython v1.17-333-gcf258c898 on 2022-01-16; win32 version

#import re
#import sys
from sys import exit
from re import match, compile
from array import array
from uctypes import addressof

# signal_1 = 34+2 k, signal_2 = 3 n, signal_3 = 4 z, signal_4 = auxilary to messure frequency

# todo: memory layout mem_slot_1

# code sample "20220104_drei_signale_003.py"

signal_1a = "111111111111111111111100000000001111111111111111111110000000000000111111111111111111111000000000000011111111111111111111100000000000011111111000"
signal_2a = "011111111111111111111100111111111111111111111000000000000011111111111111111111100000000000001111111111111111111110000000000000111111100000000000"
signal_3a = "000000000001000000000001000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
signal_4a = "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

signal_1b = "011111111111111111111100000000001111111111111111111110000000000000111111111111111111111000000000000011111111111111111111100000000000011111111000"
signal_2b = "011111111111111111111100111111111111111111111000000000000011111111111111111111100000000000001111111111111111111110000000000000111111100000000000"
signal_3b = "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"
signal_4b = "000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

def peaks(s):
	fe = compile("10") # fe = falling edge
	if s[0] == "0" and s[-1] == "1":
		return len(fe.split(s))
	else:
		#print(fe.split(s))
		return len(fe.split(s))-1

def suppress(o1, o2, o3, o4):
	fe = compile("10") # fe = falling edge
	if s[-1] == "0":
		return len(fe.split(s))
	else:
		#print(fe.split(s))
		return len(fe.split(s))-1



# check format of signals

#https://docs.micropython.org/en/latest/library/re.html -> counted repetitions ({m,n}) are not supported in micropython

signals = [signal_1a, signal_2a, signal_3a, signal_4a, signal_1b, signal_2b, signal_3b, signal_4b]

#if (not re.match("^[01]+$", signal_1) or len(signal_1) != 34):
#	print("E: signal_1 is not a valid string")
#	sys.exit(1)

for signal in signals:
	if (not match("^[01]+$", signal) or len(signal) != 144):
		print("E: signal \""+signal+"\" is not a valid string")
		exit(1)

signal_1 = signal_1a+signal_1b
signal_2 = signal_2a+signal_2b
signal_3 = signal_3a+signal_3b
signal_4 = signal_4a+signal_4b

if (peaks(signal_3) != 4):
	print("E: signal_3 does not contain 4 peaks.")
	exit(1)


# signal_3 has to be 4 peaks

a = "0011110001001000"
#print(match("^.*01.*$", a))



a = "0011110001001000"
print(peaks(a))

exit(1)

a = "i love my dog"




def shift(s, n):
	#shift("i love my dog",0) -> "i love my dog"
	#shift("i love my dog",-1) -> " love my dogi"
	#shift("i love my dog",2) -> "ogi love my d"
	#shift("i love my dog",-1000922) -> "i love my dog"
	#shift("i love my dog",-1000921) -> "gi love my do"
	l = len(a)
	n = n % l
	return a[l-n:]+a[0:l-n]

print('shift("i love my dog",0) -> "'+shift("i love my dog",0)+'"')
print('shift("i love my dog",-1) -> "'+shift("i love my dog",-1)+'"')
print('shift("i love my dog",2) -> "'+shift("i love my dog",2)+'"')
print('shift("i love my dog",-1000922) -> "'+shift("i love my dog",-1000922)+'"')
print('shift("i love my dog",-1000921) -> "'+shift("i love my dog",-1000921)+'"')

#print(shift("i love my dog",2))
#print(shift("i love my dog",-1))
#print(shift("i love my dog",-1000922))
#print(shift("i love my dog",-1000921))
