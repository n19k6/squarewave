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
scx = [cx+sr*math.sin(2*math.pi/144*(i-0.5)) for i in range(144)]
scy = [cy-sr*math.cos(2*math.pi/144*(i-0.5)) for i in range(144)]

# coordinates for big circle
bcx = [cx+br*math.sin(2*math.pi/144*(i-0.5)) for i in range(144)]
bcy = [cy-br*math.cos(2*math.pi/144*(i-0.5)) for i in range(144)]
# print(scx)

def draw_gear(sequence, dx=0, color="blue"):
    len_of_sequence = len(sequence)
    for i in range(len_of_sequence):
        #print(i)
        if i == 0:
            if (sequence[-1] == 0):
                print(f'<path transform="translate({dx:.2f}) scale(1 1)" d="M {scx[0]:.2f} {scy[0]:.2f} ', end='')
            else:
                print(f'<path transform="translate({dx:.2f}) scale(1 1)" d="M {bcx[0]:.2f} {bcy[0]:.2f} ', end='')
            if (sequence[-1] == 0 and sequence[0] == 1):
                print (f'L {bcx[0]:.2f} {bcy[0]:.2f} ', end='')
            if (sequence[-1] == 1 and sequence[0] == 0):
                print (f'L {scx[0]:.2f} {scy[0]:.2f} ', end='')
            j=0
        elif i == len_of_sequence-1:
            if sequence[j] == 0:
                print(f'A {sr:.2f} {sr:.2f} 0 0 1 {scx[-1]:.2f} {scy[-1]:.2f} ', end='')
            else:
                print(f'A {br:.2f} {br:.2f} 0 0 1 {bcx[-1]:.2f} {bcy[-1]:.2f} ', end='')
            if sequence[j] != sequence[i]:
                if sequence[j] == 0:
                    print(f'L {bcx[-1]:.2f} {bcy[-1]:.2f} ', end='')
                else:
                    print(f'L {scx[-1]:.2f} {scy[-1]:.2f} ', end='')
            if sequence[-1] == 0:
                print(f'A {sr:.2f} {sr:.2f} 0 0 1 {scx[0]:.2f} {scy[0]:.2f} ', end='')
            else:
                print(f'A {br:.2f} {br:.2f} 0 0 1 {bcx[0]:.2f} {bcy[0]:.2f} ', end='')
            print(f'Z" stroke="{color}" fill="transparent"/>')
        elif sequence[j] != sequence[i]:
            if sequence[i] == 0:
                print(f'A {br:.2f} {br:.2f} 0 0 1 {bcx[i]:.2f} {bcy[i]:.2f} ', end='')
                print(f'L {scx[i]:.2f} {scy[i]:.2f} ', end='')
            else:
                print(f'A {sr:.2f} {sr:.2f} 0 0 1 {scx[i]:.2f} {scy[i]:.2f} ', end='')
                print(f'L {bcx[i]:.2f} {bcy[i]:.2f} ', end='')
            j=i
            #pass
        #print(j)

print('<svg width="640" height="480" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">')


for i in range(144):
    print(i)
    print(f'<circle transform="translate(240) scale(1 1)" cx="{scx[i]:.2f}" cy="{scy[i]:.2f}" r="1" stroke="red" fill="transparent" stroke-width="0.1"/>')
    print(f'<circle transform="translate(240) scale(1 1)" cx="{bcx[i]:.2f}" cy="{bcy[i]:.2f}" r="1" stroke="red" fill="transparent" stroke-width="0.1"/>')

gear_tooth = [0 for i in range(144)]
for i in range(34):
    gear_tooth[i*4] = 1

draw_gear(gear_tooth)
#gear_tooth[1] = 0
#gear_tooth[-2] = 1

gear_tooth = [0 for i in range(144)]
for i in range(4):
    gear_tooth[i*36] = 1
    
draw_gear(gear_tooth, 120, "green")

gear_tooth = [0 for i in range(144)]
for i in range(3):
    gear_tooth[i*36] = 1

draw_gear(gear_tooth, 240, "red")


print('</svg>')

exit(0)

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

