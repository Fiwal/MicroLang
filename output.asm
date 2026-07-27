section .data
fmt_out_int? db "%d", 10, 0
num? dq 10
%define num [num?]
section .bss
num_2? resq 1
%define num_2 [num_2?]
section .text
global main
extern printf
%define return_value rax
print_int:
mov rsi, rdi
mov rdi, fmt_out_int?
xor rax, rax
call printf
ret
operation:
push rbp
mov rbp, rsp
sub rsp, 48
%define parameter_1 [rbp-8]
mov parameter_1, rdi
%define parameter_2 [rbp-16]
mov parameter_2, rsi
%define parameter_3 [rbp-24]
mov parameter_3, rdx
%define parameter_4 [rbp-32]
mov parameter_4, rcx
%define result [rbp-40]
mov rax, parameter_1
mov result, rax
mov rax, parameter_2
add result, rax
mov rax, result
imul rax, parameter_3
mov result, rax
mov rax, parameter_4
sub result, rax
mov rax, result
imul rax, -1
mov result, rax
mov rax, result
jmp .end
.end:
%undef parameter_1
%undef parameter_2
%undef parameter_3
%undef parameter_4
%undef result
mov rsp, rbp
pop rbp
ret
main:
push rbp
mov rbp, rsp
sub rsp, 16
%define a [rbp-8]
mov rax, 5
mov a, rax
mov rax, 12
mov num_2, rax
mov rdi, a
mov rsi, num
mov rdx, num_2
mov rcx, 7
call operation
mov rdi, return_value
call print_int
mov rax, 0
jmp .end
.end:
%undef a
mov rsp, rbp
pop rbp
ret
