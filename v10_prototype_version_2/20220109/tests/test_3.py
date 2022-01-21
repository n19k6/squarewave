# written for MicroPython v1.17-333-gcf258c898 on 2022-01-16; win32 version

#import re
#import sys
from sys import exit
from re import match
from array import array
from uctypes import addressof

# signal_1 = 34+2 k, signal_2 = 3 n, signal_3 = 4 z, signal_4 = auxilary to messure frequency

# todo: memory layout mem_slot_1

# code sample "20220104_drei_signale_003.py"

signal_1a = "111111111111111111111100000000001111111111111111111110000000000000111111111111111111111000000000000011111111111111111111100000000000011111111000"
signal_2a = "011111111111111111111100111111111111111111111000000000000011111111111111111111100000000000001111111111111111111110000000000000111111100000000000"
signal_3a = "110000000000000000000001111111111000000000000000000011111111110000000000000000000111111111100000000000000000001111111111000000000000000000011111"
signal_4a = "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

signal_1b = "011111111111111111111100000000001111111111111111111110000000000000111111111111111111111000000000000011111111111111111111100000000000011111111000"
signal_2b = "011111111111111111111100111111111111111111111000000000000011111111111111111111100000000000001111111111111111111110000000000000111111100000000000"
signal_3b = "110000000000000000000001111111111000000000000000000011111111110000000000000000000111111111100000000000000000001111111111000000000000000000011111"
signal_4b = "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

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

mem_slot_1 = array("I", [0 for _ in range(36)])
mem_slot_2 = array("I", [0 for _ in range(36)])



def fill_mem_slot_1(n, z):
	global mem_slot_1
	#mem_slot_1[0] = 0b00001011
	#signal_1 = "1100111100001111"

	for s in range(len(signal_1)):
		#calculate j (junk), k (position)
		i = s*4+1
		j, k = int(i/32), i % 32
		if signal_1[s] == "1":
			mem_slot_1[j] = mem_slot_1[j] | 1<<31-k
		else:
			mem_slot_1[j] = mem_slot_1[j] & ~(1<<31-k)
			
	for s in range(len(signal_2)):
		#calculate j (junk), k (position)
		i = ((s*4+n*4)+2) % 288
		j, k = int(i/32), i % 32
		
		if signal_1[s] == "1":
			mem_slot_1[j] = mem_slot_1[j] | 1<<31-k
		else:
			mem_slot_1[j] = mem_slot_1[j] & ~(1<<31-k)

	for s in range(len(signal_3)):
		#calculate j (junk), k (position)
		i = ((s*4+z*4)+3) % 288
		j, k = int(i/32), i % 32
		if signal_1[s] == "1":
			mem_slot_1[j] = mem_slot_1[j] | 1<<31-k
		else:
			mem_slot_1[j] = mem_slot_1[j] & ~(1<<31-k)
			
	for s in range(len(signal_4)):
		#calculate j (junk), k (position)
		i = s*4
		j, k = int(i/32), i % 32
		if signal_1[s] == "1":
			mem_slot_1[j] = mem_slot_1[j] | 1<<31-k
		else:
			mem_slot_1[j] = mem_slot_1[j] & ~(1<<31-k)

def fill_mem_slot_2(n, z):
	global mem_slot_2
	#mem_slot_2[0] = 0b00001011
	#signal_1 = "1100111100001111"

	for s in range(len(signal_1)):
		#calculate j (junk), k (position)
		i = s*4+1
		j, k = int(i/32), i % 32
		if signal_1[s] == "1":
			mem_slot_2[j] = mem_slot_2[j] | 1<<31-k
		else:
			mem_slot_2[j] = mem_slot_2[j] & ~(1<<31-k)
			
	for s in range(len(signal_2)):
		#calculate j (junk), k (position)
		i = ((s*4+n*4)+2) % 288
		j, k = int(i/32), i % 32
		
		if signal_1[s] == "1":
			mem_slot_2[j] = mem_slot_2[j] | 1<<31-k
		else:
			mem_slot_2[j] = mem_slot_2[j] & ~(1<<31-k)

	for s in range(len(signal_3)):
		#calculate j (junk), k (position)
		i = ((s*4+z*4)+3) % 288
		j, k = int(i/32), i % 32
		if signal_1[s] == "1":
			mem_slot_2[j] = mem_slot_2[j] | 1<<31-k
		else:
			mem_slot_2[j] = mem_slot_2[j] & ~(1<<31-k)
			
	for s in range(len(signal_4)):
		#calculate j (junk), k (position)
		i = s*4
		j, k = int(i/32), i % 32
		if signal_1[s] == "1":
			mem_slot_2[j] = mem_slot_2[j] | 1<<31-k
		else:
			mem_slot_2[j] = mem_slot_2[j] & ~(1<<31-k)


i = 288+2
i = -1
print(i)
print(i % 288)

fill_mem_slot_1(0,0)
fill_mem_slot_2(-2,2)

print(bin(mem_slot_1[0]))
print(addressof(mem_slot_1))

print(bin(mem_slot_2[0]))
print(addressof(mem_slot_2))