import random
import binascii
import sys

def pow_with_mod(base, exponent, mod):
    ret = 1
    base %= mod
    while (exponent > 0):
        if (exponent & 1):
            ret = (ret * base) % mod
        base = (base * base ) % mod
        exponent = exponent >> 1
    return ret

def modInverse(a, m) : 
    m0 = m 
    y = 0
    x = 1
    if (m == 1) : 
        return 0
    while (a > 1) : 
        q = a // m 
        t = m 

        m = a % m 
        a = t 
        t = y 

        y = x - q * y 
        x = t 
  
    if (x < 0) : 
        x = x + m0 
  
    return x 
      
def gcd(a, b) : 
    if (a == 0): 
        return b    
    return gcd(b % a, a) 

def messageToNum(message):
    return int(binascii.hexlify(str.encode(message)),16) 

def numToMessage(num):
    message = hex(num)
    return binascii.unhexlify(message[2:]).decode("utf-8")


def generate():
    f_elg = open("elgamal.txt","r")
    f_priv = open("private.txt","w")
    f_pub = open("public.txt","w")
    p = int(f_elg.readline())
    g = int(f_elg.readline())
    priv_key = random.randint(0,p) # private
    pub_key = pow_with_mod(g,priv_key,p)
    f_priv.write('{}\n'.format(p))
    f_priv.write('{}\n'.format(g))
    f_priv.write('{}\n'.format(priv_key))
    f_pub.write('{}\n'.format(p))
    f_pub.write('{}\n'.format(g))
    f_pub.write('{}\n'.format(pub_key))

def encrypt():
    f_pub = open("public.txt","r")
    f_mess = open("plain.txt","r")
    f_enc = open("encrypt.txt","w")
    p = int(f_pub.readline())
    g = int(f_pub.readline())
    pub_key = int(f_pub.readline())
    message = "".join(f_mess.readlines()).strip()
    m = messageToNum(message)
    if (m > p):
        raise ValueError('m >= p!') 
    k = random.randint(0,p)
    first = pow_with_mod(g,k,p)
    second = (m * pow_with_mod(pub_key,k,p)) % p
    f_enc.write('{}\n'.format(first))
    f_enc.write('{}\n'.format(second))


def decrypt():
    f_priv = open("private.txt","r")
    f_enc = open("encrypt.txt","r")
    f_dec = open("decrypt.txt","w")

    p = int(f_priv.readline())
    g = int(f_priv.readline())
    b = int(f_priv.readline())

    gK = int(f_enc.readline())
    mBetaK = int(f_enc.readline())
    Bx = pow_with_mod(gK,b,p)
    inverse = modInverse(Bx,p)
    message = (inverse * mBetaK) % p
    f_dec.write('{}\n'.format(numToMessage(message)))

def sign():
    f_priv = open("private.txt","r")
    f_mess = open("message.txt","r")
    f_sign = open("signature.txt","w")

    p = int(f_priv.readline())
    g = int(f_priv.readline())
    b = int(f_priv.readline())

    message = "".join(f_mess.readlines()).strip()
    m = messageToNum(message)
    if (m > p):
        raise ValueError('m >= p!') 
    k = random.randint(0,p-1)
    while gcd(k,p-1) != 1:
        k = random.randint(0,p-1)

    r = pow_with_mod(g,k,p)
    x = (m%(p-1)-((b*r)%(p-1))) % (p-1)
    x = x * modInverse(k,p-1) % (p-1)
    f_sign.write('{}\n'.format(r))
    f_sign.write('{}\n'.format(x))

def checkSign():
    f_pub = open("public.txt","r")
    f_mess = open("message.txt","r")
    f_sign = open("signature.txt","r")
    f_ver = open("verify.txt","w")

    p = int(f_pub.readline())
    g = int(f_pub.readline())
    pub_key = int(f_pub.readline())

    message = "".join(f_mess.readlines()).strip()
    m = messageToNum(message)
    if (m > p):
        raise ValueError('m >= p!') 
    r = int(f_sign.readline())
    x = int(f_sign.readline())

    first = pow_with_mod(g,m,p)
    second = (pow_with_mod(r,x,p) * pow_with_mod(pub_key,r,p) ) % p

    if (first == second):
        print("T")
        f_ver.write('{}\n'.format("T"))
    else:
        print("N")
        f_ver.write('{}\n'.format("N"))

if (len(sys.argv) < 2):
    print("Brak argumentu")
    sys.exit()    
if (sys.argv[1] == '-k'):
    generate()
elif (sys.argv[1] == '-e'):
    encrypt()
elif (sys.argv[1] == '-d'):
    decrypt()
elif (sys.argv[1] == '-s'):
    sign()
elif (sys.argv[1] == '-v'):
    checkSign()
else:
    print ("Brak argumentu/zly argument")
    print ("-k (przygotowanie kluczy),")
    print ("-e (szyfrowanie),")
    print ("-d (odszyfrowanie)")
    print ("-s (podpisanie)")
    print ("-v (sprawdzanie podpisu)")
