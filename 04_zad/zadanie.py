import sys
import subprocess
import binascii


def access_bit(data, num):
    base = int(num/8)
    shift = num % 8
    return (data[base] & (1<<shift)) >> shift


if (len(sys.argv) > 1 ):
    bashCommand  = "cat hash.pdf personal.txt  | " + sys.argv[1]
    bashCommand_ = "cat hash.pdf personal_.txt | " + sys.argv[1]


output1 = subprocess.getoutput(bashCommand)

str1 = output1[:-3]

output2 = subprocess.getoutput(bashCommand_)

str2 = output2[:-3]

array_of_bits1  = binascii.unhexlify(str1)
array_of_bits2  = binascii.unhexlify(str2)

array_of_bits1 = [access_bit(array_of_bits1,i) for i in range(len(array_of_bits1)*8)]
array_of_bits2 = [access_bit(array_of_bits2,i) for i in range(len(array_of_bits2)*8)]

print (str1)
print (str2)

counter = 0;
for i in range(0, len(array_of_bits1)):
    if (array_of_bits1[i] == array_of_bits2[i]):
        counter+=1

string = "Liczba bitów różniąca wyniki: " + str(len(array_of_bits1) - counter) + " tj. " + str(round((len(array_of_bits1) - counter)*100/len(array_of_bits1),2)) + "% z " + str(len(array_of_bits1)) + '\n'
print (string)

with open("diff.txt", "a", encoding="utf-8") as f:
    f.write(bashCommand + '\n')
    f.write(bashCommand_ + '\n')
    f.write(str1 + '\n')
    f.write(str2 + '\n')
    f.write(string)
    f.write('\n')
