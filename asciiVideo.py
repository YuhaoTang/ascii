import os
from ffmpy import FFmpeg
from PIL import Image, ImageDraw, ImageFont
import multiprocessing
import shutil

import time

# Variables
picRows = 135
picCols = 480
workingDir = 'C:/Users/TYH/Desktop/tem/'
ttfFile = "C:/Users/TYH/Desktop/ascii/consola.ttf"
blank1 = 'C:/Users/TYH/Desktop/ascii/blank1.png'  # blank image for analyze font
blank = 'C:/Users/TYH/Desktop/ascii/blank2.png'  # blank image for output background, width=picCols*8 height=picRows*16
videoIn = "C:/Users/TYH/Desktop/ascii/9981.mp4"
videoOut = "C:/Users/TYH/Desktop/ascii/9981out.mp4"
videoFramerate = '24'
imgType = '.png'

charpng = workingDir + 'charimg/'
pngin = workingDir + 'imgin/'
txt = workingDir + 'txt/'
pngout = workingDir + 'imgout/'

dict4 = dict()


def imgToText(inputFile, outputFile):
    lines = ''
    img = Image.open(inputFile)
    img = img.resize((picCols, picRows), Image.ANTIALIAS)
    pix = img.load()
    for row in range(picRows):
        line = ''
        for col in range(picCols):
            brightness = pix[col, row][0] / 256
            line += dict4[round(brightness, 3)] # black font white background
            # line += dict4[round(1-brightness, 3)] # white font black background
        lines += line + '\n'
    with open(outputFile, 'w') as the_file:
        the_file.write(lines)


def imgToText2(index, dict3):
    global dict4
    dict4 = dict3
    i = index
    while (True):
        print(i)
        num = str(i).zfill(9)
        inputFile = pngin + num + imgType
        txtFile = txt + num + ".txt"
        if (os.path.exists(inputFile)):
            imgToText(inputFile, txtFile)
            i += 10
        else:
            break


def textToImg(inputFile, outputFile):
    with open(inputFile, 'r') as file:
        content = file.read()
    img = Image.open(blank)
    draw = ImageDraw.Draw(img)
    fnt = ImageFont.truetype(ttfFile, 14)
    draw.multiline_text((0, 0), content, (0, 0, 0), font=fnt, anchor=None, spacing=5, align='left') # black font white background
    # draw.multiline_text((0, 0), content, (255, 255, 255), font=fnt, anchor=None, spacing=5, align='left') # white font black background
    img.save(outputFile)


def textToImg2(index):
    i = index
    while (True):
        print(i)
        num = str(i).zfill(9)
        txtFile = txt + num + '.txt'
        outputFile = pngout + num + imgType
        if (os.path.exists(txtFile)):
            textToImg(txtFile, outputFile)
            i = i + 10
        else:
            break


if __name__ == '__main__':
    # Make sure working dir is empty and create dirs
    print('Prepare working dir')
    if os.path.exists(workingDir):
        shutil.rmtree(workingDir)

    time.sleep(0.1)
    if not os.path.exists(workingDir):
        os.makedirs(workingDir)
        os.makedirs(charpng)
        os.makedirs(pngin)
        os.makedirs(txt)
        os.makedirs(pngout)

    # char to brightness
    print('Char to brightness')
    for index in range(32, 127):
        img = Image.open(blank1)
        draw = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(ttfFile, 50)
        draw.text((10, 10), chr(index), (0, 0, 0), font=fnt)
        img.save(charpng + str(index) + imgType)

    dict1 = dict()
    dict2 = dict()
    dict3 = dict()

    for index in range(32, 127):
        img = Image.open(charpng + str(index) + imgType).convert('LA')  # Font png dir
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

    print('Video to image')
    ff = FFmpeg(
        global_options={'-v warning'},
        inputs={videoIn: None},
        outputs={pngin + '%9d' + imgType: ['-vf', 'scale=480:-1']}
        # outputs={pngin + '%9d' + imgType: ['-ss', '24', '-t', '1', '-vf', 'scale=480:-1']}
    )
    print(ff.cmd)
    ff.run()

    print('Image to text')
    p = multiprocessing.Pool(10)
    for i in range(1, 11):
        p.apply_async(imgToText2, args=(i, dict3,))
    p.close()
    p.join()
    print('Finished image to text')

    print('Text to image')
    p = multiprocessing.Pool(10)
    for i in range(1, 11):
        p.apply_async(textToImg2, args=(i,))
    p.close()
    p.join()
    print('Finished text to image')

    print('Image to Video')
    ff = FFmpeg(
        global_options={'-v warning -y'},
        inputs={pngout + '%9d' + imgType: ['-framerate', videoFramerate]},
        outputs={videoOut: ['-crf', '25', '-pix_fmt', 'yuv420p']}
    )
    print(ff.cmd)
    ff.run()
