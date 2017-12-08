#!/usr/bin/env python3

def wipe_timestamp_at_header(binary_file, i):
	binary_file.seek(i + 16)
	binary_file.write(b"\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30")
	binary_file.seek(i + 48)
	data_size = int(str(binary_file.read(10), 'ascii'))

	ending = binary_file.read(2)
	if ending != b"\x60\x0A":
		print('Error: Invalid header ending')
		binary_file.close()
		sys.exit(6)

	# next header position
	i = i + 60 + data_size
	return i

if __name__ == '__main__':
	import os.path
	import sys
	argc = len(sys.argv)
	if argc != 2:
		print('Usage: ar-timestamp-wiper.py <PATH_TO_STATIC_LIB>')
		sys.exit(1)

	lib_path = sys.argv[1]
	if not os.path.exists(lib_path):
		print('Error: Invalid path')
		sys.exit(2)
	
	with open(lib_path, "r+b") as binary_file:
		binary_file.seek(0, os.SEEK_END)
		file_size = binary_file.tell()  # Get the file size
		if file_size < 68:
			print('Error: truncated file header')
			binary_file.close()
			sys.exit(4)
		
		binary_file.seek(0)
		signature = binary_file.read(8)
		if signature != b"\x21\x3C\x61\x72\x63\x68\x3E\x0A": # expected: !<arch>\n
			print('Error: invalid archive signature')
			binary_file.close()
			sys.exit(5)

		i = 8 # first headers starts after signature
		while True:
			i = wipe_timestamp_at_header(binary_file, i)
			if i & 1: # Each data section is 2 byte aligned
				i += 1
			if i >= file_size:
				break
	sys.exit(0)
