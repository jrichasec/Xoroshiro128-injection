#!/usr/bin/python
# Xoroshiro128+ - reversing the PRNG - jack richardson 2018
import z3
import sys

class xoro_inject:
	bitmask = 0xffffffffffffffff

	def __init__(self):
		pass

	def little_endian(self, injected_txt):
		assert len(injected_txt) == 16
		hexchr = [ord(c) for c in injected_txt]
		x, y = 0, 0
		for i in range(8):
			x = x + (hexchr[i] << (64 - 8 * (7 - i)))
			y = y + (hexchr[i + 8] << (64 - 8 * (7 - i)))
		return x,y

	def rotate_left(self, x, shift):
		return ((x << shift) | LShR(x, 64 - shift))  & self.bitmask

	def solve(self, string):
		chunk1, chunk2 = self.little_endian(mystr);
		print hex(chunk1)
		print hex(chunk2)
		a, b = BitVec('a', 64), BitVec('b', 64)
		xor_result = a ^ b
		new_a, new_b = (self.rotate_left(a,55) ^ xor_result ^ (xor_result << 14)) & self.bitmask, self.rotate_left(xor_result,36)
		solverZ3 = Solver()
		solverZ3.add((a + b)  & self.bitmask == chunk1, (new_a + new_b) & self.bitmask == chunk2)
		try:
			solverZ3.check()
			m = solverZ3.model()
			print("Seed 1: %s\nSeed 2: %s"%(hex(m[a].as_long()).upper(), hex(m[b].as_long()).upper()))
		except:
			print ("Had to backout, invalid string :(")



if __name__== "__main__":
	if(len(sys.argv) <2):
		print("please provide a string arg)")
		sys.exit(-1)
	mystr = sys.argv[1]
	if(len(mystr) != 16):
		print("provided string should have 16 characters, found "+str(len(mystr)))
		sys.exit(-1)
	x = xoro_inject()
	x.solve(mystr)
else:
	print("No loading..");
	sys.exit(-1)


