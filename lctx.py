from inc_noesis import *
import noesis
import rapi
import os
def registerNoesisTypes():
    handle = noesis.register("Tornado Outbreak LCTX",".lctx")
    noesis.setHandlerTypeCheck(handle,noepyCheckType)
    noesis.setHandlerLoadRGBA(handle,getTex)
    return 1

def noepyCheckType(data):
    return 1   

def texType(bs,texName,texWidth,texHeight,texList,texType,texData):
    texName = texName
    if texType == 2:
        data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "A8R8G8B8")
        texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
    else:
        texList.append(NoeTexture(texName,texWidth,texHeight,texData,noesis.NOESISTEX_DXT1))
def readLCTX(data,bs,texList):
    reader = NoeBitStream(data,NOE_BIGENDIAN)
    reader.seek(8)
    stringLength = reader.readUByte()
    texName = reader.readString()
    type = reader.readUInt()
    unk = reader.readUInt()
    print("Texture type is: " + str(type))
    mipMapCount = reader.readUByte()
    for i in range(mipMapCount):
        width = reader.readUInt()
        height = reader.readUInt()
        size = reader.readUInt()
        texData = reader.readBytes(size)
        if (type == 5):
            texData = rapi.swapEndianArray(texData,2)
            #texData = rapi.imageUntile360DXT(texData,width,height,8)
        if i == 0:
            texType(bs,texName,width,height,texList,type,texData)
def getTex(data,texList):
    bs = NoeBitStream(data,NOE_BIGENDIAN)
    bs.seek(0)
    check = bs.readUInt()
    if (check == 3):
        bs.seek(0x10)
        lctxDataSize = bs.readUInt()
        lctxData = bs.readBytes(lctxDataSize)
        readLCTX(lctxData,bs,texList)
    else:
        while (bs.tell() < os.path.getsize(rapi.getInputName())):
            lctxDataSize = bs.readUInt()
            lctxData = bs.readBytes(lctxDataSize)
            readLCTX(lctxData,bs,texList)
    return 1
    