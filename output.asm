section .data
fmt_int? db "%lld", 0
num_prompt_1 db `enter a: `, 0
num_prompt_2 db `enter b: `, 0
operation_type_prompt db `1 - addition\n2 - subtract\n3 - multiply\n4 - divide\n5 - modulus\nenter your choice: `, 0
result_prompt db `result: `, 0
invalid_operation_error db `invalid operation type\n`, 0
divide_by_zero_error db `cannot divide by zero\n`, 0
new_line db `\n`, 0
section .bss
section .text
global main
extern printf
extern scanf
%define return_value rax
is_zero:
push rbp
mov rbp, rsp
sub rsp, 16
%define parameter_1 [rbp-8]
mov parameter_1, rdi
%define num [rbp-16]
mov rax, 0
cmp num, rax
jne .else_0
mov rax, 1
jmp .end
jmp .endif_0
.else_0:
mov rax, 0
jmp .end
.endif_0:
.end:
%undef parameter_1
%undef num
mov rsp, rbp
pop rbp
ret
main:
push rbp
mov rbp, rsp
sub rsp, 32
%define a [rbp-8]
%define b [rbp-16]
%define operation_type [rbp-24]
%define result [rbp-32]
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
mov rdi, operation_type_prompt
xor rax, rax
call printf
mov rdi, fmt_int?
lea rsi, operation_type
xor rax, rax
call scanf
mov rax, 1
cmp operation_type, rax
jne .else_0
mov rax, a
mov result, rax
mov rax, b
add result, rax
jmp .endif_0
.else_0:
mov rax, 2
cmp operation_type, rax
jne .else_1
mov rax, a
mov result, rax
mov rax, b
sub result, rax
jmp .endif_1
.else_1:
mov rax, 3
cmp operation_type, rax
jne .else_2
mov rax, a
mov result, rax
mov rax, result
imul rax, b
mov result, rax
jmp .endif_2
.else_2:
mov rax, 4
cmp operation_type, rax
jne .else_3
mov rdi, b
call is_zero
mov rax, 1
cmp return_value, rax
jne .else_4
mov rdi, divide_by_zero_error
xor rax, rax
call printf
mov rax, 0
jmp .end
jmp .endif_4
.else_4:
.endif_4:
mov rax, a
mov result, rax
mov rax, result
cqo
mov rbx, b
idiv rbx
mov result, rax
jmp .endif_3
.else_3:
mov rax, 5
cmp operation_type, rax
jne .else_5
mov rax, 1
cmp return_value, rax
jne .else_6
mov rdi, divide_by_zero_error
xor rax, rax
call printf
mov rax, 0
jmp .end
jmp .endif_6
.else_6:
.endif_6:
mov rax, a
mov result, rax
mov rax, result
cqo
mov rbx, b
idiv rbx
mov result, rdx
jmp .endif_5
.else_5:
mov rdi, invalid_operation_error
xor rax, rax
call printf
mov rdi, new_line
xor rax, rax
call printf
mov rax, 0
jmp .end
.endif_5:
.endif_3:
.endif_2:
.endif_1:
.endif_0:
mov rdi, result_prompt
xor rax, rax
call printf
mov rdi, fmt_int?
mov rsi, result
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
%undef operation_type
%undef result
mov rsp, rbp
pop rbp
ret
