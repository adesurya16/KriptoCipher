import sys
import random
# file input
# nameOfFile = input("Input nama file : ")
def inputFile(nameOfFile): 
	lineString = open(nameOfFile,'r').readline()
	print(lineString)
	return lineString

# get ascii number from charachter
def getAsciiNumber(ch):
	return ord(ch)

# get charachter from ascii number
def getChar(number):
	return chr(number)

# lowercase
def lower(str):
	return str.lower()

# uppercase
def upper(str):
	return str.upper()

# last element deleted
def getStringExcpLastElment(str):
	return str[0:len(str)-1]

# output to file string param
def outputFile(strOut,nameOfFile):
	file = open(nameOfFile,"w")
	file.write(strOut)
	file.close()

# plaintext as column
# key as row
def generateMatrixVigenere(length):
	mat = []
	for i in range(length):
		mat.append([])
		for j in range(length):
			mat[i].append((i + j ) % length)
	return mat

# is Alphabet
def isAlphabet(ch):
	return (ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z') 

# delete no Alphabet Char
def deleteAllCharNonAlphabet(str):
	for i in range(256):
		if not isAlphabet(getChar(i)):
			str = str.replace(getChar(i),"")
	return str

# matrix 6x6 , mat[5][5] = null
# except1 A,B,C,....
def generateMatrixKeyPlayfair(except1 = 'J'):
	# choose random swap
	mat = []
	save = list(range(26))
	random.shuffle(save)
	save.remove(getAsciiNumber(except1) - getAsciiNumber('A'))
	k = 0
	for i in range(5):
		mat.append([])
		for j in range(5):
			# rand
			mat[i].append(save[k])
			k = k + 1
	
	# add last row in matrix
	first = mat[0]
	mat.append(first)

	# add last column
	for i in range(5):
		x = mat[i][0]
		mat[i].append(x)
	return mat

# bigram string (list of tuple) A
def chageStringToBigram(str,separator = 'Z'):
	list = []
	tp1 = ''
	tp2 = ''
	for ch in str:
		if isAlphabet(ch):
			if tp1 == '':
				tp1 = upper(ch)
			elif tp2 == '':
				tp2 = upper(ch);
				if tp1 == tp2:
					list.append((tp1,separator))
					tp1, tp2 = tp2, ''
				else :
					list.append((tp1,tp2))
					tp1, tp2 = '', ''
	if tp1 != '':
		list.append((tp1,separator))
	return list

# asumsion cipher A , plain a (covert)
# for matrix Cipher Vigenere 26 return charachter encrypt
# ch alphabet
# key alphabet
def cipherTextVCAlpha(matVC,ch,key):
	return getChar(matVC[getAsciiNumber(lower(key))-getAsciiNumber('a')][getAsciiNumber(lower(ch))-getAsciiNumber('a')] + getAsciiNumber('A'))

# for matrix Cipher Vigenere 256 return charachter encrypt
# ch alphabet
# key alphabet
def cipherTextVCAscii(matVC,ch,key):
	return getChar(matVC[getAsciiNumber(key)][getAsciiNumber(ch)])


# decrypt
def cipherTextVCAlphaDec(matVC,cipher,key):
	return getChar(matVC[getAsciiNumber(lower(key))-getAsciiNumber('a')].index(getAsciiNumber(cipher)-getAsciiNumber('A')) + getAsciiNumber('a'))

# decrypt
def cipherTextVCAsciiDec(matVC,cipher,key):
	return getChar(matVC[getAsciiNumber(key)].index(getAsciiNumber(cipher)))

# no "space" char exisiting in str
def print5char(str):
	start = 0
	while start+5 < len(str):
		print(str[start:start+5],end=" ")
		start+=5
	print(str[start:len(str)])

# encrypt in play fair
def cipherTextPlayFair(matPF,tupleCH):
	found1 = ()
	found2 = ()
	f1 = getAsciiNumber(tupleCH[0]) - getAsciiNumber('A')
	f2 = getAsciiNumber(tupleCH[1]) - getAsciiNumber('A')
	for i in range(len(matPF)-1):
		if f1 in matPF[i] and all(found1):
			found1 = (i,matPF[i].index(f1))
		if f2 in matPF[i] and all(found2):
			found2 = (i,matPF[i].index(f2))
	# get location tuple found
	# encrypt
	if found1[0] == found2[0]:
		return (getChar(matPF[found1[0]][found1[1]+1] + getAsciiNumber('A')),getChar(matPF[found2[0]][found2[1]+1] + getAsciiNumber('A'))) 
	elif found1[1] == found2[1]:
		return (getChar(matPF[found1[0]+1][found1[1]] + getAsciiNumber('A')),getChar(matPF[found2[0]+1][found2[1]] + getAsciiNumber('A'))) 
	else:
		return (getChar(matPF[found1[0]][found2[1]] + getAsciiNumber('A')),getChar(matPF[found2[0]][found1[1]] + getAsciiNumber('A')))

# decrypt
def cipherTextPlayFairDec(matPF,cipher):
	found1 = ()
	found2 = ()
	f1 = getAsciiNumber(cipher[0]) - getAsciiNumber('A')
	f2 = getAsciiNumber(cipher[1]) - getAsciiNumber('A')
	for i in range(len(matPF)-1):
		if f1 in matPF[i] and all(found1):
			idx = matPF[i].index(f1)
			if idx == 0:
				idx = 5
			if i == 0:
				i = 5
			found1 = (i,idx)
		if f2 in matPF[i] and all(found2):
			idx = matPF[i].index(f2)
			if idx == 0:
				idx = 5
			if i == 0:
				i = 5
			found2 = (i,idx)
	# get location tuple found
	# decrypt
	if found1[0] == found2[0]:
		return (getChar(matPF[found1[0]][found1[1]-1] + getAsciiNumber('A')),getChar(matPF[found2[0]][found2[1]-1] + getAsciiNumber('A'))) 
	elif found1[1] == found2[1]:
		return (getChar(matPF[found1[0]-1][found1[1]] + getAsciiNumber('A')),getChar(matPF[found2[0]-1][found2[1]] + getAsciiNumber('A'))) 
	else:
		# print(getChar(matPF[found1[1]][found2[0]] + getAsciiNumber('A')),getChar(matPF[found2[1]][found1[0]] + getAsciiNumber('A')))
		return (getChar(matPF[found1[0]][found2[1]] + getAsciiNumber('A')),getChar(matPF[found2[0]][found1[1]] + getAsciiNumber('A')))

def prosesEncrpytVC(key,str,op):
	# karena algo vc biasa key matrix pasti sama
	res = []
	mat = generateMatrixVigenere(op)
	if op == 26:
		key = deleteAllCharNonAlphabet(key)
		start1 = 0
		start2 = 0
		lenKey = len(key)
		while start1 < len(str):
			if isAlphabet(str[start1]):
				res.append(cipherTextVCAlpha(mat,lower(str[start1]),key[start2 % lenKey]))
				start2+=1
			else:
				res.append(str[start1])
			start1+=1

	elif op == 256:
		start1 = 0
		start2 = 0
		lenKey = len(key)
		while start < len(str):
			res.append(cipherTextVCAscii(mat,lower(str[start1]),key[start2 % lenKey]))
			start2+=1
			start1+=1
	return "".join(res)

def prosesDecryptVC(key,cipher,op):
	# karena algo vc biasa key matrix pasti sama
	res = []
	mat = generateMatrixVigenere(op)
	if op == 26:
		key = deleteAllCharNonAlphabet(key)
		start1 = 0
		start2 = 0
		lenKey = len(key)
		while start1 < len(cipher):
			if isAlphabet(cipher[start1]):
				res.append(cipherTextVCAlphaDec(mat,cipher[start1],key[start2 % lenKey]))
				start2+=1
			else:
				res.append(cipher[start1])
			start1+=1

	elif op == 256:
		start1 = 0
		start2 = 0
		lenKey = len(key)
		while start < len(cipher):
			res.append(cipherTextVCAsciiDec(mat,cipher[start1],key[start2 % lenKey]))
			start2+=1
			start1+=1
	return "".join(res)

def prosesEncrpytPF(str,matPF):
	str2 = str.replace('j','')
	listBgCipher = []
	strBigram = chageStringToBigram(deleteAllCharNonAlphabet(str2))
	print(strBigram)
	for bg in strBigram:
		listBgCipher.append(cipherTextPlayFair(matPF,bg))
	return listBgCipher

def prosesDecryptPF(cipherBg,matPF):
	bgText = ()
	listChar = []
	for bg in cipherBg:
		bgText = cipherTextPlayFairDec(matPF,bg)
		# print(bgText)
		listChar.append(bgText[0])
		listChar.append(bgText[1])
	return "".join(listChar)

def bigramToStr(bigram):
	listChar = []
	for bg in bigram:
		listChar.append(bg[0])
		listChar.append(bg[1])
	return "".join(listChar)

# mat = generateMatrixKeyPlayfair()	
# print("Generate matrix key play fair")
# for i in mat:
# 	print(i)
# print()
# print("############## Encrypting using Play Fair Cipher ####################")
# plain = input("Input Plaintext : ")

# clearplain = deleteAllCharNonAlphabet(plain)
# bigram = prosesEncrpytPF(clearplain,mat)
# strEnc = bigramToStr(bigram)
# print("encrypted")
# print(bigram)
# print("cipher text (penulisan biasa) : " + strEnc)
# print("cipher text (penulisan 5 karakter) : ",end="")
# print5char(strEnc)

# print()
# print("############## Decrypting using Play Fair Cipher ####################")
# print("cipher text : " + strEnc)
# print("plaintext : ",end="")
# print(prosesDecryptPF(bigram,mat))

# matVC = generateMatrixVigenere(26)
print("####### Vigenere Cipher Standard #########")
plaintext = input("Input Plaintext : ")
key = input("Input Key : ")
res1 = prosesEncrpytVC(key,plaintext,26)
print("####### Output Chipper Text biasa #######")
print(res1)

print("####### Output Chipper Text tanpa spasi #######")
res2 = res1.replace(" ","")
print(res2)

print("####### Output kelompok 5 huruf #######")
res2 = deleteAllCharNonAlphabet(res2)
print5char(res2)

print()
print("############ Decripyting ############")
print("Cipher text : " + res1)
res3 = prosesDecryptVC(key,res1,26)
print("plain text : " + res3)	