#!/usr/bin/python

# build memory
mem = bytearray(0x9000)
buf_69b8 = open('Fighter Pilot.cas_3_69b8.bin', "rb").read()
for i in range(len(buf_69b8)):
	mem[0x69b8+i] = buf_69b8[i]
buf_0480 = open('Fighter Pilot.cas_1_0480.bin', "rb").read()
for i in range(len(buf_0480)):
	mem[0x0480+i] = buf_0480[i]
buf_1100 = open('Fighter Pilot.cas_2_1100.bin', "rb").read()
for i in range(len(buf_1100)):
	mem[0x1100+i] = buf_1100[i]

buf_9400 = open('Fighter Pilot.cas_4_9400.bin', "rb").read()
buf_b400 = open('Fighter Pilot.cas_5_b400.bin', "rb").read()

def writeApp(filename,startadr,memtop):
	def writeChunk(baseaddr,mem):
		endAdr = baseaddr + len(mem) - 1
		f.write(bytearray([0xFF,0xFF,baseaddr & 0xFF,baseaddr >> 8,endAdr & 0xFF,endAdr >> 8]))
		f.write(mem)
		
	f = open(filename, "wb")
	writeChunk(0x0480, mem[0x480:memtop])
	writeChunk(0x9400, buf_9400)
	writeChunk(0xb400, buf_b400)
	
	# launch the application after loading
	STARTADR = 0x04EB
	RUNAD = 0x02E0
	f.write(bytearray([0xFF,0xFF,RUNAD & 0xFF,RUNAD >> 8,(RUNAD + 1) & 0xFF,(RUNAD + 1) >> 8, startadr & 0xFF, startadr >> 8]))
	
	f.close()

writeApp('Fighter Pilot LENSLOK.xex', 0x8100, 0x9000)

# decrypt code
for i in range(0x500,0x8000):
	mem[i] ^= 0x49 ^ (i >> 8)

writeApp('Fighter Pilot.xex', 0x04EB, 0x8100)
