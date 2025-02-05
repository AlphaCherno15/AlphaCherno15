def exponentiation():
    y = x ** i #exponentiation

# arguments defaults
def append(n , l=[]):
    l.append(n)
    return l
l1 = append(0) #[0]
l2 = append(1) #[0, 1] 
# correct way
def append(n , l=None):
    if l is None:
        l = []
    l.append(n)
    return l
l1 = append(0) #[0]
l2 = append(1) #[1] 

# isinstance check isinstance(x, 'instance, like tuple or int')
# type check type(x)

# kinda wrong
if x == None, True, False:
# correct way 
if x is None, True, False:

# kinda wrong
if x == True:
if x is True:
if bool(x):
# correct way 
if x:

# range len pattern
a = [1, 2, 3]
for i n range(len(a))
    v = a[i]
# correct way 
for v in a:
# if need index
for i, v in enumerate(a):'
    # retrive index and elemnet at the same time'

merging lists 
a = [1, 2, 3]
b = [4, 5, 6]
for i n range(len(a))
    v = a[i]
    z = b[i]
# correct way 
for v, z in zip(a, b):
# or 
for i, (v, z) in enumerate(zip(a, b)):#get hold of index

# loop using key val
d = {"a":1, "b":2, "c":3}
for key, val in d.item(): #get hold of both keys(a, b ,c) and values(1, 2 ,3)

# tuple unpacking
mytuple = (1, 2)
x = mytuple[0]
y = mytuple[1]
# correct way
x, y = mytuple

# index counter variable
l = [1, 2, 3]
i = 0
for x in l:
    i += 1
# correct way
for i, x in enumerate(l):

# timing with time for code timing
start = time.time()
end = time.time()
print(end - start)
# use insted
start = time.perf_counter()
end = time.perf_counter()
print(end - start)

# usinf logging module
print("debug info")
import logging
logging.debug("debug info")
logging.info("info")
logging.error("error info")
def main():
    level = logging.DEBUG
    fmt = '[%(levelname)s] %(asctime)s - %(message)s'
    logging.basicConfig(level=level, format=fmt)

# leran more of Numpy and pandas for math and data analysis 

# learn about package

# rounding numbers in a string
n = 0.029884663
text = f'{n:.2f}'

#use more 
if __name__ == "__main__":
    do something
