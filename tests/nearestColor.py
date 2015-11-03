import json
import math

with open('brickColor.json') as data:
    color = json.load(data)

color = [(int(i['red']), int(i['green']), int(i['blue'])) for i in color ]

def getNearestColor(allColor, im):
    d = {}
    for i in xrange(len(allColor)):
        c = map(lambda i,j:i-j, allColor[i],im)
        c = sum([j**2 for j in c])
        
        d[c] = allColor[i]

    return d[min(d.keys())]

print nearestColor(color, (160,165,160))
    
