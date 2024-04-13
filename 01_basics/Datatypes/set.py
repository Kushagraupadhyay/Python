setone = {1, 2,  4, 3, 5} # Set is a collection of unique elements , mutable and unordered
print(setone)
# with set we can calculate the union, intersection, difference, symmetric difference
print(setone&{1,2,3}) # {1, 2, 3} - intersection
print(setone|{1,2,6}) # {1, 2, 3, 4, 5 , 6} - union

print(setone - {1,2,3,4,5}) # set() - difference , type({})- dictionary - empty braces always resolve to a dictionary not set
type({}) # dict , Empty Set is denoted by - Set()