import time

n = [1, 2 ,3 ,4, 54, 5,6 ,6]
def sortbek(n):
    for i in range(len(n)):
        for j in range(len(n)):
            if int(n[i]) > int(n[j]):
                n[i], n[j] = n[j], n[i]
    return n

start_time = time.time()
print(sortbek(n))
response = time.time() - start_time
print(response)