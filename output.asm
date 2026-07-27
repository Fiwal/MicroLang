section .data
fmt_int? db "%d", 0
new_line db 10, 0
num_prompt_1 db "a: ", 0
num_prompt_2 db "b: ", 0
add_prompt db "a + b = ", 0
sub_prompt db "a - b = ", 0
section .bss
section .text
global main
extern printf
extern scanf
%define return_value rax
main:
push rbp
mov rbp, rsp
sub rsp, 32
%define a [rbp-8]
%define b [rbp-16]
mov rdi, num_prompt_1
xor rax, rax
call printf
mov rdi, fmt_int?
lea rsi, a
xor rax, rax
call scanf
mov rdi, num_prompt_2
xor rax, rax
call printf
mov rdi, fmt_int?
lea rsi, b
xor rax, rax
call scanf
%define c [rbp-24]
mov rax, a
mov c, rax
mov rax, b
add c, rax
mov rdi, add_prompt
xor rax, rax
call printf
mov rdi, fmt_int?
mov rsi, c
xor rax, rax
call printf
mov rdi, new_line
xor rax, rax
call printf
mov rax, a
mov c, rax
mov rax, b
sub c, rax
mov rdi, sub_prompt
xor rax, rax
call printf
mov rdi, fmt_int?
mov rsi, c
xor rax, rax
call printf
mov rdi, new_line
xor rax, rax
call printf
mov rax, 0
jmp .end
.end:
%undef a
%undef b
%undef c
mov rsp, rbp
pop rbp
ret
