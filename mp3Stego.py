import mp3Parser
import math

isModifiedBool = False
sizeOfMessage = 0
def signature(isModifiedNum, size):
    mp3Parser.seekStart()
    _embed(1)  # start num

    if(size > 255):
        loop = math.floor(size / 255)
        _embed(loop) # to see how many times extract to calculate size of embedded message
        _embed(isModifiedNum) # is modified flag
        _embed(1) # to set flag whether size is bigger than 255
        _embed(size % 255)

    else:
        _embed(size)  # to see how many times extract to calculate size of embedded message loop buradan geliyor
        _embed(isModifiedNum)  # is modified flag
        _embed(0) # zero means the size of message is equal to 255 or smaller than 255



def _getSignature():
    global sizeOfMessage
    isModifiedBool = False
    mp3Parser.seekStart()
    _extract()
    mp3Parser.nextFrame()
    loop = _extract()
    mp3Parser.nextFrame()
    ismodifiednum = _extract()
    mp3Parser.nextFrame()
    flag = _extract()
    if((ismodifiednum == 23) | (ismodifiednum == 33)):
           isModifiedBool = True

    if(flag == 1):
        mp3Parser.nextFrame()
        mod = _extract()
        sizeOfMessage = mod + loop*255
    else:
        sizeOfMessage = loop

    return sizeOfMessage, isModifiedBool, ismodifiednum


def _embed(payload):
    array = 0x0F
    for i in range(2):
        header = mp3Parser.getFrameHeader()
        header[1] = header[1] & 0xF0
        a = payload & array
        header[1] = header[1] | a
        payload = payload >> 4
        mp3Parser.setFrameHeader(header)
        mp3Parser.nextFrame()



def _extract():
    topla = 0x0F
    header = mp3Parser.getFrameHeader()
    topla = topla & header[1]
    mp3Parser.nextFrame()
    header = mp3Parser.getFrameHeader()
    header[1] = header[1] << 4
    binary = format(header[1], "08b")
    header[1] = int(binary[-8:], 2)
    topla = topla | header[1]
    return topla

def _countFrames():
    mp3Parser.seekStart()
    size, isModifiedBool, ismodifiednumber = _getSignature()
    print(isModifiedBool)
    print(ismodifiednumber)
    mp3Parser.nextFrame()
    frames = 0
    while mp3Parser.hasNext():
        frames += 1
        mp3Parser.nextFrame()
    if(isModifiedBool):
        frames -= size
    return frames

def calculateEmptyBytes():
    frameCount = _countFrames()
    print(frameCount)
    frameCount = math.floor(frameCount/2)
    kiloByte = frameCount / 1000
    return kiloByte

def isModified():
    mp3Parser.seekStart()
    frames, isModifiedBool, ismodifiednumber= _getSignature()
    mp3Parser.nextFrame()
    return frames,isModifiedBool


def embedText(isModifiedNum, message):
    mp3Parser.seekStart()
    signature(isModifiedNum, len(message))
    for i in message:
        _embed(i)


def extractText():
    mp3Parser.seekStart()
    enc = []
    frames, isModifiedBool, ismodifiednum = _getSignature()
    mp3Parser.nextFrame()
    i = 0
    while i < frames:
        enc.append(_extract())
        mp3Parser.nextFrame()
        i += 1
    return enc, ismodifiednum


def yazdir(newfilename):
    with open(newfilename, 'wb') as writer:
        writer.write(mp3Parser.buffer)
