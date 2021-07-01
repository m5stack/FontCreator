# By icyqwq@gmail.com
# This script converts the unicode.bin font file to a GFX font
# Please try to select consecutive Unicode blocks, otherwise it will waste a lot of memory.
'''
import sys
import math
import re
from PIL import Image
from PIL import ImageFont, ImageDraw

font = ImageFont.truetype("YuGothB.ttc", 30)

mask = font.getmask(u"啊啊啊", mode='1')

size = mask.size
print(size)
for y in (range(0, size[1])):
    for x in (range(0, size[0])):
        #print("%3d " %mask.getpixel((x, y)), end = "")
        
        if mask.getpixel((x, y)) == 255:
            print("■", end = "")
        else:
            print(" ", end = "")
        
    print("")
exit("done")
'''
import sys
import math
import re

UNICODE_BLOCK = []

# Please select the required block here, or customize the block
# For more details on characters, please refer to https://unicode-table.com/cn/
UNICODE_BLOCK.append((0x0000, 0x001F)) # Control character
UNICODE_BLOCK.append((0x0020, 0x007F)) # Basic Latin
#UNICODE_BLOCK.append((0x0080, 0x00FF)) # Latin-1 Supplement
#UNICODE_BLOCK.append((0x0100, 0x017F)) # Latin Extended-A
#UNICODE_BLOCK.append((0x0180, 0x024F)) # Latin Extended-B
#UNICODE_BLOCK.append((0x0250, 0x02AF)) # IPA Extensions
#UNICODE_BLOCK.append((0x02B0, 0x02FF)) # Spacing Modifier Letters
#UNICODE_BLOCK.append((0x0300, 0x036F)) # Combining Diacritical Marks
#UNICODE_BLOCK.append((0x0370, 0x03FF)) # Greek and Coptic
#UNICODE_BLOCK.append((0x0400, 0x04FF)) # Cyrillic
#UNICODE_BLOCK.append((0x0500, 0x052F)) # Cyrillic Supplement
#UNICODE_BLOCK.append((0x0530, 0x058F)) # Armenian
#UNICODE_BLOCK.append((0x0590, 0x05FF)) # Hebrew
#UNICODE_BLOCK.append((0x0600, 0x06FF)) # Arabic
#UNICODE_BLOCK.append((0x0700, 0x074F)) # Syriac
#UNICODE_BLOCK.append((0x0750, 0x077F)) # Arabic Supplement
#UNICODE_BLOCK.append((0x0780, 0x07BF)) # Thaana
#UNICODE_BLOCK.append((0x07C0, 0x07FF)) # NKo
#UNICODE_BLOCK.append((0x0800, 0x083F)) # Samaritan 
#UNICODE_BLOCK.append((0x0840, 0x085F)) # Mandaic
#UNICODE_BLOCK.append((0x0860, 0x086F)) # Syriac Supplement
#UNICODE_BLOCK.append((0x08A0, 0x08FF)) # Arabic Extended-A
#UNICODE_BLOCK.append((0x0900, 0x097F)) # Devanagari
#UNICODE_BLOCK.append((0x0980, 0x09FF)) # Bengali
#UNICODE_BLOCK.append((0x0A00, 0x0A7F)) # Gurmukhi
#UNICODE_BLOCK.append((0x0A80, 0x0AFF)) # Gujarati
#UNICODE_BLOCK.append((0x0B00, 0x0B7F)) # Oriya
#UNICODE_BLOCK.append((0x0B80, 0x0BFF)) # Tamil
#UNICODE_BLOCK.append((0x0C00, 0x0C7F)) # Telugu
#UNICODE_BLOCK.append((0x0C80, 0x0CFF)) # Kannada
#UNICODE_BLOCK.append((0x0D00, 0x0D7F)) # Malayalam
#UNICODE_BLOCK.append((0x0D80, 0x0DFF)) # Sinhala
#UNICODE_BLOCK.append((0x0E00, 0x0E7F)) # Thai
#UNICODE_BLOCK.append((0x0E80, 0x0EFF)) # Lao
#UNICODE_BLOCK.append((0x0F00, 0x0FFF)) # Tibetan
#UNICODE_BLOCK.append((0x1000, 0x109F)) # Myanmar
#UNICODE_BLOCK.append((0x10A0, 0x10FF)) # Georgian
#UNICODE_BLOCK.append((0x1100, 0x11FF)) # Hangul Jamo
#UNICODE_BLOCK.append((0x1200, 0x137F)) # Ethiopic
#UNICODE_BLOCK.append((0x1380, 0x139F)) # Ethiopic Supplement
#UNICODE_BLOCK.append((0x13A0, 0x13FF)) # Cherokee
#UNICODE_BLOCK.append((0x1400, 0x167F)) # Unified Canadian Aboriginal Syllabics
#UNICODE_BLOCK.append((0x1680, 0x169F)) # Ogham
#UNICODE_BLOCK.append((0x16A0, 0x16FF)) # Runic
#UNICODE_BLOCK.append((0x1700, 0x171F)) # Tagalog
#UNICODE_BLOCK.append((0x1720, 0x173F)) # Hanunoo
#UNICODE_BLOCK.append((0x1740, 0x175F)) # Buhid
#UNICODE_BLOCK.append((0x1760, 0x177F)) # Tagbanwa
#UNICODE_BLOCK.append((0x1780, 0x17FF)) # Khmer
#UNICODE_BLOCK.append((0x1800, 0x18AF)) # Mongolian
#UNICODE_BLOCK.append((0x18B0, 0x18FF)) # Unified Canadian Aboriginal Syllabics Extended
#UNICODE_BLOCK.append((0x1900, 0x194F)) # Limbu
#UNICODE_BLOCK.append((0x1950, 0x197F)) # Tai Le
#UNICODE_BLOCK.append((0x1980, 0x19DF)) # New Tai Lue
#UNICODE_BLOCK.append((0x19E0, 0x19FF)) # Khmer Symbols
#UNICODE_BLOCK.append((0x1A00, 0x1A1F)) # Buginese
#UNICODE_BLOCK.append((0x1A20, 0x1AAF)) # Tai Tham
#UNICODE_BLOCK.append((0x1AB0, 0x1AFF)) # Combining Diacritical Marks Extended
#UNICODE_BLOCK.append((0x1B00, 0x1B7F)) # Balinese
#UNICODE_BLOCK.append((0x1B80, 0x1BBF)) # Sundanese
#UNICODE_BLOCK.append((0x1BC0, 0x1BFF)) # Batak
#UNICODE_BLOCK.append((0x1C00, 0x1C4F)) # Lepcha
#UNICODE_BLOCK.append((0x1C50, 0x1C7F)) # Ol Chiki
#UNICODE_BLOCK.append((0x1C80, 0x1C8F)) # Cyrillic Extended C
#UNICODE_BLOCK.append((0x1CC0, 0x1CCF)) # Sundanese Supplement
#UNICODE_BLOCK.append((0x1CD0, 0x1CFF)) # Vedic Extensions
#UNICODE_BLOCK.append((0x1D00, 0x1D7F)) # Phonetic Extensions
#UNICODE_BLOCK.append((0x1D80, 0x1DBF)) # Phonetic Extensions Supplement
#UNICODE_BLOCK.append((0x1DC0, 0x1DFF)) # Combining Diacritical Marks Supplement
#UNICODE_BLOCK.append((0x1E00, 0x1EFF)) # Latin Extended Additional
#UNICODE_BLOCK.append((0x1F00, 0x1FFF)) # Greek Extended
#UNICODE_BLOCK.append((0x2000, 0x206F)) # General Punctuation
#UNICODE_BLOCK.append((0x2070, 0x209F)) # Superscripts and Subscripts
#UNICODE_BLOCK.append((0x20A0, 0x20CF)) # Currency Symbols
#UNICODE_BLOCK.append((0x20D0, 0x20FF)) # Combining Diacritical Marks for Symbols
#UNICODE_BLOCK.append((0x2100, 0x214F)) # Letterlike Symbols
#UNICODE_BLOCK.append((0x2150, 0x218F)) # Number Forms
#UNICODE_BLOCK.append((0x2190, 0x21FF)) # Arrows
#UNICODE_BLOCK.append((0x2200, 0x22FF)) # Mathematical Operators
#UNICODE_BLOCK.append((0x2300, 0x23FF)) # Miscellaneous Technical
#UNICODE_BLOCK.append((0x2400, 0x243F)) # Control Pictures
#UNICODE_BLOCK.append((0x2440, 0x245F)) # Optical Character Recognition
#UNICODE_BLOCK.append((0x2460, 0x24FF)) # Enclosed Alphanumerics
#UNICODE_BLOCK.append((0x2500, 0x257F)) # Box Drawing
#UNICODE_BLOCK.append((0x2580, 0x259F)) # Block Elements
#UNICODE_BLOCK.append((0x25A0, 0x25FF)) # Geometric Shapes
#UNICODE_BLOCK.append((0x2600, 0x26FF)) # Miscellaneous Symbols
#UNICODE_BLOCK.append((0x2700, 0x27BF)) # Dingbats
#UNICODE_BLOCK.append((0x27C0, 0x27EF)) # Miscellaneous Mathematical Symbols-A
#UNICODE_BLOCK.append((0x27F0, 0x27FF)) # Supplemental Arrows-A
#UNICODE_BLOCK.append((0x2800, 0x28FF)) # Braille Patterns
#UNICODE_BLOCK.append((0x2900, 0x297F)) # Supplemental Arrows-B
#UNICODE_BLOCK.append((0x2980, 0x29FF)) # Miscellaneous Mathematical Symbols-B
#UNICODE_BLOCK.append((0x2A00, 0x2AFF)) # Supplemental Mathematical Operators
#UNICODE_BLOCK.append((0x2B00, 0x2BFF)) # Miscellaneous Symbols and Arrows
#UNICODE_BLOCK.append((0x2C00, 0x2C5F)) # Glagolitic
#UNICODE_BLOCK.append((0x2C60, 0x2C7F)) # Latin Extended-C
#UNICODE_BLOCK.append((0x2C80, 0x2CFF)) # Coptic
#UNICODE_BLOCK.append((0x2D00, 0x2D2F)) # Georgian Supplement
#UNICODE_BLOCK.append((0x2D30, 0x2D7F)) # Tifinagh
#UNICODE_BLOCK.append((0x2D80, 0x2DDF)) # Ethiopic Extended
#UNICODE_BLOCK.append((0x2DE0, 0x2DFF)) # Cyrillic Extended-A
#UNICODE_BLOCK.append((0x2E00, 0x2E7F)) # Supplemental Punctuation
#UNICODE_BLOCK.append((0x2E80, 0x2EFF)) # CJK Radicals Supplement
#UNICODE_BLOCK.append((0x2F00, 0x2FDF)) # Kangxi Radicals
#UNICODE_BLOCK.append((0x2FF0, 0x2FFF)) # Ideographic Description Characters
#UNICODE_BLOCK.append((0x3000, 0x303F)) # CJK Symbols and Punctuation
UNICODE_BLOCK.append((0x3040, 0x309F)) # Hiragana
UNICODE_BLOCK.append((0x30A0, 0x30FF)) # Katakana
#UNICODE_BLOCK.append((0x3100, 0x312F)) # Bopomofo
#UNICODE_BLOCK.append((0x3130, 0x318F)) # Hangul Compatibility Jamo
#UNICODE_BLOCK.append((0x3190, 0x319F)) # Kanbun
#UNICODE_BLOCK.append((0x31A0, 0x31BF)) # Bopomofo Extended
#UNICODE_BLOCK.append((0x31C0, 0x31EF)) # CJK Strokes
#UNICODE_BLOCK.append((0x31F0, 0x31FF)) # Katakana Phonetic Extensions
#UNICODE_BLOCK.append((0x3200, 0x32FF)) # Enclosed CJK Letters and Months
#UNICODE_BLOCK.append((0x3300, 0x33FF)) # CJK Compatibility
#UNICODE_BLOCK.append((0x3400, 0x4DBF)) # CJK Unified Ideographs Extension A
#UNICODE_BLOCK.append((0x4DC0, 0x4DFF)) # Yijing Hexagram Symbols
#UNICODE_BLOCK.append((0x4E00, 0x9FFF)) # CJK Unified Ideographs
#UNICODE_BLOCK.append((0xA000, 0xA48F)) # Yi Syllables
#UNICODE_BLOCK.append((0xA490, 0xA4CF)) # Yi Radicals
#UNICODE_BLOCK.append((0xA4D0, 0xA4FF)) # Lisu
#UNICODE_BLOCK.append((0xA500, 0xA63F)) # Vai
#UNICODE_BLOCK.append((0xA640, 0xA69F)) # Cyrillic Extended-B
#UNICODE_BLOCK.append((0xA6A0, 0xA6FF)) # Bamum
#UNICODE_BLOCK.append((0xA700, 0xA71F)) # Modifier Tone Letters
#UNICODE_BLOCK.append((0xA720, 0xA7FF)) # Latin Extended-D
#UNICODE_BLOCK.append((0xA800, 0xA82F)) # Syloti Nagri
#UNICODE_BLOCK.append((0xA830, 0xA83F)) # Common Indic Number Forms
#UNICODE_BLOCK.append((0xA840, 0xA87F)) # Phags-pa
#UNICODE_BLOCK.append((0xA880, 0xA8DF)) # Saurashtra
#UNICODE_BLOCK.append((0xA8E0, 0xA8FF)) # Devanagari Extended
#UNICODE_BLOCK.append((0xA900, 0xA92F)) # Kayah Li
#UNICODE_BLOCK.append((0xA930, 0xA95F)) # Rejang
#UNICODE_BLOCK.append((0xA960, 0xA97F)) # Hangul Jamo Extended-A
#UNICODE_BLOCK.append((0xA980, 0xA9DF)) # Javanese
#UNICODE_BLOCK.append((0xA9E0, 0xA9FF)) # Myanmar Extended-B
#UNICODE_BLOCK.append((0xAA00, 0xAA5F)) # Cham
#UNICODE_BLOCK.append((0xAA60, 0xAA7F)) # Myanmar Extended-A
#UNICODE_BLOCK.append((0xAA80, 0xAADF)) # Tai Viet
#UNICODE_BLOCK.append((0xAAE0, 0xAAFF)) # Meetei Mayek Extensions
#UNICODE_BLOCK.append((0xAB00, 0xAB2F)) # Ethiopic Extended-A
#UNICODE_BLOCK.append((0xAB30, 0xAB6F)) # Latin Extended-E
#UNICODE_BLOCK.append((0xAB70, 0xABBF)) # Cherokee Supplement
#UNICODE_BLOCK.append((0xABC0, 0xABFF)) # Meetei Mayek
#UNICODE_BLOCK.append((0xAC00, 0xD7AF)) # Hangul Syllables
#UNICODE_BLOCK.append((0xD7B0, 0xD7FF)) # Hangul Jamo Extended-B
#UNICODE_BLOCK.append((0xD800, 0xDB7F)) # High Surrogates
#UNICODE_BLOCK.append((0xDB80, 0xDBFF)) # High Private Use Surrogates
#UNICODE_BLOCK.append((0xDC00, 0xDFFF)) # Low Surrogates
#UNICODE_BLOCK.append((0xE000, 0xF8FF)) # Private Use Area
#UNICODE_BLOCK.append((0xF900, 0xFAFF)) # CJK Compatibility Ideographs
#UNICODE_BLOCK.append((0xFB00, 0xFB4F)) # Alphabetic Presentation Forms
#UNICODE_BLOCK.append((0xFB50, 0xFDFF)) # Arabic Presentation Forms-A
#UNICODE_BLOCK.append((0xFE00, 0xFE0F)) # Variation Selectors
#UNICODE_BLOCK.append((0xFE10, 0xFE1F)) # Vertical Forms
#UNICODE_BLOCK.append((0xFE20, 0xFE2F)) # Combining Half Marks
#UNICODE_BLOCK.append((0xFE30, 0xFE4F)) # CJK Compatibility Forms
#UNICODE_BLOCK.append((0xFE50, 0xFE6F)) # Small Form Variants
#UNICODE_BLOCK.append((0xFE70, 0xFEFF)) # Arabic Presentation Forms-B
#UNICODE_BLOCK.append((0xFF00, 0xFFEF)) # Halfwidth and Fullwidth Forms
#UNICODE_BLOCK.append((0xFFF0, 0xFFFF)) # Specials

def MergeUnicodeBlock():
    global UNICODE_BLOCK
    block = []
    start = 0
    flag = True
    for i in range(0, len(UNICODE_BLOCK)-1):
        if flag == True:
            flag = False
            start = UNICODE_BLOCK[i][0]
        if UNICODE_BLOCK[i][1] + 1 == UNICODE_BLOCK[i+1][0]:
            continue
        else:
            flag = True
            block.append((start, UNICODE_BLOCK[i][1]))
    block.append((start, UNICODE_BLOCK[i+1][1]))
    for x in block:
        print("%04X %04X" %(x[0], x[1]))

    UNICODE_BLOCK = block
                
def GetBitmap(unicode):
    global fonts
    fonts.seek(CHARACTER_ADDR_BASE * unicode, 0)
    bitmap = []
    for x in range(0, CHARACTER_SIZE):
        bitmap.append(bin(int(fonts.read(CHARACTER_BYTES).hex(), 16)).replace('0b', '').rjust(CHARACTER_BYTES * 8, '0'))
    
    width = 0
    x_start = 999
    x_end = 0
    y_start = 999
    y_end = 0
    for line in range(0, CHARACTER_SIZE):
        lfind = bitmap[line].find('1')
        if lfind >= 0:
            y_end = line
            if y_start == 999:
                    y_start = line
            if lfind < x_start:
                x_start = lfind
        rfind = bitmap[line].rfind('1')
        if rfind > x_end:
            x_end = rfind
    if x_start > x_end:
        width = 0
    else:
        width = x_end - x_start + 1

    if y_start > y_end:
        height = 0
    else:
        height = y_end - y_start + 1

    x_offset = XGAP
    y_offset = CHARACTER_SIZE - y_start

    valid_bitmap = []
    for y in range(y_start, y_end + 1):
        valid_bitmap.append(bitmap[y][x_start : x_end + 1])

    fullbinstr = ''
    for line in valid_bitmap:
        fullbinstr += line

    hex_bitmap = []
    if len(valid_bitmap):
        nbyte = math.ceil(len(fullbinstr) / 8.0)
        fullbinstr.ljust(nbyte * 8, '0')
        for n in range(nbyte):
            hex_bitmap.append("0x%02X" %int(fullbinstr[n*8 : (n+1)*8], 2))

    if unicode == 0x0020:
        return [[], [], CHARACTER_SIZE/2, 0, CHARACTER_SIZE/2, 0, 0, unicode]
    if width == 0 or height == 0:
        return [[], [], 0, 0, 0, 0, 0, unicode]
    return [hex_bitmap, valid_bitmap, width, height, width+XGAP*2, XGAP, -y_offset, unicode]

def DisplayBitmap(attributes):
    print("Width: %d  Heigth: %d  xAdvance: %d  xOffset: %d  yOffset: %d" %(attributes[2], attributes[3], attributes[4], attributes[5], attributes[6]))
    s = '    '
    for i in range(0, attributes[2]):
        s += '| '
    print(s)
    for x in range(0, len(attributes[1])):
        print('%-2d' %x, end='  ')
        for y in attributes[1][x]:
            if(y == '1'):
                print('■ ', end='')
            else:
                print('  ', end='')
        print('')

def isInBlock(unicode):
    for block in UNICODE_BLOCK:
        if unicode >= block[0] and unicode <= block[1]:
            return True
    return False

MergeUnicodeBlock()
CHARACTER_SIZE = 16
XGAP = 1

try:
    m = re.search('(\w+)', sys.argv[1])
    filename = m.group(1)
except:
    exit('Please specify the correct file name')

try:
    CHARACTER_SIZE = int(sys.argv[2])
except:
    exit('Please specify the correct font size (px)')

try:
    XGAP = int(sys.argv[3])
except:
    XGAP = 1
    print('Unspecified character spacing, using default spacing 1')

CHARACTER_BYTES	= math.ceil(CHARACTER_SIZE / 8.0)
CHARACTER_ADDR_BASE = CHARACTER_SIZE * CHARACTER_BYTES

print('Running...')
    
fonts = open(sys.argv[1], "rb+")
dst = open("%s.h" %filename, "w")


glyph_list = []
for block in UNICODE_BLOCK :
    for unicode in range(block[0], block[1] + 1):
        glyph_list.append(GetBitmap(unicode))

dst.write('/* This file is automatically generated by a Unicode to GFX script */\n')
dst.write('/* by icyqwq@gmail.com */\n\n')
dst.write('#ifndef _%s_H_\n' %filename)
dst.write('#define _%s_H_\n' %filename)
dst.write('const uint8_t %sBitmaps[] PROGMEM = {\n' %filename)

size = 0
x_cursor = 0
for glyph in glyph_list:
    for hexstr in glyph[0]:
        dst.write('%s, ' %hexstr)
        size += 1
        x_cursor += 1
        if x_cursor == 10:
            x_cursor = 0
            dst.write('\n')
    x_cursor = 0
    dst.write('/* 0x%04X */\n' %glyph[7])
dst.seek(dst.tell()-2)
dst.write('};\n\n')

dst.write('/* bitmapOffset, width, height, xAdvance, xOffset, yOffset */\n')
dst.write('const GFXglyph %sGlyphs[] PROGMEM = {\n' %filename)

base_list = []
base_list.append(0)
base = 0
newrange_flag = False
bitmap_offset = 0
unicode_start = UNICODE_BLOCK[0][0]
unicode_end = UNICODE_BLOCK[len(UNICODE_BLOCK)-1][1]
glyph_index = 0
waste_size = 6
for unicode in range(unicode_start, unicode_end + 1):
    if isInBlock(unicode):
        newrange_flag = True
        base += 1
        glyph = glyph_list[glyph_index]
        glyph_index += 1
        dst.write('{0x%X, %d, %d, %d, %d, %d}, /* 0x%04X */\n' %(bitmap_offset, glyph[2], glyph[3], glyph[4], glyph[5], glyph[6], glyph[7]))
        bitmap_offset += len(glyph[0])
        size += 7
    else:
        if newrange_flag is True:
            waste_size += 6
            newrange_flag = False
            base_list.append(base)
        else:
            pass
        #print('Invalid Unicode 0x%04X' %unicode)
        #dst.write('{0, 0, 0, 0, 0, 0}, /* 0x%04X */\n' %(unicode))
        #waste_size += 7
dst.seek(dst.tell()-16)
dst.write('};/* 0x%04X */\n\n' %(unicode))
size += waste_size

if len(UNICODE_BLOCK) is not len(base_list):
    print("Error %d != %d" %(len(UNICODE_BLOCK), len(base_list)))

dst.write('const EncodeRange %sEncodeRange[] PROGMEM = {\n' %filename)
for i in range(0, len(UNICODE_BLOCK)):
    dst.write('{0x%04X, 0x%04X, 0x%04X},\n' %(UNICODE_BLOCK[i][0], UNICODE_BLOCK[i][1], base_list[i]))
dst.seek(dst.tell()-3)
dst.write('};\n\n')

dst.write('const GFXfont %s PROGMEM = {\n' %filename)
dst.write('(uint8_t  *) %sBitmaps,\n' %filename)
dst.write('(GFXglyph  *) %sGlyphs,\n' %filename)
dst.write('0x%04X, 0x%04X, %d, ' %(unicode_start, unicode_end, CHARACTER_SIZE+XGAP))
dst.write('%d,\n' %len(base_list))
dst.write('(EncodeRange  *) %sEncodeRange};\n\n' %filename)

dst.write('/* Approx. %.1f KiB (Waste %d Byte, Memory utilization %.2f%%) */\n\n' %(size/1024.0, waste_size, 100-(waste_size/size)*100))
dst.write('#endif\n')

fonts.close()
dst.close()
exit('Generate successfully, Approx. %.1f KiB (Waste %d Byte, Memory utilization %.2f%%)' %(size/1024.0, waste_size, 100-(waste_size/size)*100))
