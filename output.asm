section .data
fmt_int? db "%lld", 0
fmt_str? db "%s", 0
str$auto0$ db `enter a: `, 0
str$auto1$ db `enter b: `, 0
str$auto2$ db `1 - addition\n`, 0
str$auto3$ db `2 - subtract\n`, 0
str$auto4$ db `3 - multiply\n`, 0
str$auto5$ db `4 - divide\n`, 0
str$auto6$ db `5 - modulus\n`, 0
str$auto7$ db `6 - power\n`, 0
str$auto8$ db `7 - the greatest common divisor (GCD)\n`, 0
str$auto9$ db `8 - the least common multiple (LCM)\n`, 0
str$auto10$ db `enter your choice: `, 0
str$auto11$ db `result: `, 0
str$auto12$ db `\n`, 0
str$auto13$ db `cannot divide by zero\n`, 0
str$auto14$ db `program cannot raise to a negative power\n`, 0
str$auto15$ db `GCD(0, 0) is undefined\n`, 0
str$auto16$ db `invalid operation type\n`, 0
str$auto17$ db `do you want to exit? (1-NO/2-yes): `, 0
str$auto18$ db `invalid choice\n`, 0
section .bss
section .text
global main
extern printf
extern scanf
%define return_value rax
power$:
push rbp
mov rbp, rsp
sub rsp, 32
%define parameter_0 [rbp-8]
mov parameter_0, rdi
%define parameter_1 [rbp-16]
mov parameter_1, rsi
%define a parameter_0
%define b parameter_1
%define counter$ [rbp-24]
mov r15, 0
mov counter$, r15
%define result$ [rbp-32]
mov r15, 1
mov result$, r15
.loop_0:
mov r8, counter$
mov r9, b
cmp r8, r9
jne .else_0
jmp .endloop_0
.else_0:
mov r15, result$
imul r15, a
mov result$, r15
mov r15, 1
add counter$, r15
jmp .loop_0
.endloop_0:
mov rax, result$
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
absolute_value$:
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
mov r15, a
imul r15, -1
mov a, r15
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
Euclidean_algorithm$:
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
mov r15, rax
mov r11, b
mov rax, a
cqo
idiv r11
mov a, rdx
mov rax, r15
mov rdi, b
mov rsi, a
call Euclidean_algorithm$
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
GCD$:
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
call absolute_value$
mov r15, return_value
mov a, r15
mov rdi, b
call absolute_value$
mov r15, return_value
mov b, r15
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
call Euclidean_algorithm$
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
LCM$:
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
call absolute_value$
mov r15, return_value
mov a, r15
mov rdi, b
call absolute_value$
mov r15, return_value
mov b, r15
%define c$ [rbp-24]
mov r15, a
mov c$, r15
mov r15, c$
imul r15, b
mov c$, r15
mov r8, c$
mov r9, 0
cmp r8, r9
jne .else_0
mov rax, 0
jmp .end
.else_0:
mov rdi, a
mov rsi, b
call Euclidean_algorithm$
mov r15, rax
mov r11, return_value
mov rax, c$
cqo
idiv r11
mov c$, rax
mov rax, r15
mov rax, c$
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
calculator$:
push rbp
mov rbp, rsp
sub rsp, 32
%define a$ [rbp-8]
%define b$ [rbp-16]
%define operation_type$ [rbp-24]
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto0$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_int?
lea rsi, a$
xor rax, rax
call scanf
mov rax, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto1$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_int?
lea rsi, b$
xor rax, rax
call scanf
mov rax, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto2$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto3$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto4$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto5$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto6$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto7$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto8$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto9$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto10$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_int?
lea rsi, operation_type$
xor rax, rax
call scanf
mov rax, r15
mov r8, operation_type$
mov r9, 1
cmp r8, r9
jne .else_0
mov r15, b$
add a$, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto11$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_int?
mov rsi, a$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto12$
xor rax, rax
call printf
mov rax, r15
jmp .end
.else_0:
mov r8, operation_type$
mov r9, 2
cmp r8, r9
jne .else_1
mov r15, b$
sub a$, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto11$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_int?
mov rsi, a$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto12$
xor rax, rax
call printf
mov rax, r15
jmp .end
.else_1:
mov r8, operation_type$
mov r9, 3
cmp r8, r9
jne .else_2
mov r15, a$
imul r15, b$
mov a$, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto11$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_int?
mov rsi, a$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto12$
xor rax, rax
call printf
mov rax, r15
jmp .end
.else_2:
mov r8, operation_type$
mov r9, 4
cmp r8, r9
jne .else_3
mov r8, b$
mov r9, 0
cmp r8, r9
je .else_4
mov r15, rax
mov r11, b$
mov rax, a$
cqo
idiv r11
mov a$, rax
mov rax, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto11$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_int?
mov rsi, a$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto12$
xor rax, rax
call printf
mov rax, r15
jmp .end
jmp .endif_4
.else_4:
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto13$
xor rax, rax
call printf
mov rax, r15
jmp .end
.endif_4:
.else_3:
mov r8, operation_type$
mov r9, 5
cmp r8, r9
jne .else_5
mov r8, b$
mov r9, 0
cmp r8, r9
je .else_6
mov r15, rax
mov r11, b$
mov rax, a$
cqo
idiv r11
mov a$, rdx
mov rax, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto11$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_int?
mov rsi, a$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto12$
xor rax, rax
call printf
mov rax, r15
jmp .end
jmp .endif_6
.else_6:
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto13$
xor rax, rax
call printf
mov rax, r15
jmp .end
.endif_6:
.else_5:
mov r8, operation_type$
mov r9, 6
cmp r8, r9
jne .else_7
mov r8, b$
mov r9, 0
cmp r8, r9
jl .else_8
mov rdi, a$
mov rsi, b$
call power$
mov r15, return_value
mov a$, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto11$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_int?
mov rsi, a$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto12$
xor rax, rax
call printf
mov rax, r15
jmp .end
jmp .endif_8
.else_8:
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto14$
xor rax, rax
call printf
mov rax, r15
jmp .end
.endif_8:
.else_7:
mov r8, operation_type$
mov r9, 7
cmp r8, r9
jne .else_9
mov r8, a$
mov r9, 0
cmp r8, r9
jne .else_10
mov r8, b$
mov r9, 0
cmp r8, r9
jne .else_11
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto15$
xor rax, rax
call printf
mov rax, r15
jmp .end
.else_11:
.else_10:
mov rdi, a$
mov rsi, b$
call GCD$
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto11$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_int?
mov rsi, return_value
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto12$
xor rax, rax
call printf
mov rax, r15
jmp .end
.else_9:
mov r8, operation_type$
mov r9, 8
cmp r8, r9
jne .else_12
mov rdi, a$
mov rsi, b$
call LCM$
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto11$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_int?
mov rsi, return_value
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto12$
xor rax, rax
call printf
mov rax, r15
jmp .end
.else_12:
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto16$
xor rax, rax
call printf
mov rax, r15
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
%define exit_choice$ [rbp-8]
.loop_0:
call calculator$
.loop_1:
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto17$
xor rax, rax
call printf
mov rax, r15
mov r15, rax
mov rdi, fmt_int?
lea rsi, exit_choice$
xor rax, rax
call scanf
mov rax, r15
mov r8, exit_choice$
mov r9, 2
cmp r8, r9
jne .else_0
mov rax, 0
jmp .end
jmp .endif_0
.else_0:
mov r8, exit_choice$
mov r9, 1
cmp r8, r9
je .else_1
mov r15, rax
mov rdi, fmt_str?
mov rsi, str$auto18$
xor rax, rax
call printf
mov rax, r15
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
