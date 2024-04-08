import numpy as np
from PIL import Image

img = Image.open('test.png').convert('RGB')
# img = img.resize((int(img.width / 4), int(img.height / 4)))
img = np.floor(np.asarray(img, dtype='float32') / 8).astype('uint8')

lut_png = np.asarray(Image.open('lut.png').convert('RGB'))

lut = np.zeros((32, 32, 32, 3), dtype='uint8')
pattern = np.zeros((17, 4, 4), dtype='float32')
colors = np.zeros((16, 3), dtype='uint8')

for y in range(4):
    for x in range(8):
        for g in range(32):
            lut[y * 8 + x, g] = lut_png[y * 32 + g, x * 32 : x * 32 + 32]

for x in range(17):
    for y in range(4):
        pattern[x, y] = lut_png[128 + y, x * 4 : x * 4 + 4, 0]

pattern = pattern / 255
colors[:] = lut_png[132, 0:16]

# print(img[0,0])
# print(lut[5,5,5])
# print(lut[15, 15, 15])
# print(pattern)
# print(colors)
# print(np.where(pattern[2], colors[7], colors[0]))

# for i in range(32):
#     print(lut[i, i, i])

out_img = np.zeros_like(img, dtype='uint8')

for y in range(out_img.shape[0]):
    for x in range(out_img.shape[1]):
        r, g, b = img[y, x, :]
        fr, to, factor = lut[b, g, r, :]
        out_img[y, x, :] = colors[to] if pattern[factor, y % 4, x % 4] > 0.5 else colors[fr]

# out_img = (np.power(out_img.astype('float32') / 255.0, 1 / 2.2) * 255).astype('uint8')

Image.fromarray(out_img).save('test_out.png')