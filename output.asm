section .data
fmt_int? db "%lld", 0
num_prompt_1 db `enter a: `, 0
num_prompt_2 db `enter b: `, 0
operation_type_prompt db `1 - addition\n2 - subtract\n3 - multiply\n4 - divide\n5 - modulus\nenter your choice: `, 0
result_prompt db `result: `, 0
invalid_operation_error_prompt db `invalid operation type\n`, 0
divide_by_zero_error_prompt db `cannot divide by zero\n`, 0
new_line db `\n`, 0
division_by_zero_error? dq 0
%define division_by_zero_error [division_by_zero_error?]
invalid_operation_error? dq 0
%define invalid_operation_error [invalid_operation_error?]
section .bss
section .text
global main
extern printf
extern scanf
%define return_value rax
calculate:
push rbp
mov rbp, rsp
sub rsp, 32
%define parameter_0 [rbp-8]
mov parameter_0, rdi
%define parameter_1 [rbp-16]
mov parameter_1, rsi
%define parameter_2 [rbp-24]
mov parameter_2, rdx
%define a parameter_0
%define b parameter_1
%define operation_type parameter_2
mov rax, 1
cmp operation_type, rax
jne .else_0
mov rax, b
add a, rax
mov rax, a
jmp .end
jmp .endif_0
.else_0:
.endif_0:
mov rax, 2
cmp operation_type, rax
jne .else_1
mov rax, b
sub a, rax
mov rax, a
jmp .end
jmp .endif_1
.else_1:
.endif_1:
mov rax, 3
cmp operation_type, rax
jne .else_2
mov rax, a
imul rax, b
mov a, rax
mov rax, a
jmp .end
jmp .endif_2
.else_2:
.endif_2:
mov rax, 4
cmp operation_type, rax
jne .else_3
mov rax, 0
cmp b, rax
je .else_4
mov rax, a
cqo
mov rbx, b
idiv rbx
mov a, rax
mov rax, a
jmp .end
jmp .endif_4
.else_4:
mov rax, 1
mov division_by_zero_error, rax
jmp .end
.endif_4:
jmp .endif_3
.else_3:
.endif_3:
mov rax, 5
cmp operation_type, rax
jne .else_5
mov rax, 0
cmp b, rax
je .else_6
mov rax, a
cqo
mov rbx, b
idiv rbx
mov a, rdx
mov rax, a
jmp .end
jmp .endif_6
.else_6:
mov rax, 1
mov division_by_zero_error, rax
mov rax, 0
jmp .end
.endif_6:
jmp .endif_5
.else_5:
.endif_5:
mov rax, 1
mov invalid_operation_error, rax
mov rax, 0
jmp .end
.end:
%undef parameter_1
%undef parameter_2
%undef parameter_3
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
mov rdi, a
mov rsi, b
mov rdx, operation_type
call calculate
mov rax, return_value
mov result, rax
mov rax, 1
cmp division_by_zero_error, rax
jne .else_0
mov rdi, divide_by_zero_error_prompt
xor rax, rax
call printf
jmp .endif_0
.else_0:
mov rax, 1
cmp invalid_operation_error, rax
jne .else_1
mov rdi, invalid_operation_error_prompt
xor rax, rax
call printf
jmp .endif_1
.else_1:
mov rdi, result_prompt
xor rax, rax
call printf
mov rdi, result
xor rax, rax
call printf
.endif_1:
.endif_0:
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
