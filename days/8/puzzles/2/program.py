import sys
from PIL import Image

WIDTH = 25
HEIGHT = 6
LAYER_SIZE = WIDTH * HEIGHT

raw_data = sys.stdin.read()
layers = []
message = []

for i in range(0, len(raw_data), LAYER_SIZE):
  layer = raw_data[i:i+LAYER_SIZE]
  layer = [layer[i:i+WIDTH] for i in range(0, len(layer), WIDTH)]
  layers.append(layer)

for i in range(HEIGHT):
  for j in range(WIDTH):
    for layer in layers:
      pixel = layer[i][j]

      if pixel == '0':
        message.append((0,0,0))
        break
      if pixel == '1':
        message.append((255,255,255))
        break

img = Image.new('RGB', (WIDTH,HEIGHT))
img.putdata(message)
img.save('password.png')
