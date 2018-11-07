import sys
import io

lengthOfLine = 16
spaceAscii = 32
def isLetterOrSpace(char):
    if (ord(char) == spaceAscii or (ord(char) >= ord('a') and ord(char) <= ord('z'))):
        return True
    return False


def MakePlainText():
    try:
        finput = open("orig.txt","r")
    except IOError:
        print ("Brak pliku z tekstem oryginalnym (orig.txt)")
        return
    foutput = open("plain.txt","w")
    if (finput != None):
        result = [list(line.rstrip()) for line in finput]
        mergelist = result[0]
        for i in range(1, len(result)):
            mergelist = mergelist + result[i]
        k = 0
        line = ''
        for i in range(0, len(mergelist)):
            if (isLetterOrSpace(mergelist[i])):
                line = line + mergelist[i]
                k+=1
            if (k == lengthOfLine):
                k = 0
                foutput.write(line+'\n')
                line = ''

        return
def Encrypt():
    try:
        finput = open("plain.txt","r")
    except IOError:
        print ("Brak pliku z tekstem do przerobienia (plain.txt)")
        return
    try:
        fkey = open("key.txt", "r")
    except IOError:
        print ("Brak pliku z kluczem")
        return
    key = fkey.readline().rstrip('\n')
    if (len(key) != lengthOfLine):
        print ("Zla dlugosc klucza")
        return
    foutput = io.open("encrypt.txt","w", encoding='utf-8')


    result = [x.rstrip('\n') for x in finput.readlines()]
    ret =''
    for line in result :
        for i in range(0, lengthOfLine):
            c = (ord(line[i]) ^ ord(key[i])) + spaceAscii
            ret = ret + chr(c)
        foutput.write (ret+'\n')
        ret = ''

def Kryptoanalysis():
    try:
        finput = io.open("encrypt.txt", "r", encoding='utf-8')
    except IOError:
        print ("Brak pliku z tekstem zaszyfrowanym")
        return
    result = [x.rstrip('\n') for x in finput.readlines()]
    columnLen = len(result)
    rowLen = len(result[0])
    array = [[0 for x in range(rowLen)] for y in range(columnLen)]
    decryptArr = [[0 for x in range(rowLen)] for y in range(columnLen)]

    for i in range(columnLen):
        for j in range(rowLen):
            array[i][j] = ord(result[i][j]) - spaceAscii

    key  = ['*'] * rowLen


    for column in range(rowLen):
        for row in range(columnLen-2):
            xorM12 = array[row][column] ^ array[row+1][column]
            xorM23 = array[row+1][column] ^ array[row+2][column]
            xorM13 = array[row][column] ^ array[row+2][column]
            if (xorM12 >= 64 and xorM12 <= 95 ):
                if (xorM23 >= 64 and xorM23 <= 95):
                    if (xorM13 == 0):
                        continue
                    else:
                        key[column] = chr(spaceAscii ^ array[row+1][column])
                        break
                elif xorM23 != 0 :
                    key[column] = chr(spaceAscii ^ array[row][column])
                    break
                else :
                    key[column] = chr(spaceAscii ^ array[row+1][column])
                    break

    print ("Uzyskany klucz: ")
    k = ''
    for i in range(len(key)):
        k = k + key[i]
    print (k)
    for row in range(columnLen):
        for column in range(rowLen):
            decryptArr[row][column] = chr(array[row][column] ^ ord(key[column]))
    foutput = open("decrypt.txt", "w")
    for row in range(columnLen):
        for column in range(rowLen):
            foutput.write (decryptArr[row][column])
        foutput.write('\n')


if (sys.argv[1] == '-p'):
    MakePlainText()
elif (sys.argv[1] == '-e'):
    Encrypt()
elif (sys.argv[1] == '-k'):
    Kryptoanalysis()
else:
    print ("Brak argumentu/zly argument")
    print ("-p (przygotowanie tekstu do przykładu działania),")
    print ("-e (szyfrowanie),")
    print ("-k (kryptoanaliza wyłącznie w oparciu o kryptogram)")
