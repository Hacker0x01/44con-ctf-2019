import struct

code = ['']

def HALT():
	code[0] += chr(0)

def SET(n):
	assert 0 <= n <= 255
	code[0] += chr(1) + chr(n)

def GET(n):
	assert 0 <= n <= 255
	code[0] += chr(2) + chr(n)

def DUP():
	code[0] += chr(3)

def DEREF():
	code[0] += chr(4)

def PUSH(n):
	code[0] += chr(5) + struct.pack('<Q', n)

def PUSHI(n):
	code[0] += chr(5) + struct.pack('<q', n)

def SWAP():
	code[0] += chr(6)

def ADD():
	code[0] += chr(7)

def SUB():
	code[0] += chr(8)

def AND():
	code[0] += chr(9)

def OR():
	code[0] += chr(10)

def LSL():
	code[0] += chr(11)

def LSR():
	code[0] += chr(12)

def ASR():
	code[0] += chr(13)

def PRINT():
	code[0] += chr(14)

def LABEL():
	return len(code[0])

def BNZ(label):
	code[0] += chr(15) + struct.pack('<q', label - len(code[0]))

PRINT()
PUSH(15)
SET(0)
jmp = LABEL()
GET(0)
PRINT()
PUSH(3)
GET(0)
SUB()
DUP()
SET(0)
BNZ(jmp)
HALT()

file('/app/code.bin', 'wb').write(code[0])
