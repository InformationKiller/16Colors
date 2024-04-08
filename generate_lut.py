import numpy as np
from PIL import Image
import math

colors = np.asarray([[0, 0, 0],
                     [0, 0, 128],
                     [0, 128, 0],
                     [0, 128, 128],
                     [128, 0, 0],
                     [128, 0, 128],
                     [128, 128, 0],
                     [192, 192, 192],
                     [128, 128, 128],
                     [0, 0, 255],
                     [0, 255, 0],
                     [0, 255, 255],
                     [255, 0, 0],
                     [255, 0, 255],
                     [255, 255, 0],
                     [255, 255, 255]], dtype='float32') / 255.0
colors = np.power(colors, 2.2)
colors = colors[np.argsort(0.299 * colors[:,0] + 0.587 * colors[:,1] + 0.114 * colors[:,2])]

# print(colors)

pre = np.zeros((16, 16, 16, 3), dtype='float32')

for i in range(16):
    for j in range(16):
        for k in range(16):
            pre[i, j, k] = (k / 16) * colors[j] + (1 - k / 16) * colors[i]

colors = np.power(colors, 1 / 2.2)
pre = np.power(pre, 1 / 2.2)
# pre = (pre * 255 / 8).astype('uint8').astype('float32')

lut = np.zeros((32, 32, 32, 3), dtype='uint8')

for b in range(32):
    for g in range(32):
        for r in range(32):
            min_dist = np.linalg.norm(np.abs(pre - np.asarray([r, g, b]) / 31.0), axis=-1)
            w = np.where(min_dist == np.min(min_dist))
            lut[b, g, r, :] = (w[0][0], w[1][0], w[2][0])

lut_png = np.zeros((256, 256, 3), dtype='uint8')

for y in range(4):
    for x in range(8):
        for y_ in range(32):
            for x_ in range(32):
                lut_png[y * 32 + y_, x * 32 + x_, :] = lut[y * 8 + x, y_, x_]

pattern = np.zeros(16, dtype='uint8')
up = np.asarray([0, 2, 5, 7, 8, 10, 13, 15])[[0, 5, 3, 7, 6, 1, 2, 4]]
down = np.asarray([1, 3, 4, 6, 9, 11, 12, 14])[np.random.choice(8, 8, False)]

for i in range(8):
    pattern[up[i]] = 255

    for y in range(4):
        for x in range(4):
            lut_png[128 + y, i * 4 + x + 4, :] = [pattern[y * 4 + x], pattern[y * 4 + x], pattern[y * 4 + x]]

for i in range(7):
    pattern[down[i]] = 255

    for y in range(4):
        for x in range(4):
            lut_png[128 + y, i * 4 + x + 36, :] = [pattern[y * 4 + x], pattern[y * 4 + x], pattern[y * 4 + x]]

for i in range(colors.shape[0]):
    lut_png[132, i, :] = (colors[i] * 255)

Image.fromarray(lut_png).save('lut.png')