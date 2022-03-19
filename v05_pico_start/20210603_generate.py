import math

# this program dumps a svg file to stdout which contains three different gears

# center of gears
cx = 100
cy = 100

# radius of small and big circle used to construct gears
# br-sr defines tooth high
sr = 50
br = 55

# coordinates for small circle
scx = [cx+sr*math.sin(2*math.pi/144*(i-0.5)) for i in range(143)]
scy = [cy-sr*math.cos(2*math.pi/144*(i-0.5)) for i in range(143)]

# coordinates for big circle
bcx = [cx+br*math.sin(2*math.pi/144*(i-0.5)) for i in range(143)]
bcy = [cy-br*math.cos(2*math.pi/144*(i-0.5)) for i in range(143)]
# print(scx)

print('<svg width="640" height="480" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">')

print(f'<path d="M {scx[0]:.2f} {scy[0]:.2f} ', end='')
for i in range(34):
    print (f'L {bcx[i*4]:.2f} {bcy[i*4]:.2f} ', end='')
    print (f'A {br:.2f} {br:.2f} 0 0 1 {bcx[i*4+1]:.2f} {bcy[i*4+1]:.2f} ', end='')
    print(f'L {scx[i*4+1]:.2f} {scy[i*4+1]:.2f} ', end='')
    print(f'A {sr:.2f} {sr:.2f} 0 0 1 {scx[i*4+4]:.2f} {scy[i*4+4]:.2f} ', end='')

print(f'A {sr:.2f} {sr:.2f} 0 0 1 {scx[0]:.2f} {scy[0]:.2f} ', end='')
print('Z" stroke="green" fill="transparent"/>');


print(f'<path transform="translate(120)" d="M {scx[0]:.2f} {scy[0]:.2f} ', end='')
for i in range(4):
    print (f'L {bcx[i*36]:.2f} {bcy[i*36]:.2f} ', end='')
    print (f'A {br:.2f} {br:.2f} 0 0 1 {bcx[i*36+1]:.2f} {bcy[i*36+1]:.2f} ', end='')
    print(f'L {scx[i*36+1]:.2f} {scy[i*36+1]:.2f} ', end='')
    print(f'A {sr:.2f} {sr:.2f} 0 0 1 {scx[((i+1)*36) % 144]:.2f} {scy[((i+1)*36) % 144]:.2f} ', end='')

print('Z" stroke="blue" fill="transparent"/>')

print(f'<path transform="translate(240)" d="M {scx[0]:.2f} {scy[0]:.2f} ', end='')
for i in range(3):
    print(f'L {bcx[i*36]:.2f} {bcy[i*36]:.2f} ', end='')
    print(f'A {br:.2f} {br:.2f} 0 0 1 {bcx[i*36+1]:.2f} {bcy[i*36+1]:.2f} ', end='')
    print(f'L {scx[i*36+1]:.2f} {scy[i*36+1]:.2f} ', end='')
    print(f'A {sr:.2f} {sr:.2f} 0 0 1 {scx[((i+1)*36) % 144]:.2f} {scy[((i+1)*36) % 144]:.2f} ', end='')

print(f'A {sr:.2f} {sr:.2f} 0 0 1 {scx[0]:.2f} {scy[0]:.2f} ', end='')
print('Z" stroke="red" fill="transparent"/>')

print('</svg>')

