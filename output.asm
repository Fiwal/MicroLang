section .data
fmt_int? db "%lld", 0
num_prompt_1 db `enter a: `, 0
num_prompt_2 db `enter b: `, 0
operation_type_prompt db `1 - addition\n2 - subtract\n3 - multiply\n4 - divide\n5 - modulus\n6 - power\nenter your choice: `, 0
result_prompt db `result: `, 0
exit_prompt db `do you want to exit? (1-NO/2-yes): `, 0
invalid_operation_error_prompt db `invalid operation type\n`, 0
divide_by_zero_error_prompt db `cannot divide by zero\n`, 0
power_error_prompt db `program cannot raise to a negative power\n`, 0
invalid_choice_prompt db `invalid choice\n`, 0
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
mov rax, b
cmp counter, rax
jne .else_0
jmp .endloop_0
jmp .endif_0
.else_0:
.endif_0:
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
mov rax, 1
cmp operation_type, rax
jne .else_0
mov rax, b
add a, rax
mov rdi, a
call print_result
jmp .end
jmp .endif_0
.else_0:
.endif_0:
mov rax, 2
cmp operation_type, rax
jne .else_1
mov rax, b
sub a, rax
mov rdi, a
call print_result
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
mov rdi, a
call print_result
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
mov r11, b
idiv r11
mov a, rax
mov rdi, a
call print_result
jmp .end
jmp .endif_4
.else_4:
mov rdi, divide_by_zero_error_prompt
xor rax, rax
call printf
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
mov r11, b
idiv r11
mov a, rdx
mov rdi, a
call print_result
jmp .end
jmp .endif_6
.else_6:
mov rdi, divide_by_zero_error_prompt
xor rax, rax
call printf
jmp .end
.endif_6:
jmp .endif_5
.else_5:
.endif_5:
mov rax, 6
cmp operation_type, rax
jne .else_7
mov rax, 0
cmp b, rax
jl .else_8
mov rdi, a
mov rsi, b
call power
mov rax, return_value
mov a, rax
mov rdi, a
call print_result
jmp .end
jmp .endif_8
.else_8:
mov rdi, power_error_prompt
xor rax, rax
call printf
jmp .end
.endif_8:
jmp .endif_7
.else_7:
.endif_7:
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
%define run [rbp-16]
mov rax, 1
mov run, rax
.loop_0:
mov rax, 0
cmp run, rax
jne .else_0
jmp .endloop_0
jmp .endif_0
.else_0:
.endif_0:
call calculator
.loop_1:
mov rdi, exit_prompt
xor rax, rax
call printf
mov rdi, fmt_int?
lea rsi, exit_choice
xor rax, rax
call scanf
mov rax, 2
cmp exit_choice, rax
jne .else_1
mov rax, 0
mov run, rax
jmp .endloop_1
jmp .endif_1
.else_1:
mov rax, 1
cmp exit_choice, rax
je .else_2
mov rdi, invalid_choice_prompt
xor rax, rax
call printf
jmp .endif_2
.else_2:
jmp .endloop_1
.endif_2:
.endif_1:
jmp .loop_1
.endloop_1:
jmp .loop_0
.endloop_0:
mov rax, 0
jmp .end
.end:
%undef exit_choice
%undef run
mov rsp, rbp
pop rbp
ret
