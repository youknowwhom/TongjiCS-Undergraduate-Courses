.data
	A:.space 240
	B:.space 240
    C:.space 240
    D:.space 240
    E:.space 240

.text
    j main
    exc:
    nop
    j exc

main:
    addi $2, $0, 0      # a[i]
    addi $3, $0, 1      # b[i]
    addi $4, $0, 0      # c[i]
    addi $13, $0, 0     # d[i]
    addi $5, $0, 4      # 计数器，每次+4
    addi $6, $0, 0      # a[i - 1]
    addi $7, $0, 1      # b[i - 1]
    addi $10, $0, 0     # 分段区间标识
    addi $11, $0, 240   # 存放数组总长
    addi $14, $0, 3     # 存放常数3

    addi $30, $0, 0
    lui $27, 0x0000
    addu $27, $27, $0
    sw $2, A($27)

    lui $27, 0x0000
    addu $27, $27, $0
    sw $2, B($27)

    addi $31, $31, 1
    lui $27, 0x0000
    addu $27, $27, $0
    sw $3, D($27)

loop:
    # 计算A的值
    srl $12, $5, 2
    add $6, $6, $12

    lui $27, 0x0000
    addu $27, $27, $5
    sw $6, A($27)

    # 计算B的值
    mul $15, $14, $12

    add $7, $7, $15
    lui $27, 0x0000
    addu $27, $27, $5
    sw $7, B($27)

    slti $10, $5, 80
    bne $10, 1, c1

    lui $27, 0x0000
    addu $27, $27, $5
    sw $7, D($27)

    # 本次的值转存记录上一次
    addi $15, $6, 0
    addi $16, $7, 0
    j endc
c1:
    slti $10, $5, 160
    addi $27, $0, 1
    bne $10, $27, c2

    add $15, $6, $7     # c[i] = a[i] + b[i]
    lui $27, 0x0000
    addu $27, $27, $5
    sw $15, C($27)

    mul $16, $15, $6    # d[i] = a[i] * b[i]
    lui $27, 0x0000
    addu $27, $27, $5
    sw $16, D($27)

    j endc

c2:
    mul $15, $6, $7     # c[i] = a[i] * b[i]
    lui $27, 0x0000
    addu $27, $27, $5
    sw $15, C($27)

    mul $16, $15, $7    # d[i] = c[i] * b[i]
    lui $27, 0x0000
    addu $27, $27, $5
    sw $16, D($27)

endc:
    add $28, $15, $16
    lui $27, 0x0000
    addu $27, $27, $5
    sw $28, E($27)
    addiu $5, $5, 4
    bne $5, $11, loop