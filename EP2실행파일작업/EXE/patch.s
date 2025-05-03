.open "EXE/BOOT.BIN", "EBOOT.BIN", 0x8804000-0x80
.psp

/* \xFC 제어코드 Fix (나도 잘 모름 시발) */
//.org 0x0883AF1C
//	addiu	a1,v0,0x0  // 변하지 않게. + 1 --> + 0
.org 0x0883AF28
	nop  // 쓰지 않기

/* 문자 인덱스 계산 변경 */
//.org 0x0883845C
//	sltiu	v0,v1,0xEA  // 0xEA 그대로
	
.org 0x08838468
	sltiu	v0,v1,0xF1

// 버튼 문자 구별
.org 0x08838F48
	lui	v1,0x090A
	ori	v1,0xE420
	jr	v1
	nop

.org 0x090AE420+0x202290
	addiu	v1,a0,-0x51
	sltiu	v1,v1,4
	beq	v1,zero,0x090AE420+(8*4)+0x202290  // 아니라면 돌아가기
	lh	fp,0x0(v0)
	li	v1,0x08839050
	jr	v1
	nop
	
	// 8
	li	v1,0x08838F58
	jr v1
	andi	v1,t0,0xFF
	

.org 0x08838F58
	sltiu	v0,v1,0xF1
	
.org 0x08838FD4
	j	0x08839010  // 강제로 새 로직으로 이동
	
.org 0x08838E38
	j	0x08838F24
	
.org 0x08838F28   // CLUT ID 테이블 사용 Fix
	sltiu	v1,a0,0xF7  // 0xF9 --> 0xF7
	
// 1바이트 열, 행 계산
.org 0x08838F64
	li	v0,41  // 20 -> 41
	div	v1,v0
	mflo	v1  // 나누기
	andi	s2,v1,0xFF  // 행 계산
	nop
	
	// 0x08838F78
	andi	a0,a1,0xFF  // 2번째 바이트
	bltu	t0,0xF1,0x08838F78+(15*4)  // 1바이트 문자일 때 점프
	nop
	andi	a1,t0,0xFF  // 1번째 바이트
	sll	a1,a1,8
	or	a0,a1,a0  // 2바이트 인덱스 완성
	li	t8,0xF016
	sub	a0,a0,t8  // 0xF100 - 0xF016 = 0xEA
	li	t8,0x6EA
	blt	a0,t8,0x08838F78+(15*4)  // 0x6EA 이상이라면 -0x6EA
	nop
	sub a0,a0,t8
	nop
	// 15
	li	s6,0x090AE230
	jalr	s6
	nop
	mfhi	v0  // 나머지 값
	j	0x08838B18
	.word	0x305500FF + 0x1DFF000  // andi	s5,v0,0xFF  // 열 계산
	nop  // 08838FD0
	
.org 0x08839008
	.word 0x0A20E3DE + 0x1DFF000  // j	0x08838F78
	
.org 0x090AE230+0x202290
	bltu	t0,0xA9,0x090AE230+0x202290+(9*4)  // 0xA8까지의 문자 검사
	nop
	li	s6,0xC
	li	s7,0xC
	li	v0,41  // 20 -> 41
	div	a0,v0
	jr	ra
	nop
	
	// 9
	li	t4,0x090AE460  // 테이블 위치
	addu	t4,t4,a0  // 문자 너비 위치 (테이블 위치 + 문자 인덱스)
	lbu	s6,0x00(t4)  // 문자 너비 정의
	li	s7,0xC
	li	v0,41  // 20 -> 41
	div	a0,v0
	jr	ra
	nop
	
	
// 문자 너비 테이블
.org 0x090AE460+0x202290
.byte 12  // ０
.byte 12  // １
.byte 12  // ２
.byte 12  // ３
.byte 12  // ４
.byte 12  // ５
.byte 12  // ６
.byte 12  // ７
.byte 12  // ８
.byte 12  // ９
.byte 12  // 、
.byte 12  // 。
.byte 12  // ＇
.byte 12  // ！
.byte 12  // ？
.byte 12  // 「
.byte 12  // ・
.byte 12  // （
.byte 12  // ）
.byte 12  // ：
.byte 12  // Ａ
.byte 12  // Ｂ
.byte 12  // Ｃ
.byte 12  // Ｄ
.byte 12  // Ｅ
.byte 12  // Ｆ
.byte 12  // Ｇ
.byte 12  // Ｈ
.byte 12  // Ｉ
.byte 12  // Ｊ
.byte 12  // Ｋ
.byte 12  // Ｌ
.byte 12  // Ｍ
.byte 12  // Ｎ
.byte 12  // Ｏ
.byte 12  // Ｐ
.byte 12  // Ｑ
.byte 12  // Ｒ
.byte 12  // Ｓ
.byte 12  // Ｔ
.byte 12  // Ｕ
.byte 12  // Ｖ
.byte 12  // Ｗ
.byte 12  // Ｘ
.byte 12  // Ｙ
.byte 12  // Ｚ
.byte 12  // ａ
.byte 12  // ｂ
.byte 12  // ｃ
.byte 12  // ｄ
.byte 12  // ｅ
.byte 12  // ｆ
.byte 12  // ｇ
.byte 12  // ｈ
.byte 12  // ｉ
.byte 12  // ｊ
.byte 12  // ｋ
.byte 12  // ｌ
.byte 12  // ｍ
.byte 12  // ｎ
.byte 12  // ｏ
.byte 12  // ｐ
.byte 12  // ｑ
.byte 12  // ｒ
.byte 12  // ｓ
.byte 12  // ｔ
.byte 12  // ｕ
.byte 12  // ｖ
.byte 12  // ｗ
.byte 12  // ｘ
.byte 12  // ｙ
.byte 12  // ｚ
.byte 12  // ＆
.byte 12  // ＄
.byte 12  // ￥
.byte 12  // ／
.byte 12  // 　
.byte 12  // 」
.byte 12  // ～
.byte 12  // ー
.byte 6  //  
.byte 12  // ○
.byte 12  // △
.byte 12  // ▽
.byte 12  // □
.byte 12  // “
.byte 12  // －
.byte 12  // ＝
.byte 12  // ÷
.byte 12  // ，
.byte 12  // ”
.byte 12  // ．
.byte 12  // …
.byte 12  // ▷
.byte 12  // ＋
.byte 12  // ％
.byte 12  // ▶
.byte 12  // ×
.byte 7+2  // 0
.byte 3+2  // 1
.byte 7+2  // 2
.byte 7+2  // 3
.byte 8+2  // 4
.byte 7+2  // 5
.byte 7+2  // 6
.byte 7+2  // 7
.byte 7+2  // 8
.byte 7+2  // 9
.byte 2+2  // ,
.byte 2+2  // .
.byte 2+2  // '
.byte 5+2  // "
.byte 1+2  // !
.byte 7+2  // ?
.byte 4+2  // (
.byte 4+2  // )
.byte 2+2  // :
.byte 9+2  // A
.byte 8+2  // B
.byte 8+2  // C
.byte 8+2  // D
.byte 8+2  // E
.byte 8+2  // F
.byte 8+2  // G
.byte 8+2  // H
.byte 1+2  // I
.byte 6+2  // J
.byte 7+2  // K
.byte 8+2  // L
.byte 9+2  // M
.byte 7+2  // N
.byte 8+2  // O
.byte 8+2  // P
.byte 9+2  // Q
.byte 8+2  // R
.byte 8+2  // S
.byte 9+2  // T
.byte 8+2  // U
.byte 9+2  // V
.byte 9+2  // W
.byte 8+2  // X
.byte 7+2  // Y
.byte 8+2  // Z
.byte 6+2  // a
.byte 6+2  // b
.byte 6+2  // c
.byte 6+2  // d
.byte 6+2  // e
.byte 5+2  // f
.byte 6+2  // g
.byte 6+2  // h
.byte 1+2  // i
.byte 4+2  // j
.byte 6+2  // k
.byte 1+2  // l
.byte 7+2  // m
.byte 6+2  // n
.byte 7+2  // o
.byte 6+2  // p
.byte 7+2  // q
.byte 4+2  // r
.byte 6+2  // s
.byte 5+2  // t
.byte 6+2  // u
.byte 5+2  // v
.byte 9+2  // w
.byte 6+2  // x
.byte 5+2  // y
.byte 6+2  // z


// 2바이트 열, 행 계산
.org 0x08839010
	lbu	a1,0x0(t1)  // 2번째 바이트 읽음
	andi	a1,a1,0xFF
	sll	v1,v1,8
	or	v1,v1,a1  // 2바이트 인덱스 완성
	li	t8,0xF016
	sub	v1,v1,t8  // 0xF100 - 0xF016 = 0xEA
	
	// 08839028
	li	t8,0x6EA
	blt	v1,t8,0x0883903C  // 0x6EA 이상이라면 -0x6EA
	nop
	sub v1,v1,t8
	
	// 0x0883903C
	.word	0x34020029 - 0x02201000 + 0x4000000  //li	v0,41  // 20 -> 41
	div	v1,v0
	mflo	v1  // 나누기
	.word	0x0A20E402 - 0x4460  //j	0x08839008  // andi	s2,v0,0xFF 하고 0x08838F8C 으로 점프
	andi	v0,v1,0xFF  // 행 계산
	// 0x08839050
	lui	t9,0x090A
	ori	t9,t9,0xE070
	.word	0x0320F809 - 0x02201000  //jalr	t9
	nop  // 0883905C
	
// 버튼 CLUT ID 조정
.org 0x090AE070+0x202290
	lbu	v0,0x0(t1)
	lh	a0,-0x5D5C(a2)
	addiu	v0,v0,-0x51
	andi	t2,v0,0xFF
	slti	v1,t2,0x4
	movn	fp,a0,v1
	li	t9,0x08838F58
	jr	t9
	andi	v1,t0,0xFF
	nop

// 좌표 불러오기
.org 0x08AA939C
	lui	t9,0x090A
	ori	t9,t9,0xDF90
	jalr	t9
	nop
	nop
	nop
	nop
	nop
	nop
	nop  // 08AA93C0
	
.org 0x090ADF90+0x202290
	lhu	v1,0x3C(v0)
	lw	v0,0x1A6C(a1)
	mult	v0,a2
	mflo	v0
	addu	v0,v0,a0
	lhu	t9,0x40(v0)
	
	li	k1,0x090AE220  // 확인 필요
	lw	k1,0x00(k1)  // 텍스처 주소 읽어오기
	li	at,0x090B0790
	beq	at,k1,0x090ADF90+0x202290+(18*4)  // 폰트라면 점프
	nop
	addu	v1,v1,s1
	andi	v1,v1,0xFFFF
	sh	v1,0xA(t6)  // 끝 좌표 쓰기
	jr   ra
	nop
	
	// 18
	// 12 곱하고 다시 쓰기
	sll	k1,t7,0x1
	addu	k1,k1,t7
	sll	t7,k1,0x2
	sh	t7,0x0(t6)  // 2바이트로 시작 좌표 다시 쓰기 (x)
	
	addu	v1,v1,t7
	andi	v1,v1,0xFFFF
	sh	v1,0xA(t6)  // 끝 좌표 쓰기
	
	sll	k1,t8,0x1
	addu	k1,k1,t8
	sll	t8,k1,0x2
	sh	t8,0x2(t6)  // 2바이트로 시작 좌표 다시 쓰기 (y)
	
	addu	t9,t9,t8
	sh	t9,0xC(t6)  // 끝 좌표 쓰기
	
	// 복귀
	lui	k1,0x08AA
	ori	k1,k1,0x93DC
	jr	k1
	nop
	
	
// 커서 문자 위치 변경
.org 0x0883AB8C  // ▷ 문자 X좌표 설정 (열로 변경)
	li	t7,0x0B  // 0x9C  -- > 0x0B

.org 0x0883AC44  // ▶ 문자 X좌표 설정 (열로 변경)
	li	t7,0x0E  // 0xC0 --> 0x0E
	
.org 0x0883ABE8  // Y좌표 설정 (행으로 변경)
	ori	v1,v1,0x0200  // 0x9000 (0x90) --> 0x0200 (0x02)
	
// ▶ 문자 X, Y좌표 설정 (열, 행으로 변경) 
.org 0x08A3EEB4  // 특수 무기 장착, 개발
	ori	a2,a2,0x020E
	
.org 0x08A426E0  // ?
	ori	a2,a2,0x020E
	
.org 0x0888E670  // 롤의 일기장
	ori	a2,a2,0x020E
	
.org 0x08A9A0E4  // ?
	ori	a2,a2,0x020E


/* 폰트 위치 변경 */
// 폰트 VRAM 위치를 RAM상에서의 위치로
// 0x04128180 --> 0x090B0790
.org 0x08AAAAB4
	lui	t1,0x090A
	ori	t1,t1,0xE030
	jalr	t1
	nop

.org 0x090AE030+0x202290
	sll	s0,s0,0x2
	sw	s4,0x10(sp)
	move	s4,a3
	sw	s3,0xC(sp)

	lui   t1,0x0412
	ori   t1,0x8180   // 비교할 값
	xor  t1,t0,t1  // t0와 비교
	beq  t1,zero,0x090AE030+0x202290+(11*4)  // 일치한다면 이동
	nop
	
	jr   ra
	nop
	
	// 11
	lui   t1,0x090B
	ori   t1,t1,0x0790  // 새로운 주소
	move  t0,t1
	jr   ra
	nop
	
	
/* 텍스처 크기 변경 */
// 텍스처 크기 512x512으로 변경 (폰트만)
.org 0x08AA74B4
	li	v1,0x9
	srav	v0,a0,v1
	andi	v0,v0,0x1  // 0x08AA74BC
	bne	v0,zero,0x08AA74D0
	lui	t8,0x090A
	ori	t8,t8,0xE1B0
	jr	t8
	ori	t8,t8,0xE1F4  // 0x08AA74D0
	jr	t8
	nop  // 08AA74D8
	
.org 0x090AE1B0+0x202290
	li	t9,0x090AE220  // 확인 필요
	sw	t0,0x00(t9)  // 텍스처 주소 작성
	addiu	v1,v1,-0x1
	bgtzl	v1,0x090AE1B0+0x202290+(13*4)
	srav	v0,a0,v1
	
	li	t8,0x090B0790
	beq	t8,t0,0x090AE200+0x202290  // 폰트 처리 중인지 확인
	nop
	
	jr	ra
	move	v0,v1
	nop
	
	// 13
	lui	t8,0x08AA
	ori	t8,t8,0x74BC
	jr	t8
	nop
	
	// 0x090AE1F4
	li	t8,0x090B0790
	li	t9,0x090AE220  // 확인 필요
	beq	t8,t0,0x090AE214+0x202290  // 폰트 처리 중인지 확인
	sw	t0,0x00(t9)  // 텍스처 주소 작성
	jr	ra
	move	v0,v1
	
.org 0x090AE214+0x202290
	jr	ra
	li	v0,0x9  // 512
	
	
/* 텍스트 주소 2바이트에서 4바이트로 변환 */
.org 0x0883ADAC
	lui	t8,0x090A
	ori	t8,t8,0xE0A0
	jr	t8
	nop

.org 0x090AE0A0+0x202290
	li	t9,0xFFFF
	lw	t8,0x00(a2)  // 첫번째 오프셋 읽기
	beq	t8,t9,0x090AE0A0+0x202290+(11*4)  // 첫번째 오프셋이 0xFFFF이라면 4바이트 모드
	nop
	sll	a1,a1,0x1
	addu	a1,a1,a2
	lhu	t0,0x0(a1)
	lui	t8,0x0883
	ori	t8,t8,0xADB8
	jr	t8
	li	v0,-0xF01
	
	// 11
	sll	a1,a1,0x2
	addu	a1,a1,a2
	addiu	a1,a1,4
	lw	t0,0x0(a1)
	lui	t8,0x0883
	ori	t8,t8,0xADB8
	jr	t8
	li	v0,-0xF01


// 다른 것
.org 0x08837CC8
	nop  //sll	a2,a2,0x1
	sw	s5,0x24(sp)
	nop  //addu	a2,a2,a1

.org 0x08837D04
	lui	v0,0x090A
	ori	v0,v0,0xE0F0
	jalr	v0
	nop

.org 0x090AE0F0+0x202290
	li	s1,0xFFFF
	lw	v0,0x0(a1)  // 첫번째 오프셋 읽기
	beq	v0,s1,0x090AE0F0+0x202290+(12*4)  // 첫번째 오프셋이 0xFFFF이라면 4바이트 모드
	nop
	
	// 그대로
	sll	a2,a2,0x1
	addu	a2,a2,a1
	lhu	v0,0x0(a2)
	srl	a2,a0,0x13
	andi	s6,a2,0x7
	addu	a1,a1,v0
	jr	ra
	andi	s1,a0,0x3FF  // s1 복구
	
	// 12
	sll	a2,a2,0x2
	addu	a2,a2,a1
	addiu	a2,a2,4
	lw	v0,0x0(a2)
	srl	a2,a0,0x13
	andi	s6,a2,0x7
	addu	a1,a1,v0
	jr	ra
	andi	s1,a0,0x3FF  // s1 복구
	
	
// 다른 것
.org 0x0883C810
	li	a0,0x090AE150
	jr	a0
	nop
	nop  //	addiu	a0,a0,0x2
	nop  //	sw	a0,0x30(t0)
	jr	ra
	nop
	
.org 0x090AE150+0x202290
	li	at,0xFFFF
	lw	a0,0x0(t1)  // 첫번째 오프셋 읽기
	beq	a0,at,0x090AE150+0x202290+(12*4)
	nop
	
	sll	v1,v1,0x1
	addu	v1,v1,t1
	lhu	a0,0x0(v1)
	addu	a0,a0,t1
	addiu	a0,a0,0x2
	sw	a0,0x30(t0)
	jr	ra
	nop
	
	// 12
	sll	v1,v1,0x2
	addu	v1,v1,t1
	addiu v1,v1,4
	lw	a0,0x0(v1)
	addu	a0,a0,t1
	addi	a0,a0,2
	sw	a0,0x30(t0)
	jr	ra
	nop
	
	
// 다른 것
.org 0x0883C894
	li	v0,0x090AE280
	jr	v0
	nop  //	addiu	v1,v1,0x2
	nop
	jr	ra
	nop  //	sw	v1,0x34(a3)
	
.org 0x090AE280+0x202290
	li	t9,0xFFFF
	lw	v0,0x0(t0)  // 첫번째 오프셋 읽기
	beq	v0,t9,0x090AE280+0x202290+(11*4)
	nop

	sll	v0,a0,0x1
	addu	v0,v0,t0
	lhu	v1,0x0(v0)
	addu	v1,v1,t0
	addiu	v1,v1,0x2
	jr	ra
	sw	v1,0x34(a3)
	
	// 11
	sll	v0,a0,0x2
	addu	v0,v0,t0
	addiu	v0,v0,4
	lw	v1,0x0(v0)
	addu	v1,v1,t0
	addi	v1,v1,2
	jr	ra
	sw	v1,0x34(a3)

// 다른 것
.org 0x0883D8F8
	//sll	v1,v1,0x1
	//addu	v1,v1,a2
	//sw	a0,0x30(a1)
	//lhu	v0,0x0(v1)
	li	v0,0x090AE2D0
	jr	v0
	nop

.org 0x090AE2D0+0x202290
	li	at,0xFFFF
	lw	v0,0x0(a2)  // 첫번째 오프셋 읽기
	beq	v0,at,0x090AE2D0+0x202290+(12*4)
	nop

	sll	v1,v1,0x1
	addu	v1,v1,a2
	sw	a0,0x30(a1)
	lhu	v0,0x0(v1)
	
	li	at,0x0883D908
	jr	at
	nop
	
	// 12
	sll	v1,v1,0x2
	addu	v1,v1,a2
	sw	a0,0x30(a1)
	addiu	v1,v1,4
	lw	v0,0x0(v1)
	li	at,0x0883D908
	jr	at
	nop
	
// 다른 것
.org 0x0883D948
	li	v0,0x090AE330
	jr	v0
	nop
	nop
	nop
	
.org 0x090AE330+0x202290
	li	t0,0xFFFF
	lw	v0,0x0(a1)  // 첫번째 오프셋 읽기
	beq	v0,t0,0x090AE330+0x202290+(10*4)
	nop

	sll	v1,v1,0x1
	addu	v1,v1,a1
	lhu	v0,0x0(v1)
	addu	v0,v0,a1
	jr	ra
	sw	v0,0x34(a0)
	
	// 10
	sll	v1,v1,0x2
	addu	v1,v1,a1
	addiu	v1,v1,4
	lw	v0,0x0(v1)
	addu	v0,v0,a1
	jr	ra
	sw	v0,0x34(a0)
	
// 다른 것
.org 0x0883C5FC
	li	a0,0x090AE380
	jr	a0
	nop
	nop
	nop
	nop
	
.org 0x090AE380+0x202290
	li	at,0xFFFF
	lw	a0,0x0(t1)  // 첫번째 오프셋 읽기
	beq	a0,at,0x090AE380+0x202290+(11*4)
	nop

	sll	v1,v1,0x1
	addu	v1,v1,t1
	lhu	a0,0x0(v1)
	addu	a0,a0,t1
	sw	a0,0x30(t0)
	jr	ra
	nop	
	
	// 11
	sll	v1,v1,0x2
	addu	v1,v1,t1
	addiu	v1,v1,4
	lw	a0,0x0(v1)
	addu	a0,a0,t1
	sw	a0,0x30(t0)
	jr	ra
	nop	
	
// 다른 것
.org 0x0883C650
	li	v1,0x090AE3D0
	jr v1
	nop
	nop
	nop
	
.org 0x090AE3D0+0x202290
	li	t0,0xFFFF
	lw	v1,0x0(a3)  // 첫번째 오프셋 읽기
	beq	v1,t0,0x090AE3D0+0x202290+(10*4)
	nop

	sll	v0,v0,0x1
	addu	v0,v0,a3
	lhu	v1,0x0(v0)
	addu	v1,v1,a3
	jr	ra
	sw	v1,0x34(a0)
	
	// 10
	sll	v0,v0,0x2
	addu	v0,v0,a3
	addiu	v0,v0,4
	lw	v1,0x0(v0)
	addu	v1,v1,a3
	jr	ra
	sw	v1,0x34(a0)


/* 미션, 스타트, 컴플리트 텍스처 맵핑 변경 */
.org 0x08AE927C+0x202290
	.db 0xE8, 0x00, 0x80, 0x0A, 0x00, 0xFD, 0x98, 0x01, 0x00, 0x00, 0x16, 0x00, 0xF0, 0x00, 0x00, 0x0B, 0x00, 0xFE, 0x98, 0x01, 0x00, 0x00, 0x17, 0x00, 0xF8, 0x00, 0x80, 0x0B, 0x00, 0xFF, 0x98, 0x01, 0x00, 0x00, 0x00, 0x00, 0x80, 0x00, 0x00, 0x08, 0x00, 0xE8, 0x13, 0x18, 0x13, 0x00, 0x00, 0x00, 0xA0, 0x00, 0x00, 0x0A, 0x13, 0xE8, 0x06, 0x18, 0x19, 0x00, 0x00, 0x00, 0xC0, 0x00, 0x00, 0x0C, 0x19, 0xE8, 0x16, 0x18, 0x2F, 0x00, 0x00, 0x00, 0xE0, 0x00, 0x00, 0x0E, 0x2F, 0xE8, 0x06, 0x18, 0x35, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x35, 0xE8, 0x1E, 0x18, 0x58, 0x00, 0x00, 0x00, 0x20, 0x01, 0x00, 0x02, 0x58, 0xE8, 0x0D, 0x18, 0x65, 0x00, 0x00, 0x00, 0x40, 0x01, 0x00, 0x04, 0x65, 0xE8, 0x19, 0x18, 0x7E, 0x00, 0x00, 0x00, 0x60, 0x01, 0x00, 0x06, 0x7E, 0xE8, 0x0C, 0x18, 0x8A, 0x00, 0x00, 0x00, 0x80, 0x01, 0x00, 0x08, 0x8A, 0xE8, 0x0C, 0x18, 0x00, 0x00, 0x00, 0x00, 0x80, 0x00, 0x00, 0x08, 0x00, 0xE8, 0x13, 0x18, 0x13, 0x00, 0x00, 0x00, 0xA0, 0x00, 0x00, 0x0A, 0x13, 0xE8, 0x06, 0x18, 0x19, 0x00, 0x00, 0x00, 0xC0, 0x00, 0x00, 0x0C, 0x19, 0xE8, 0x16, 0x18, 0x2F, 0x00, 0x00, 0x00, 0xE0, 0x00, 0x00, 0x0E, 0x2F, 0xE8, 0x06, 0x18, 0x35, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x35, 0xE8, 0x1E, 0x18, 0x58, 0x00, 0x00, 0x00, 0x20, 0x01, 0x00, 0x02, 0x98, 0xE8, 0x0D, 0x18, 0x65, 0x00, 0x00, 0x00, 0x40, 0x01, 0x00, 0x04, 0xA5, 0xE8, 0x10, 0x18, 0x75, 0x00, 0x00, 0x00, 0x60, 0x01, 0x00, 0x06, 0xB5, 0xE8, 0x13, 0x18, 0x88, 0x00, 0x00, 0x00, 0x80, 0x01, 0x00, 0x08, 0xC8, 0xE8, 0x15, 0x18, 0x9D, 0x00, 0x00, 0x00, 0xA0, 0x01, 0x00, 0x0A, 0xDD, 0xE8, 0x0A, 0x18, 0xA7, 0x00, 0x00, 0x00, 0xC0, 0x01, 0x00, 0x0C, 0xE7, 0xE8, 0x16, 0x18

/* 롤러보드 경주 이름과 시간 */
.org 0x08844E88
	lui	t1,0xF50F  // 사
.org 0x08844EDC
	ori	t1,t1,0xF406  // 못
.org 0x08844EE8
	li	t2,0x4C  // 　
	
// ” 문자 Fix
.org 0x0883CACC
	li	v0,0xFA  // 0xF8 --> 0xFA
.org 0x0883CAE4
	li	v0,0x7C  // 0x1E --> 0x7C
	
// 이름 입력 Fix
.org 0x08AEA370+0x202290
	.db 0x14, 0x00, 0x15, 0x00, 0x16, 0x00, 0x17, 0x00, 0x18, 0x00, 0x19, 0x00, 0x1A, 0x00, 0x1B, 0x00, 0x1C, 0x00, 0x1D, 0x00, 0x1E, 0x00, 0x1F, 0x00, 0x20, 0x00, 0x21, 0x00, 0x22, 0x00, 0x23, 0x00, 0x24, 0x00, 0x25, 0x00, 0x26, 0x00, 0x27, 0x00, 0x28, 0x00, 0x29, 0x00, 0x2A, 0x00, 0x2B, 0x00, 0x2C, 0x00, 0x2D, 0x00, 0x00, 0x00, 0x01, 0x00, 0x02, 0x00, 0x03, 0x00, 0x04, 0x00, 0x05, 0x00, 0x06, 0x00, 0x07, 0x00, 0x08, 0x00, 0x09, 0x00, 0x0C, 0x00, 0x0D, 0x00, 0x0E, 0x00, 0x10, 0x00, 0x13, 0x00, 0x4F, 0x00, 0x5B, 0x00, 0x4C, 0x00

.close
