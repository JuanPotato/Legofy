import json
import math

#with open('brickColor.json') as data:
#    color = json.load(data)

color = [
    (255, 255, 255),  # 1: white
    (217, 187, 123),  # 5: brick yellow
    (214, 114, 64),  # 18: nougat
    (222, 0, 13),  # 21: bright red
    (0, 87, 168),  # 23: bright blue
    (254, 196, 0),  # 24: bright yellow
    (1, 1, 1),  # 26: black
    (0, 123, 40),  # 28: dark green
    (0, 150, 36),  # 37: bright green
    (168, 61, 21),  # 38: dark orange
    (71, 140, 198),  # 102: medium blue
    (231, 99, 24),  # 106: bright orange
    (149, 185, 11),  # 119: bright yellowish green
    (156, 0, 107),  # 124: bright reddish violet
    (94, 116, 140),  # 135: sand blue
    (141, 116, 82),  # 138: sand yellow
    (0, 37, 65),  # 140: earth blue
    (0, 52, 22),  # 141: earth green
    (95, 130, 101),  # 151: sand green
    (128, 8, 27),  # 154: dark red
    (244, 155, 0),  # 191: flame yellowish orange
    (91, 28, 12),  # 192: reddish brown
    (156, 146, 145),  # 194: medium stone grey
    (76, 81, 86),  # 199: dark stone grey
    (228, 228, 218),  # 208: light stone grey
    (135, 192, 234),  # 212: light royal blue
    (222, 55, 139),  # 221: bright purple
    (238, 157, 195),  # 222: light purple
    (255, 255, 153),  # 226: cool yellow
    (44, 21, 119),  # 268: medium lilac
    (245, 193, 137),  # 283: light nougat
    (48, 15, 6),  # 308: dark brown
    (170, 125, 85),  # 312: medium nougat
    (70, 155, 195),  # 321: dark azur
    (104, 195, 226),  # 322: medium azur
    (211, 242, 234),  # 323: aqua
    (160, 110, 185),  # 324: medium lavender
    (205, 164, 222),  # 325: lavender
    (245, 243, 215),  # 329: white glow
    (226, 249, 154),  # 326: spring yellowish green
    (119, 119, 78),  # 330: olice green
    (150, 185, 59),  # 331: medium yellowish green
]


#color = [(int(i['red']), int(i['green']), int(i['blue'])) for i in color ]

def getNearestColor(allColor, im):
    d = {}
    for i in xrange(len(allColor)):
        c = map(lambda i,j:i-j, allColor[i],im)
        c = sum([j**2 for j in c])
        
        d[c] = allColor[i]

    return d[min(d.keys())]

