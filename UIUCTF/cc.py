from pwn import disasm


valid_instructions = []

for byte in range(0x00,0xff):
	if (byte & 1) != 0:
		valid_instructions.append(byte)

for valid_byte in valid_instructions:
	byte = valid_byte.to_bytes(1,'little')
	print(disasm(byte,arch= "amd64"))
