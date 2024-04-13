mylist=[123 , "chai" , 3.14] # List can contain any type of data type , mutable and ordered

print(mylist) # print() is used to print the list

len(mylist) # len() is used to find the length of the list
print(len(mylist)) # print() is used to print the length of the list

mylist[0] # Accessing the first element of the list
print(mylist[0]) # print() is used to print the first element of the list

myListOne = [1,2,3]
myListTwo = myListOne
myListOne = 'chai'

print(myListTwo) # still point to the same refernce 1,2,3

myListOne = [1,2,3] # difference object than myListTwo
myListOne[0] = 33

print(myListOne) # [33,2,3] # List is mutable
print(myListTwo) # [1,2,3] # List is mutable


l1=[1,2,3]
l2=l1

print(l1)
print(l2)

l1[0]=44

print(l1)
print(l2) # Both l1 and l2 point to the same reference


P1=[1,2,3]
P2=P1
P2=[1,2,3] # P2 is a different object than p1
P1[0]=55

print(P1)
print(P2) # Both P1 and P2 point to different references

h1=[1,2,3]
h2=h1[:] # h2 is a copy of h1 , so h2 is a different object than h1 , colon is iterator from start to end justl like [0:len(h1)]
print(h1)
print(h2)

h1[0]=55
print(h1)
print(h2) # h2 is not affected by the change in h1

# ______________________________________________________________________________________________________________________

tea_variety = ["Black","green","oolong","white"]
print(tea_variety) # ['Black', 'green', 'oolong', 'white']
print(tea_variety[-1]) # white - negative index to access the last element of the list
print(tea_variety[1:3]) # ['green', 'oolong'] - slice of the list
tea_variety[3] = "Herbal"
print(tea_variety) # ['Black', 'green', 'oolong', 'Herbal'] - list is mutable
print(tea_variety[1:2]) # ['green'] - slice of the list
tea_variety[1:2] = "Lemon" # lemon is considered as an array and sliced into the list
print(tea_variety) # ['Black', 'L', 'e', 'm', 'o', 'n', 'oolong', 'Herbal'] - replaces the slice with the string 

tea_variety = ["Black","green","oolong","white"]
tea_variety[1:2] = ["Lemon"] # replaces the slice with the list
print(tea_variety) # ['Black', 'Lemon', 'oolong', 'white'] - replaces the slice with the list
tea_variety[1:3] = ["green","Masala"]
print(tea_variety) # ['Black', 'green', 'Masala', 'white'] - replaces the slice with the list