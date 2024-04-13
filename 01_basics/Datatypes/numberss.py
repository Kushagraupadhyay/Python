# number is ont a single object but a group of objects
# In Python, numbers are of 3 types: Integer, Float, and Complex.
x=2
y=3
z=4
print(x+y)
print(40+2.23)
#print('kushagra'+3) # TypeError: can only concatenate str (not "int") to str
print(int(2.23))
print(float(40))
print('chai'+'code')
print(x,y,z) 
print(y%2)
print(z**5)
print(100**2)
print(2**1000)

result = 1/3.0
print(result)

repr('chai')
print(repr('chai'))
print(str('chai'))
print('chai')

print(1<2)
print(5.0 == 5.0 )
print(4.0 != 5.0)
print(x<y<z)
print(x<y and y<z) # is equivalent to the above statement
print(1 == 2 < 3) # 1 is true 
print(1 == 2 and 2<3)

import math
print(math.floor(3.5)) # 3  - floor - downwards in number line
print(math.floor(-3.5)) # -4
print(math.floor(3.6)) # 3
print(math.floor(3.9)) # 3
print(math.trunc(2.8)) # 2 towards 0 - trun
print(math.trunc(-2.8)) # -2

print(0o20)   # 16 in decimal - octal - start with zero then ooo
print(0xFF)   # 255 in decimal - hexadecimal - start with zero then x
print(oct(16)) # 0o20 - octal - start with zero then ooo
print(hex(255)) # 0xff - hexadecimal - start with zero then x
print(bin(64)) # 0b11111111 - binary - start with zero then b
print(int('20',8)) # 16 - octal - start with zero then ooo , INT WITH A BASE 8
print(int('FF',16)) # 255 - hexadecimal - start with zero then x , INT WITH A BASE 16
print(int('11111111',2)) # 255 - binary - start with zero then b , INT WITH A BASE 2

X=1
X<<2 # 4 - left shift
X>>2 # 0 - right shift

import random
print(random.random()) # 0.0 to 1.0 - random number in decimal
print(random.randint(1,10)) # 1 to 10 - random number in integer
l1=['lemon','masala','ginger','mint'] # random choice from the list
print(random.choice(l1)) # random choice from the list
random.shuffle(l1) # shuffle the list
print(l1) # shuffle the list

print(0.1+0.1+0.1-0.3) # 5.551115123125783e-17 - floating point error
from decimal import Decimal #decimal context manager
result = (Decimal('0.1')+Decimal('0.1')+Decimal('0.1')-Decimal('0.3')) # 0.0 - no floating point error
print(result)

from fractions import Fraction #fraction context manager
print(1/3+1/3+1/3-1/3) # 0.0 - floating point error
result = (Fraction(1,3)+Fraction(1,3)+Fraction(1,3)-Fraction(1,3)) # 1 - no floating point error

