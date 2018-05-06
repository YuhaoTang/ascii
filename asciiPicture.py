import os
from PIL import Image, ImageDraw, ImageFont
import shutil
import time

picRows = 90
picCols = 320
workingDir = 'E:/tem/'
ttfFile = "E:/consolab.ttf"
blank1 = 'E:/blank1.png'  # blank image for analyze font
blank = 'E:/blank2.png'  # blank image for output background, width=picCols*8 height=picRows*16
imgType = '.png'
inputFile = 'E:/in2.jpg'
outputFile = 'E:/out2.png'

dict3 = dict()

def imgToText(inputFile, outputFile):
    lines = ''
    img = Image.open(inputFile)
    img = img.resize((picCols, picRows), Image.ANTIALIAS)
    pix = img.load()
    for row in range(picRows):
        line = ''
        for col in range(picCols):
            brightness = pix[col, row][0] / 256
            line += dict3[round(brightness, 3)] # black font white background
            # line += dict3[round(1-brightness, 3)] # white font black background
        lines += line + '\n'
    with open(outputFile, 'w') as the_file:
        the_file.write(lines)

def textToImg(inputFile, outputFile):
    with open(inputFile, 'r') as file:
        content = file.read()
    img = Image.open(blank)
    draw = ImageDraw.Draw(img)
    fnt = ImageFont.truetype(ttfFile, 14)
    draw.multiline_text((0, 0), content, (0, 0, 0), font=fnt, anchor=None, spacing=5, align='left') # black font white background
    # draw.multiline_text((0, 0), content, (255, 255, 255), font=fnt, anchor=None, spacing=5, align='left') # white font black background
    img.save(outputFile)


print('Prepare working dir')
if os.path.exists(workingDir):
    shutil.rmtree(workingDir)
time.sleep(0.1)
if not os.path.exists(workingDir):
    os.makedirs(workingDir)

print('Char to brightness')
for index in range(32, 127):
    img = Image.open(blank1)
    draw = ImageDraw.Draw(img)
    fnt = ImageFont.truetype(ttfFile, 50)
    draw.text((10, 10), chr(index), (0, 0, 0), font=fnt)
    img.save(workingDir + str(index) + imgType)

dict1 = dict()
dict2 = dict()

for index in range(32, 127):
    img = Image.open(workingDir + str(index) + imgType).convert('LA')  # Font png dir
    pix = img.load()
    total = 0
    for row in range(100):
        for col in range(50):
            total = total + pix[col, row][0]
    dict1[total] = index

print('Build dict1')
del dict1[sorted(dict1.keys())[0]]
min = sorted(dict1.keys())[0]
max = sorted(dict1.keys())[len(dict1.keys()) - 1]

print('Build dict2')
for key in sorted(dict1.keys()):
    percent = (key - min) / (max - min)
    dict2[percent] = chr(dict1[key])
dict2[0.97] = " "


def brightToChar(brightness):
    global dict2
    for key in sorted(dict2.keys(), reverse=True):
        if (brightness >= key):
            return dict2[key]


print('Build dict3')
for index in range(1001):
    brightness = index / 1000
    dict3[brightness] = brightToChar(brightness)

print('Image to text')
imgToText(inputFile, workingDir+'tem.txt')

print('Text to image')
textToImg(workingDir+'tem.txt', outputFile)
