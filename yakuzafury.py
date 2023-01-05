
from inc_noesis import *


def registerNoesisTypes():
	handle = noesis.register("Yakuza Fury",".bin")
	noesis.setHandlerTypeCheck(handle, bcCheckType)
	noesis.setHandlerLoadModel(handle, bcLoadModel)
	return 1


# Check file type

def bcCheckType(data):
	return 1

def bcLoadModel(data, mdlList):
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    ctx = rapi.rpgCreateContext()
    bs.seek(0x2a0)
    texturename = bs.readString().replace(".tm2","")
    bs.seek(0x39c)
    vertCount = bs.readUInt()
    vertBuff = bytes()
    normals = bytes()
    uvs = bytes()
    for _ in range(vertCount):
        vert = NoeVec3.fromBytes(bs.readBytes(12))
        vertBuff += vert.toBytes()
        bs.seek(0x4,NOESEEK_REL)
    for _ in range(vertCount):
        normal = NoeVec3.fromBytes(bs.readBytes(12))
        normals += normal.toBytes()
        bs.seek(0x4,NOESEEK_REL)
    for _ in range(vertCount):
        uv = bs.readBytes(8)
        uvs += uv
        bs.seek(0x8,NOESEEK_REL)
    texture = rapi.loadExternalTex(texturename)
    rapi.rpgSetMaterial(texturename)
    rapi.rpgBindPositionBuffer(vertBuff, noesis.RPGEODATA_FLOAT, 12)
    rapi.rpgBindNormalBuffer(normals, noesis.RPGEODATA_FLOAT, 12)
    rapi.rpgBindUV1Buffer(uvs, noesis.RPGEODATA_FLOAT, 8)
    rapi.rpgCommitTriangles(None, noesis.RPGEODATA_USHORT, vertCount, noesis.RPGEO_TRIANGLE)		# auto-generate because faces are consecutive
    rapi.rpgSetOption(noesis.RPGOPT_TRIWINDBACKWARD, 1)
    try:
        mdl = rapi.rpgConstructModel()
    except:
        mdl = NoeModel()

    mdlList.append(mdl)
        
    return 1