chai = "Lemon Chai"
print(chai)

chai = "Masala Chai"
first_char=chai[0]
print(first_char) # M - first character of the string
slice_chai = chai[0:6]
print(slice_chai) # Masala - slice of the string

num_list = "0123456789"
print(num_list[:]) # 0123456789 - slice of the string` from start to end
print(num_list[3:]) # 3456789 - slice of the string from 3 to end
print(num_list[:7]) # 012 - slice of the string from start to 7
print(num_list[0:7:2]) # 0246 - slice of the string from start to 7 with step 2

print(chai.upper()) # MASALA CHAI
print(chai.lower()) # masala chai

chai="     Masala  Chai     "
print(chai.strip()) # Masala Chaia - removes leading and trailing spaces

chai= "Lemon Chai"
print(chai.replace("Lemon", "Ginger")) # Masala Chai     - replaces Lemon with Ginger

chai= "Lemon, Ginger, Masala, Mint"
print(chai.split()) # ['Lemon,', 'Ginger,', 'Masala,', 'Mint'] - splits the string by space and returns a list
print(chai.split(", ")) # ['Lemon', 'Ginger', 'Masala', 'Mint'] - splits the string by comma followed by a space and returns a list

chai= "Masala Chai"
print(chai.find("Chai")) # 7 - returns the index of the first occurrence of the substring
print(chai.find("chai")) # -1 - returns -1 if the substring is not found
print(chai.count("Chai")) # 1 - returns the number of occurrences of the substring

chai_type = "Masala"
quantity = 2
order = "I ordered {} cups of {} chai"
print(order.format(quantity,chai_type)) # I ordered 2 cups of Masala chai - formats the string with the given values 


chai_variety = ["Masala", "Ginger", "Lemon", "Mint"]
print(chai_variety) # ['Masala', 'Ginger', 'Lemon', 'Mint']
print("".join(chai_variety)) # MasalaGingerLemonMint - joins the list of strings with an empty string
print(" ".join(chai_variety)) # Masala Ginger Lemon Mint - joins the list of strings with a space

chai = "Masala Chai"
print(len(chai)) # 11 - returns the length of the string
for each_letter in chai:
    print(each_letter) # M a s a l a   C h a i - prints each character of the string

chai= "He said, \"Masala chai is awesome\" " # He said, "Masala chai is awesome" - escape character to include double quotes in the string
print(chai)
chai = r"Masala\nchai" # Masala\nchai - raw string
chai2 = "Masala\nchai" # Masala - chai - normal string with newline character
print(chai)
print(chai2)

chai = r"c:\user\pwd" # c:\user\pwd - raw string
print(chai)
chai = "c:\\user\\pwd" # c:\user\pwd - escape character to include backslash in the string 
print(chai)

chai = "Masala in Chai"
print("Masala" in chai) # True - checks if the substring is present in the string
print("Masalaa" in chai) # False - checks if the substring is present in the string