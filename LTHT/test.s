.section .data
.LC0:
.byte 0x68,0x69,0x74,0x68,0x75,0x

.section .bss
	.lcomm input, 5
	
.section .text
	.globl main
main:
	movl	$0x402500, %ebp
	movl	$0,-4(%ebp)
	movl	$0xdeadbeef,-8(%ebp)
	movw	.LC0,%dx
	movw	%dx,-12(%ebp)
	leave	
	ret
