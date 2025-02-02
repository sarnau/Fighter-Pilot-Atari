#!/usr/bin/python

import struct,os,sys

# Return an ASCII hex dump
def dump(src, length=16):
    result = []
    digits = 2
    for i in range(0, len(src), length):
       s = src[i:i+length]
       hexa = ' '.join(["%02X" % (x) for x in s])
       text = ''.join([chr(x) if 0x20 <= x < 0x7F else '.'  for x in s])
       result.append("%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )
    return '\n'.join(result)

def parseCAS(thePath):
	print("Parsing %s" % (thePath))
	f = open(thePath, "rb") # notice the b for binary mode
	buffer = f.read()
	f.close()
#	print(dump(buffer))

	fileOffset = 0
	fileLength = len(buffer)
	files = [
		[ 0xA100, 0x80, 13 ], # loader code
		[ 0x0480, 0x640, 2 ], # main application, encrypted
		[ 0x1100, 0x7BA, 12 ], # main application continued, encrypted
		[ 0x69B8, 0x4c9, 8 ], # LENSLOK code
		[ 0x9400, 0x100, 13 ],
		[ 0xB400, 0x200, 4 ],
	]
	for file_index in range(len(files)):
		file = files[file_index]
		print('LOADING #%d AT $%04x LEN=$%04x' % (file_index, file[0],file[1] * file[2]))
		chunk_count = 0
		data = bytes()
		while chunk_count < file[2]:
			if fileOffset >= fileLength:
				break
	
			chunk_type = buffer[fileOffset:fileOffset+4].decode('ascii')
			chunk_length,param = struct.unpack_from("<HH", buffer[fileOffset+4:fileOffset+8], 0)
			chunk_data = buffer[fileOffset+8:fileOffset+8+chunk_length]
			#print(dump(chunk_data))
			if chunk_type == 'baud':
				#print('BAUD: %d baud' % param)
				pass
			elif chunk_type == 'data':
				print('DATA: LEN=$%04x PARAM=$%04x' % (chunk_length,param))
				csum = 0x00
				for i in range(0,chunk_length-1):
					csum += chunk_data[i]
					if csum > 0x100:
						csum = (csum & 0xFF) + (csum >> 8)
				if chunk_data[0] == 0x55 and chunk_data[1] == 0x55:
					if chunk_data[2] == 0xFC or chunk_data[2] == 0xFD:
						if chunk_length != file[1] + 4:
							print('CHUNK_SIZE $%04x $%04x' % (chunk_length,file[1] + 4))
						elif csum != chunk_data[-1]:
							print('CHECKSUM $%02x $%02x' % (csum,chunk_data[-1]))
						else:
							data += chunk_data[3:-1]
							chunk_count += 1
					else:
						print('RECORD $%02x' % (chunk_data[2]))
				else:
					print('MARKER $%02x $%02x' % (chunk_data[0],chunk_data[1]))
			elif chunk_type == 'FUJI' or chunk_type == 'fsk ':
				pass
			else:
				print('%s $%04x $%04x' % (chunk_type,chunk_length,param))
			fileOffset += 8 + chunk_length

		if len(data):
			f = open(thePath+'_%d_%04x.bin' % (file_index,file[0]), "wb") # notice the b for binary mode
			f.write(data)
			f.close()

parseCAS("Fighter Pilot.cas")
