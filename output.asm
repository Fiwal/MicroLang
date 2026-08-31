section .data
fmt_int? db "%lld", 0
num_prompt_1 db `enter a: `, 0
num_prompt_2 db `enter b: `, 0
operation_type_prompt db `1 - addition\n2 - subtract\n3 - multiply\n4 - divide\n5 - modulus\n6 - power\n7 - the greatest common divisor (GCD)\n8 - the leparsed_program common multiple (LCM)\nenter your choice: `, 0
result_prompt db `result: `, 0
exit_prompt db `do you want to exit? (1-NO/2-yes): `, 0
invalid_operation_error_prompt db `invalid operation type\n`, 0
divide_by_zero_error_prompt db `cannot divide by zero\n`, 0
power_error_prompt db `parsed_program cannot raise to a negative power\n`, 0
invalid_choice_prompt db `invalid choice\n`, 0
gcd_error_prompt db `GCD(0, 0) is undefined\n`, 0
new_line db `\n`, 0
section .bss
section .text
global main
extern printf
extern scanf
%define return_value rax
print_result:
push rbp
mov rbp, rsp
sub rsp, 16
%define parameter_0 [rbp-8]
mov parameter_0, rdi
mov rdi, result_prompt
xor rax, rax
call printf
mov rdi, fmt_int?
mov rsi, parameter_0
xor rax, rax
call printf
mov rdi, new_line
xor rax, rax
call printf
.end:
%undef parameter_0
mov rsp, rbp
pop rbp
ret
power:
push rbp
mov rbp, rsp
sub rsp, 32
%define parameter_0 [rbp-8]
mov parameter_0, rdi
%define parameter_1 [rbp-16]
mov parameter_1, rsi
%define a parameter_0
%define b parameter_1
%define counter [rbp-24]
mov rax, 0
mov counter, rax
%define result [rbp-32]
mov rax, 1
mov result, rax
.loop_0:
mov r8, counter
mov r9, b
cmp r8, r9
jne .else_0
jmp .endloop_0
.else_0:
mov rax, result
imul rax, a
mov result, rax
mov rax, 1
add counter, rax
jmp .loop_0
.endloop_0:
mov rax, result
jmp .end
.end:
%undef parameter_0
%undef parameter_1
%undef counter
%undef result
%undef a
%undef b
mov rsp, rbp
pop rbp
ret
absolute_value:
push rbp
mov rbp, rsp
sub rsp, 16
%define parameter_0 [rbp-8]
mov parameter_0, rdi
%define a parameter_0
mov r8, a
mov r9, 0
cmp r8, r9
jge .else_0
mov rax, a
imul rax, -1
mov a, rax
mov rax, a
jmp .end
.else_0:
mov rax, a
jmp .end
.end:
%undef parameter_0
%undef a
mov rsp, rbp
pop rbp
ret
Euclidean_algorithm:
push rbp
mov rbp, rsp
sub rsp, 16
%define parameter_0 [rbp-8]
mov parameter_0, rdi
%define parameter_1 [rbp-16]
mov parameter_1, rsi
%define a parameter_0
%define b parameter_1
mov r8, b
mov r9, 0
cmp r8, r9
je .else_0
mov r11, b
mov rax, a
cqo
idiv r11
mov a, rdx
mov rdi, b
mov rsi, a
call 53
mov rax, return_value
jmp .end
.else_0:
mov rax, a
jmp .end
.end:
%undef parameter_0
%undef parameter_1
%undef a
%undef b
mov rsp, rbp
pop rbp
ret
GCD:
push rbp
mov rbp, rsp
sub rsp, 16
%define parameter_0 [rbp-8]
mov parameter_0, rdi
%define parameter_1 [rbp-16]
mov parameter_1, rsi
%define a parameter_0
%define b parameter_1
mov rdi, a
call 64
mov rax, return_value
mov a, rax
mov rdi, b
call 67
mov rax, return_value
mov b, rax
mov r8, a
mov r9, 0
cmp r8, r9
jne .else_0
mov rax, b
jmp .end
.else_0:
mov r8, b
mov r9, 0
cmp r8, r9
jne .else_1
mov rax, a
jmp .end
.else_1:
mov rdi, a
mov rsi, b
call 78
mov rax, return_value
jmp .end
.end:
%undef parameter_0
%undef parameter_1
%undef a
%undef b
mov rsp, rbp
pop rbp
ret
LCM:
push rbp
mov rbp, rsp
sub rsp, 32
%define parameter_0 [rbp-8]
mov parameter_0, rdi
%define parameter_1 [rbp-16]
mov parameter_1, rsi
%define a parameter_0
%define b parameter_1
mov rdi, a
call 86
mov rax, return_value
mov a, rax
mov rdi, b
call 89
mov rax, return_value
mov b, rax
%define c [rbp-24]
mov rax, a
mov c, rax
mov rax, c
imul rax, b
mov c, rax
mov r8, c
mov r9, 0
cmp r8, r9
jne .else_0
mov rax, 0
jmp .end
.else_0:
mov rdi, a
mov rsi, b
call 98
mov r11, return_value
mov rax, c
cqo
idiv r11
mov c, rax
mov rax, c
jmp .end
.end:
%undef parameter_0
%undef parameter_1
%undef c
%undef a
%undef b
mov rsp, rbp
pop rbp
ret
calculator:
push rbp
mov rbp, rsp
sub rsp, 32
%define a [rbp-8]
%define b [rbp-16]
%define operation_type [rbp-24]
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
mov r8, operation_type
mov r9, 1
cmp r8, r9
jne .else_0
mov rax, b
add a, rax
mov rdi, a
call 118
jmp .end
.else_0:
mov r8, operation_type
mov r9, 2
cmp r8, r9
jne .else_1
mov rax, b
sub a, rax
mov rdi, a
call 124
jmp .end
.else_1:
mov r8, operation_type
mov r9, 3
cmp r8, r9
jne .else_2
mov rax, a
imul rax, b
mov a, rax
mov rdi, a
call 130
jmp .end
.else_2:
mov r8, operation_type
mov r9, 4
cmp r8, r9
jne .else_3
mov r8, b
mov r9, 0
cmp r8, r9
je .else_4
mov r11, b
mov rax, a
cqo
idiv r11
mov a, rax
mov rdi, a
call 137
jmp .end
jmp .endif_4
.else_4:
mov rdi, divide_by_zero_error_prompt
xor rax, rax
call printf
jmp .end
.endif_4:
.else_3:
mov r8, operation_type
mov r9, 5
cmp r8, r9
jne .else_5
mov r8, b
mov r9, 0
cmp r8, r9
je .else_6
mov r11, b
mov rax, a
cqo
idiv r11
mov a, rdx
mov rdi, a
call 148
jmp .end
jmp .endif_6
.else_6:
mov rdi, divide_by_zero_error_prompt
xor rax, rax
call printf
jmp .end
.endif_6:
.else_5:
mov r8, operation_type
mov r9, 6
cmp r8, r9
jne .else_7
mov r8, b
mov r9, 0
cmp r8, r9
jl .else_8
mov rdi, a
mov rsi, b
call 158
mov rax, return_value
mov a, rax
mov rdi, a
call 160
jmp .end
jmp .endif_8
.else_8:
mov rdi, power_error_prompt
xor rax, rax
call printf
jmp .end
.endif_8:
.else_7:
mov r8, operation_type
mov r9, 7
cmp r8, r9
jne .else_9
mov r8, a
mov r9, 0
cmp r8, r9
jne .else_10
mov r8, b
mov r9, 0
cmp r8, r9
jne .else_11
mov rdi, gcd_error_prompt
xor rax, rax
call printf
jmp .end
.else_11:
.else_10:
mov rdi, a
mov rsi, b
call 176
mov rdi, fmt_int?
mov rsi, return_value
xor rax, rax
call printf
jmp .end
.else_9:
mov r8, operation_type
mov r9, 8
cmp r8, r9
jne .else_12
mov rdi, a
mov rsi, b
call 182
mov rax, return_value
mov a, rax
mov rdi, a
call 184
jmp .end
.else_12:
mov rdi, invalid_operation_error_prompt
xor rax, rax
call printf
.end:
%undef a
%undef b
%undef operation_type
mov rsp, rbp
pop rbp
ret
main:
push rbp
mov rbp, rsp
sub rsp, 16
%define exit_choice [rbp-8]
.loop_0:
call 195
.loop_1:
mov rdi, exit_prompt
xor rax, rax
call printf
mov rdi, fmt_int?
lea rsi, exit_choice
xor rax, rax
call scanf
mov r8, exit_choice
mov r9, 2
cmp r8, r9
jne .else_0
mov rax, 0
jmp .end
jmp .endif_0
.else_0:
mov r8, exit_choice
mov r9, 1
cmp r8, r9
je .else_1
mov rdi, invalid_choice_prompt
xor rax, rax
call printf
jmp .endif_1
.else_1:
jmp .endloop_1
.endif_1:
.endif_0:
jmp .loop_1
.endloop_1:
jmp .loop_0
.endloop_0:
mov rax, 0
jmp .end
.end:
%undef exit_choice
mov rsp, rbp
pop rbp
ret
