# Author: NSA Cloud
# -----General Functions-----#
import bpy
import os
import struct

# ---General Functions---#
os.system("color")  # Enable console colors


class textColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# read unsigned byte from file
def read_ubyte(file_object, endian='<'):
    data = struct.unpack(endian + 'B', file_object.read(1))[0]
    return data


# read signed byte from file
def read_byte(file_object, endian='<'):
    data = struct.unpack(endian + 'b', file_object.read(1))[0]
    return data


# read signed short from file
def read_short(file_object, endian='<'):
    data = struct.unpack(endian + 'h', file_object.read(2))[0]
    return data


# read unsigned short from file
def read_ushort(file_object, endian='<'):
    data = struct.unpack(endian + 'H', file_object.read(2))[0]
    return data


# read unsigned integer from filel
def read_uint(file_object, endian='<'):
    data = struct.unpack(endian + 'I', file_object.read(4))[0]
    return data


# read signed integer from file
def read_int(file_object, endian='<'):
    data = struct.unpack(endian + 'i', file_object.read(4))[0]
    return data


# read unsigned long integer from file
def read_uint64(file_object, endian='<'):
    data = struct.unpack(endian + 'Q', file_object.read(8))[0]
    return data


# read signed long integer from file
def read_int64(file_object, endian='<'):
    data = struct.unpack(endian + 'q', file_object.read(8))[0]
    return data


# read floating point number from file
def read_float(file_object, endian='<'):
    data = struct.unpack(endian + 'f', file_object.read(4))[0]
    return data


# read double from file
def read_double(file_object, endian='<'):
    data = struct.unpack(endian + 'd', file_object.read(8))[0]
    return data


# read null terminated string from file
def read_string(file_object):
    data = ''.join(iter(lambda: file_object.read(1).decode('ascii'), '\x00'))
    return data


def read_unicode_string(file_object):  # Reads unicode string from file into utf-8 string
    wchar = file_object.read(2)
    byteString = wchar
    while wchar != b'\x00\x00':
        wchar = file_object.read(2)
        byteString += wchar
    unicodeString = byteString.decode("utf-16le").replace('\x00', '')
    return unicodeString


# write unsigned byte to file
def write_ubyte(file_object, input, endian='<'):
    data = struct.pack(endian + 'B', input)
    file_object.write(data)


# write signed byte to file
def write_byte(file_object, input, endian='<'):
    data = struct.pack(endian + 'b', input)
    file_object.write(data)


# write signed short to file
def write_short(file_object, input, endian='<'):
    data = struct.pack(endian + 'h', input)
    file_object.write(data)


# write unsigned short to file
def write_ushort(file_object, input, endian='<'):
    data = struct.pack(endian + 'H', input)
    file_object.write(data)


# write unsigned integer to file
def write_uint(file_object, input, endian='<'):
    data = struct.pack(endian + 'I', input)
    file_object.write(data)


# write signed integer to file
def write_int(file_object, input, endian='<'):
    data = struct.pack(endian + 'i', input)
    file_object.write(data)


# write unsigned long integer to file
def write_uint64(file_object, input, endian='<'):
    data = struct.pack(endian + 'Q', input)
    file_object.write(data)


# write unsigned long integer to file
def write_int64(file_object, input, endian='<'):
    data = struct.pack(endian + 'q', input)
    file_object.write(data)


# write floating point number to file
def write_float(file_object, input, endian='<'):
    data = struct.pack(endian + 'f', input)
    file_object.write(data)


# write double to file
def write_double(file_object, input, endian='<'):
    data = struct.pack(endian + 'd', input)
    file_object.write(data)


# write null terminated string to file
def write_string(file_object, input):
    input += '\x00'
    data = bytes(input, 'utf-8')
    file_object.write(data)


def write_unicode_string(file_object, input):  # Writes utf-8 string as utf-16
    data = input.encode('UTF-16LE') + b'\x00\x00'  # Little endian utf16
    file_object.write(data)


def getPaddingAmount(currentPos, alignment):
    padding = (currentPos * -1) % alignment
    return padding


# bitflag operations
def getBit(bitFlag, index):
    return bool((bitFlag >> index) & 1)


def setBit(bitFlag, index):
    return bitFlag | (1 << index)


def unsetBit(bitFlag, index):
    return bitFlag & ~(1 << index)


def raiseError(error, errorCode=999):
    try:
        raise Exception()
    except Exception:
        print(textColors.FAIL + "ERROR: " + error + textColors.ENDC)


def raiseWarning(warning):
    print(textColors.WARNING + "WARNING: " + warning + textColors.ENDC)


def getByteSection(byteArray, offset, size):
    data = byteArray[offset:(offset + size)]
    return data


def removeByteSection(byteArray, offset, size):  # removes specified amount of bytes from byte array at offset
    del byteArray[offset:(offset + size)]  # Deletes directly from the array passed to it


def insertByteSection(byteArray, offset, input):  # inserts bytes into bytearray at offset
    byteArray[offset:offset] = input


def showMessageBox(message="", title="Message Box", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def showErrorMessageBox(message):
    print(textColors.FAIL + "ERROR: " + message + textColors.ENDC)
    showMessageBox(message, title="Error", icon="ERROR")


class ContextExecuterOverride:
    def __init__(self, window, screen, area, region):
        self.window, self.screen, self.area, self.region = window, screen, area, region
        self.legacy = not hasattr(bpy.context, "temp_override")
        if self.legacy:
            self.context = bpy.context.copy()
            self.context['window'] = window
            self.context['screen'] = screen
            self.context['area'] = area
            self.context['region'] = region
        else:
            self.context = bpy.context.temp_override(window=window, screen=screen, area=area, region=region)

    def __enter__(self):
        if not self.legacy:
            self.context.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.legacy:
            self.context.__exit__(self, exc_type, exc_value, traceback)
        return self


class ContextScriptExecuter():

    def __init__(self, area_type, ui_type=None, script=None):
        self.area_type = area_type
        self.ui_type = ui_type if ui_type else area_type
        self.script = script

    def script_content(self, override):
        self.script(override)

    def execute_script(self):
        window = bpy.context.window
        screen = window.screen
        areas = [area for area in screen.areas if area.type == self.area_type]
        area = areas[0] if len(areas) else screen.areas[0]
        prev_ui_type = area.ui_type
        area.ui_type = self.ui_type
        regions = [region for region in area.regions if region.type == 'WINDOW']
        region = regions[0] if len(regions) else None
        with ContextExecuterOverride(window=window, screen=screen, area=area, region=region) as override:
            self.script_content(override)
        area.ui_type = prev_ui_type


def outlinerShowObject(objName):
    if objName in bpy.data.objects:
        obj = bpy.data.objects[objName]
        bpy.context.view_layer.objects.active = obj
        ContextScriptExecuter(
            area_type='OUTLINER',
            script=lambda override: (
                bpy.ops.outliner.show_active(override.context)
                if override.legacy
                else bpy.ops.outliner.show_active()
            )
        ).execute_script()


def operator_exists(idname):
    #from bpy.ops import op_as_string
    try:
        bpy.ops.op_as_string(idname)
        return True
    except:
        return False
