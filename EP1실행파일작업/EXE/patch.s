.open "EXE/dash2e1.prx", "dash2e1.prx", 0x091B2000-0x80
.psp

.org 0x091DD984
	//sll	a1,a1,0x1
	//addu	a1,a1,v1
	//lhu	v0,0x0(a1)
	//addu	v1,v1,v0
	li	v0,0x096F8DA0
	jr	v0
	nop


.org 0x096F8DA0+0xCF560
	li	t0,0xFFFF
	lw	t1,0x00(v1)  // 첫번째 오프셋 읽기
	beq	t1,t0,0x096F8DA0+0xCF560+(11*4)
	nop
	sll	a1,a1,0x1
	addu	a1,a1,v1
	lhu	v0,0x0(a1)
	li	t1,0x091DD994
	jr	t1
	addu	v1,v1,v0
	
	// 11
	sll	a1,a1,0x2
	addu	a1,a1,v1
	addiu	a1,a1,4
	lw	v0,0x0(a1)
	li	t1,0x091DD994
	jr	t1
	addu	v1,v1,v0

// 다른 거
.org 0x091DB080
	//addu	a2,a2,a1
	nop

.org 0x091DB0C4
	li	v0,0x096F8DF0
	jr	v0
	nop
	
.org 0x096F8DF0+0xCF560
	li	at,0xFFFF
	lw	v0,0x00(a1)  // 첫번째 오프셋 읽기
	beq	v0,at,0x096F8DF0+0xCF560+(12*4)
	nop
	
	addu	a2,a2,a1
	lhu	v0,0x0(a2)
	sw	v1,0x4(sp)
	li	a2,0xFE
	li	at,0x091DB0D4
	jr	at
	addu	s1,a1,v0
	
	// 12
	sll	a2,a2,0x1  // 한 번 더
	addu	a2,a2,a1
	addiu	a2,a2,4
	lw	v0,0x0(a2)
	sw	v1,0x4(sp)
	li	a2,0xFE
	li	at,0x091DB0D4
	jr	at
	addu	s1,a1,v0

// 다른 거
.org 0x091DEBB8
	li	v0,0x096F8E50
	jr	v0
	nop
	nop
	jr	ra
	nop

.org 0x096F8E50+0xCF560
	li	at,0xFFFF
	lw	v0,0x00(a3)  // 첫번째 오프셋 읽기
	beq	v0,at,0x096F8E50+0xCF560+(11*4)
	nop
	
	sll	v0,a0,0x1
	addu	v0,v0,a3
	lhu	v1,0x0(v0)
	addu	v1,v1,a3
	addiu	v1,v1,0x2
	jr	ra
	sw	v1,0x34(a2)
	
	// 11
	sll	v0,a0,0x2
	addu	v0,v0,a3
	addiu	v0,v0,4
	lw	v1,0x0(v0)
	addu	v1,v1,a3
	addi	v1,v1,0x2
	jr	ra
	sw	v1,0x34(a2)
	
// 버튼
.org 0x091DEB3C
	li	v1,0x096F8EA0
	jr	v1
	nop
	
.org 0x096F8EA0+0xCF560
	li	at,0xFFFF
	lw	v1,0x00(t0)  // 첫번째 오프셋 읽기
	beq	v1,at,0x096F8EA0+0xCF560+(11*4)
	nop

	sll	v1,a1,0x1
	addu	v1,v1,t0
	lhu	a0,0x0(v1)
	li	at,0x091DEB4C
	jr	at
	addu	a0,a0,t0
	
	// 11
	sll	v1,a1,0x2
	addu	v1,v1,t0
	addiu	v1,v1,4
	lw	a0,0x0(v1)
	li	at,0x091DEB4C
	jr	at
	addu	a0,a0,t0
	

.close
