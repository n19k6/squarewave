#```
# +---+   +---+   +---+   +--     -+   +---+   +---+                  
# |   |   |   |   |   |   |   ...  |   |   |   |   |
# +   +---+   +---+   +---+        +---+   +---+   +---+---+---+---+---
#
# |   |...|           |   |
# 1  22   2         113 114            61      62      63      64
# (generate via python)
#```


"""
generate differen strings and remove middle partition

----............----............----............----............----............----............----............----............----............----............
---+            +--+            +--+            +--+            +--+            +--+            +--+            +--+            +--+            +--+
   |            |  |
   
# +---+   +---+   +---+   +--     -+   +---+   +---+                  
# |   |   |   |   |   |   |   ...  |   |   |   |   |
# +   +---+   +---+   +---+        +---+   +---+   +---+---+---+---+---

"""

gear_tooth = [0 for i in range(144)]
for i in range(34):
    gear_tooth[i*4] = 1

s = list(" "*144*4)


for i in range(len(gear_tooth)):
    if gear_tooth[i] == 1:
        s[i*4] = "-"
        s[i*4+1] = "-"
        s[i*4+2] = "-"
        s[i*4+3] = "-"

#s = s[:160]

#s = str(s)
s = ''.join(s)

s1 = s
s1 = s1.replace("- ", "-+")
s1 = s1.replace(" -", " +")
s1 = s1.replace("-", "+", 1)

s2 = s
s2 = s2.replace("- ", "-+")
s2 = s2.replace(" -", " +")
s2 = s2.replace("+", "|")
s2 = s2.replace("-", " ")
s2 = s2.replace(" ", "|", 1)

s3 = s
s3 = s3.replace("- ", "-+")
s3 = s3.replace(" -", " +")
s3 = s3.replace("-", "_")
s3 = s3.replace(" ", "-")
s3 = s3.replace("_", " ")
s3 = s3.replace(" ", "+", 1)

s4 = "0"
for i in range(1,144):
    s4 = s4+str(i).rjust(4)
s4 = s4.ljust(len(s3))


def mod(s, f = '       '):
    #return s+"|"
    return s[:63]+f+s[-83:]

#print(mod(s.replace(" ", " ")))
print(mod(s1))
print(mod(s2, "  ...  "))
print(mod(s3))
print(mod(s4))
