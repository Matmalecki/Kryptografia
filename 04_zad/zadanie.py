import sys
import subprocess
import binascii



if (len(sys.argv) > 1 ):
    bashCommand  = "cat hash.pdf personal.txt  | " + sys.argv[1]
    bashCommand_ = "cat hash.pdf personal_.txt | " + sys.argv[1]


output1 = subprocess.getoutput(bashCommand)

str1 = output1[:-3]

output2 = subprocess.getoutput(bashCommand_)

str2 = output2[:-3]

array_of_bits1 = bin(int(str1,16))
array_of_bits2 = bin(int(str2,16))

counter = 0;
for i in range(0, len(array_of_bits1)):
    if (array_of_bits1[i] == array_of_bits2[i]):
        counter+=1


print ("Podobienstwo w: " , counter*100/len(array_of_bits1) , " %")
