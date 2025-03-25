from django.test import TestCase

# Create your tests here.

s= 'Hello World!'
# sorted_s = ''.join(sorted(s))
# print(sorted_s)
#
# char_index = []
# amount_char = 1
# step = 0
# for i in range(len(sorted_s) -1):
#     if sorted_s[i] == sorted_s[i+1]:
#         amount_char +=1
#     char_index.append(amount_char)
#     amount_char = 1
# index = char_index.index(max(char_index))
# print(sorted_s[index])

dct = {}

for x in s:
    dct[x] = dct.get(x, 0) + 1

_max = max(dct.values())
for x in dct:
    if dct[x] == _max:
        print(x)