import math
import numpy as np
from math import floor

start = 0
current = 0
bitrate = 0
srate = 0
padding = 0
end=0
offset = 0
bitrateTable = [
        0, 32, 40, 48,
        56, 64, 80, 96,
        112, 128, 160, 192,
        224, 256, 320, 0
    ]

srateTable = [
        44.1, 48.0, 32.0, 0.0
    ]

def openFile(filename):
    global end, buffer
    file = open(filename,"rb")
    bytes = file.read()
    buffer1 = np.frombuffer(bytes, dtype=np.uint8)
    file.close()
    buffer = np.copy(buffer1)
    buffer.flags["WRITEABLE"]
    end = len(buffer)
    _skipTags()
    _unpack()



def _synchToInt(b):
    a = b[3] | (b[2] << 7) | (b[1] << 14) | (b[0] << 21)
    return a


def _skipTags():
    global end

    triplet = buffer[end - 128:end - 125]
    str = triplet.tostring().decode("ascii")

    if str == "TAG":
        end = end-128
        triplet = buffer[0:3]
        str = triplet.tostring().decode("ascii")
        if str == "ID3":
            global current, start
            size = buffer[6:10]
            current = start = _synchToInt(size) + 10


def _unpack():
    global current, bitrate, srate, padding
    byte = buffer[current+2]
    bitrate = bitrateTable[byte >> 4]
    srate = srateTable[(byte & 0x0C) >> 2]
    padding = (byte & 0x02) >> 1
    return bitrate, srate, padding


def getFrameHeader():
     global current
     a = buffer[current+2:current+4]
     return buffer[current+2:current+4]


def setFrameHeader(header):
    global current
    buffer[current + 2] = header[0]
    buffer[current + 3] = header[1]


def nextFrame():
    global current, offset, bitrate, srate, padding
     #burada bir unpacki deneyelim
    a = srate
    if(a == 0):
        offset = math.trunc(floor((144 * bitrate / 1)))
        current += offset

    else:
        offset = math.trunc(floor(((144 * bitrate / srate)+padding)))
        current += offset
    _unpack()


def hasNext():
    global current, end,offset
    return current < end - offset


def seekStart():
    global current, start, offset
    offset = 0
    current = start


