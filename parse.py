from base64 import decode
from flask import request
import binascii
import struct
import ctypes
HEADER_MASK = 0xF8   
HEADER_LEN_MASK = 0x07
TLV_BIG = 0x06
TLV_EXTRA_BYTE = 0x07
TLV_BIG_LEN_IN_BITS = 0xFE
TLV_EXTRA_BYTE_LEN_IN_BYTES = 0xFD
SUPPORTED_MAJOR_VERSION = 2
SUPPORTED_MINOR_VERSION = 0


req_data = request.data
data = [int(byte) for byte in req_data]

Variable = {
    0: "Null",
    1: "version", 
    2: "CollectionId",
    3: "Command",
    4: "ReturnCode",
    5: "Signature",           #HMAC-SHA256
    6: "CloudPrinterId",
    7: "DeviceDesriptor",
    8: "EpochTimeLastRecvdReply",   #Valid Reply
    9: "EpochTimeCurrRepy",
    10: "CurrentEpochTime",
    11: "CollectionContent",    #RLE Bitmap Encoding
    12: "AppFlags",
    13: "PrinterStatus",
    14: "ReplyExpiration",
    15: "SignatureGcm",
    16: "EncryptedBlock",
    17: "Padding",
    18: "AppFlagsAck",
    19: "Nonce",
    20: "EnhanceGcm",
    31: "ReservedLast"
}
var = ()
decoded_data = dict()     #dictionary to store the decoded data
#Version class
class Version:
    major = 3
    minor = 5

    def __init__(self):
        self.major = SUPPORTED_MAJOR_VERSION
        self.minor = SUPPORTED_MINOR_VERSION

Commands = {
    0: "Reserved",
    1: "GetCollection",
    2: "ChangePollingFreq",
    3: "ChangeRetryGraceCnt"
}

def extractTlvValue(length, vec, idx, currTime):
    if (length == 0) or (len(data[idx:]) < length):
        return -1
    for i in data[idx:idx+length]:
        currTime = (currTime << 8) | str(i)
    return 0


def decodeTlv(num):

    varValue = ((num & HEADER_MASK) >> 3)
    # print("varValue: ", varValue, "and varName = ", Variable[varValue])
    if (varValue > 20):
        pass
    varName = Variable[varValue]

    if ((num & HEADER_LEN_MASK) ==  TLV_BIG):
        length = TLV_BIG_LEN_IN_BITS
    elif ((num & HEADER_LEN_MASK) ==  TLV_EXTRA_BYTE):
        length = TLV_EXTRA_BYTE_LEN_IN_BYTES
    else:
        length = num & HEADER_LEN_MASK
    
    return varName, length

def Parse(data):
    if len(data) == 0:
        return "Error"
    idx = 0
    parsedReplySize = 0
    while(idx != len(data)):
        var = decodeTlv(data[idx])
        varName = var[0]
        length = int(var[1])

        if (varName == "Null"):
            return "Error"
        else:
            parsedReplySize += 1
            if (length == TLV_BIG_LEN_IN_BITS):
                idx += 1
                parsedReplySize += 1
                length = data[idx]
            elif (len == TLV_EXTRA_BYTE_LEN_IN_BYTES):
                parsedReplySize += 1
                idx += 1
                length = 0x0100 | data[idx]

            parsedReplySize += length
        
        if varName == Variable[1]:      #if variable is version
            version = Version()
            idx += 1
            byte = data[idx]
            version.major = (byte & 0x70) >> 5
            version.minor = (byte & 0x1F)
            decoded_data[varName] = str(version.major)+"."+str(version.minor)
            print(varName, ": ", decoded_data[varName])
        
        elif varName == Variable[3]:
            idx += 1
            command = Commands[data[idx]]
            if command == Commands[1]:
                decoded_data[varName] = Commands[1]
            print(varName, ": ", decoded_data[varName])
            
        elif varName == Variable[2]:
            idx += 1
            collectionId = str(data[idx:idx+length])
            idx += length - 1
            decoded_data[varName] = collectionId
            print(varName, ": ", decoded_data[varName])
        
        elif varName == Variable[19]:
            idx += 1
            nonce = str(data[idx:idx+length])
            idx += length - 1
            decoded_data[varName] = nonce
            print(varName, ": ", decoded_data[varName])

        elif varName == Variable[10]:
            idx += 1     
            currentTime = 0
            res = extractTlvValue(length, data, idx+1, currentTime)
            if (res == -1):
                currentTime = 0
                break
            idx += length
            decoded_data[varName] = currentTime
            print(varName, ": ", decoded_data[varName])

        elif varName == Variable[9]:
            idx += 1
            res = extractTlvValue(length, data, idx+1, currentTime)
            if (res == -1):
                currentTime = 0
                break
            idx += length - 1
            decoded_data[varName] = currentTime
            print(varName, ": ", decoded_data[varName])
        
        elif varName == Variable[12]:
            idx += 1
            print("AppFlags: ", data[idx, idx+length])
            idx = idx+length-1
            decoded_data[varName] = str(data[idx, idx+length])
            print(varName, ": ", decoded_data[varName])

        elif varName == Variable[11]:
            idx += 1
            print("CollectionContent: ", data[idx, idx+length])
            idx = idx+length-1
            decoded_data[varName] = str(data[idx, idx+length])
            print(varName, ": ", decoded_data[varName])

        elif varName == Variable[15]:
            idx += 1
            print("SignatureGCM: ", data[idx, idx+length])
            idx = idx+length-1
            decoded_data[varName] = str(data[idx, idx+length])
            print(varName, ": ", decoded_data[varName])
        
        elif varName == Variable[17]:
            idx += 1
            print("Padding: ", data[idx, idx+length])
            idx = idx+length-1
            decoded_data[varName] = str(data[idx, idx+length])
            print(varName, ": ", decoded_data[varName])

        elif varName == Variable[20]:
            idx += 1
            print("EnhanceGcm: ", data[idx, idx+length])
            idx = idx+length-1
            decoded_data[varName] = str(data[idx, idx+length])
            print(varName, ": ", decoded_data[varName])
        idx += 1     
    return decoded_data   




        

            







   




