# Spongebob Bowling
# Noesis script by Dave, 2022


from inc_noesis import *


def registerNoesisTypes():
	handle = noesis.register("Spongebob Bowling",".g3")
	noesis.setHandlerTypeCheck(handle, bcCheckType)
	noesis.setHandlerLoadModel(handle, bcLoadModel)
	return 1


# Check file type

def bcCheckType(data):
	return 1


# Read the model data

def bcLoadModel(data, mdlList):
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    ctx = rapi.rpgCreateContext()
    bs.seek(0x8e)
    type = bs.readShort()
    if (type == 592):
        getTex(data)
        print("Texture Saved to " + os.path.splitext(rapi.getInputName())[0] + ".png")
    if (type == 816):
        getTex1(data)
        print("Texture Saved to " + os.path.splitext(rapi.getInputName())[0] + ".png")
    if (type != 592):
        if (type == 296):
            bs.seek(0x158)
        if (type == 212):
            bs.seek(0x134)
        else:
            print("Not Supported")
        faceCount = bs.readShort()
        vertexCount = bs.readShort()
        vertBuff = bytes()
        faceBuff = bytes()
        normalBuff = bytes()
        uvBuff = bytes()
        if (type == 296):
            bs.seek(0x184)
            vert_data = 0x184
        if (type == 212):
            bs.seek(0x160)
            vert_data = 0x160
        else:
            print("Not Supported")
        norm_data = vert_data + (vertexCount*12)
        face_data = vert_data + (vertexCount*12) + (vertexCount*12)

        vertices = bytearray(faceCount * 0x24)
        normals = bytearray(faceCount * 0x24)
        uvs = bytearray(faceCount * 0x18)

    # Read face buffer to rebuild vertex/norma/UV buffers

        for a in range(faceCount):
            bs.seek(face_data + (a * 0x28))
            bs.readUInt()
            f1 = bs.readUInt()
            uv1x = bs.readFloat()
            uv1y = bs.readFloat()
            f2 = bs.readUInt()
            uv2x = bs.readFloat()
            uv2y = bs.readFloat()
            f3 = bs.readUInt()
            uv3x = bs.readFloat()
            uv3y = bs.readFloat()

            bs.seek(vert_data + (f1 * 12))
            verts = bs.read("3f")
            bs.seek(norm_data + (f1 * 12))
            norms = bs.read("3f")
            struct.pack_into("fff", vertices, a * 36, *verts)
            struct.pack_into("fff", normals, a * 36, *norms)

            bs.seek(vert_data + (f2 * 12))
            verts = bs.read("3f")
            bs.seek(norm_data + (f2 * 12))
            norms = bs.read("3f")
            struct.pack_into("fff", vertices, a * 36 + 12, *verts)
            struct.pack_into("fff", normals, a * 36 + 12, *norms)

            bs.seek(vert_data + (f3 * 12))
            verts = bs.read("3f")
            bs.seek(norm_data + (f3 * 12))
            norms = bs.read("3f")
            struct.pack_into("fff", vertices, a * 36 + 24, *verts)
            struct.pack_into("fff", normals, a * 36 + 24, *norms)

            struct.pack_into("ffffff", uvs, a * 0x18, uv1x, uv1y, uv2x, uv2y, uv3x, uv3y)

        texName = os.path.splitext(rapi.getInputName())[0]
        getTex(data)
        rapi.rpgSetMaterial(os.path.splitext(rapi.getInputName())[0] + ".png")
        print(os.path.splitext(rapi.getInputName())[0] + ".png")
        rapi.rpgBindPositionBuffer(vertices, noesis.RPGEODATA_FLOAT, 12)
        rapi.rpgBindUV1Buffer(uvs, noesis.RPGEODATA_FLOAT, 8)
        rapi.rpgBindNormalBuffer(normals, noesis.RPGEODATA_FLOAT, 12)

        rapi.rpgCommitTriangles(None, noesis.RPGEODATA_USHORT, faceCount * 3, noesis.RPGEO_TRIANGLE)		# auto-generate because faces are consecutive


        try:
            mdl = rapi.rpgConstructModel()
        except:
            mdl = NoeModel()

        mdlList.append(mdl)
        
        return 1
def findall(p, s):
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)
def getTex(data):
    bs = NoeBitStream(data)
    result = [(i+3) for i in findall(b'tmp', data)]
    print(result)
    bs.seek(result[0]+89)
    texWidth = bs.readShort()
    texHeight = bs.readShort()
    bs.seek(12,NOESEEK_REL)
    texName = os.path.splitext(rapi.getInputName())[0]
    texData = bs.readBytes(texWidth * texHeight * 3)
    data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "R8G8B8")
    noesis.saveImageRGBA(os.path.splitext(rapi.getInputName())[0],NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))

def getTex1(data):
    bs = NoeBitStream(data)
    result = [(i+3) for i in findall(b'tmp', data)]
    print(result)
    bs.seek(result[0]+125)
    texWidth = bs.readShort()
    texHeight = bs.readShort()
    texName = os.path.splitext(rapi.getInputName())[0]
    bs.seek(12,NOESEEK_REL)
    texData = bs.readBytes(texWidth * texHeight * 3)
    data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "R8G8B8")
    noesis.saveImageRGBA(os.path.splitext(rapi.getInputName())[0],NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))