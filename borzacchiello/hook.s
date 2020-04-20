.globl __hook_0
.globl __hook_1


.section .text

__hook_0:
  push %rax
  push %rbx
  push %rcx
  push %rdx
  push %rbp
  push %rdi
  push %rsi
  push %r8
  push %r9
  push %r10
  push %r11
  push %r12
  push %r13
  push %r14
  push %r15
  movq 120(%rsp), %rdi
  call pltcov_log@plt
  pop %r15
  pop %r14
  pop %r13
  pop %r12
  pop %r11
  pop %r10
  pop %r9
  pop %r8
  pop %rsi
  pop %rdi
  pop %rbp
  pop %rdx
  pop %rcx
  pop %rbx
  pop %rax
  jmp puts@plt

__hook_1:
  push %rax
  push %rbx
  push %rcx
  push %rdx
  push %rbp
  push %rdi
  push %rsi
  push %r8
  push %r9
  push %r10
  push %r11
  push %r12
  push %r13
  push %r14
  push %r15
  movq 120(%rsp), %rdi
  call pltcov_log@plt
  pop %r15
  pop %r14
  pop %r13
  pop %r12
  pop %r11
  pop %r10
  pop %r9
  pop %r8
  pop %rsi
  pop %rdi
  pop %rbp
  pop %rdx
  pop %rcx
  pop %rbx
  pop %rax
  jmp __cxa_finalize@plt

