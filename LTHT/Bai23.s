.section .data
msg: .string "Doi xung"
msg2: .string "Khong doi xung"

.section .bss
	.lcomm input, 5
	
.section .text
	.globl _start
_start:
	movl $3, %eax
	movl $0, %ebx
	movl $input, %ecx
	movl $5, %edx
	int $0x80
	
	movl $0x104, %eax
	mov (%eax), %bl
	cmpb 4(%eax), %bl
	jne L2
	mov 1(%eax), %bl
	cmpb 3(%eax), %bl
	jne L2
	movl $4, %eax
        movl $1, %ebx
        movl $msg, %ecx
        movl $9, %edx
        int $0x80
		
	movl $1, %eax
	int $0x80
L2:
	movl $4, %eax
        movl $1, %ebx
        movl $msg2, %ecx
        movl $15, %edx
        int $0x80       
        movl $1, %eax
	int $0x80	
