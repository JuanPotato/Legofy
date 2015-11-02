import json
import math

with open('brickColor.json') as data:
    color = json.load(data)

color = [(i['red'], i['green'], i['blue']) for i in color ]

