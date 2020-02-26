from wx_gui import *
import wx
import wx.xrc
import re
import math
#import Gerenator

font_name = ''
font_dict = {}
list_ctrl_id = 0

def MessageDialog(self, level, msg):
    if level == wx.LOG_Warning: # 1
        dialog = wx.MessageDialog(None, message=msg, caption='Warning', style=wx.ICON_WARNING | wx.OK)
    elif level == wx.LOG_Error: # 2
        dialog = wx.MessageDialog(None, message=msg, caption='Error', style=wx.ICON_ERROR | wx.OK)
    elif level == wx.LOG_User:
        dialog = wx.MessageDialog(None, message=msg, caption='Confirmation', style=wx.ICON_INFORMATION | wx.OK | wx.CANCEL)
    elif level == wx.LOG_Message:
        dialog = wx.MessageDialog(None, message=msg, caption='Message', style=wx.ICON_INFORMATION | wx.OK)

    res = dialog.ShowModal()
    dialog.Destroy()
    return res 

class Frame_Gerenate(Gerenate):
    def __init__(self, parent, font_size):
        super(Frame_Gerenate, self).__init__(parent, font_size)
        self.clientdc = wx.ClientDC(self)
        self.dc = wx.BufferedDC(dc = self.clientdc, area = wx.Size(font_size, font_size), style=wx.BUFFER_CLIENT_AREA)
        self.parent = parent
        self.parent.Disable()
        self.brush = wx.Brush("white")  
        self.dc.SetBackground(self.brush)  
        #font_dict[self.listctrl_fontinfo.GetItemText(0, 3)]

    def OnClose_Cb( self, event):
        self.parent.Enable()
        self.Destroy()

    def RenderBitmap(self, unicode, font_size):
        self.dc.Clear()
        self.dc.DrawText(chr(unicode), 0, 0)
        #print('%04X' %unicode)
        #self.dc.DrawText('%04X' %unicode, font_size, 0)

        bitmap = []
        for y in range(0, font_size):
            line = ''
            for x in range(0, font_size):
                color = self.dc.GetPixel(x, y)
                if color.blue < 200 or color.red < 200 or color.green < 200:
                    line += '1'
                else:
                    line += '0'
            bitmap.append(line)

        return bitmap
    
    def GetBlockStart(self, elem):
        return elem[0]

    def GetBitmapAttribute(self, bitmap, unicode, font_spacing, font_size):
        width = 0
        x_start = 999
        x_end = 0
        y_start = 999
        y_end = 0
        for line in range(0, font_size):
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

        x_offset = font_spacing
        y_offset = font_size - y_start

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
            return [[], [], font_size/2, 0, font_size/2, 0, 0, unicode]
        if width == 0 or height == 0:
            return [[], [], 0, 0, 0, 0, 0, unicode]
        return [hex_bitmap, valid_bitmap, width, height, width+font_spacing*2, font_spacing, -y_offset, unicode]
            
    def Generate(self, blocks, font_spacing, font_size, filename):
        dst = open('%s.h' %filename, "w")
        blocks.sort(key = self.GetBlockStart)
        unicode_start = blocks[0][0]
        unicode_end = blocks[-1][1]

        # Write Bitmap
        dst.write('/* This file is automatically generated by a Unicode to GFX script */\n')
        dst.write('/* by icyqwq@gmail.com */\n\n')
        dst.write('#ifndef _%s_H_\n' %filename)
        dst.write('#define _%s_H_\n' %filename)
        dst.write('const uint8_t %sBitmaps[] PROGMEM = {\n' %filename)

        size = len(blocks) * 6
        x_cursor = 0
        gfxglyph_buffer = []
        bitmap_offset = 0
        base_list = []
        base_list.append(0)
        base = 0
        for block in blocks:
            block[2].SetPixelSize(wx.Size(0, font_size))
            self.dc.SetFont(block[2])
            print('0x%04X - 0x%04X' %(block[0], block[1]))
            for unicode in range(block[0], block[1] + 1):
                self.parent.button_gen.SetLabelText('%04X' %unicode)
                base += 1
                glyph = self.GetBitmapAttribute(self.RenderBitmap(unicode, font_size), unicode, font_spacing, font_size)
                gfxglyph_buffer.append('{0x%X, %d, %d, %d, %d, %d}, /* 0x%04X */\n' %(bitmap_offset, glyph[2], glyph[3], glyph[4], glyph[5], glyph[6], glyph[7]))
                size += 7
                bitmap_offset += len(glyph[0])
                for hexstr in glyph[0]:
                    dst.write('%s, ' %hexstr)
                    size += 1
                    x_cursor += 1
                    if x_cursor == 10:
                        x_cursor = 0
                        dst.write('\n')
                x_cursor = 0
                dst.write('/* 0x%04X */\n' %glyph[7])
            base_list.append(base)
        dst.seek(dst.tell()-2)
        dst.write('};\n\n')

        # Write GFXglyph
        dst.write('/* bitmapOffset, width, height, xAdvance, xOffset, yOffset */\n')
        dst.write('const GFXglyph %sGlyphs[] PROGMEM = {\n' %filename)
        for line in gfxglyph_buffer:
            dst.write(line)
        dst.seek(dst.tell()-16)
        dst.write('};/* 0x%04X */\n\n' %(unicode))

        base_list.pop()
        if len(blocks) is not len(base_list):
            print("Error %d != %d" %(len(blocks), len(base_list)))

        #Write Index
        dst.write('const EncodeRange %sEncodeRange[] PROGMEM = {\n' %filename)
        for i in range(0, len(blocks)):
            dst.write('{0x%04X, 0x%04X, 0x%04X},\n' %(blocks[i][0], blocks[i][1], base_list[i]))
        dst.seek(dst.tell()-3)
        dst.write('};\n\n')

        #Write GFXfont
        dst.write('const GFXfont %s PROGMEM = {\n' %filename)
        dst.write('(uint8_t  *) %sBitmaps,\n' %filename)
        dst.write('(GFXglyph  *) %sGlyphs,\n' %filename)
        dst.write('0x%04X, 0x%04X, %d, ' %(unicode_start, unicode_end, font_size+font_spacing))
        dst.write('%d,\n' %len(base_list))
        dst.write('(EncodeRange  *) %sEncodeRange};\n\n' %filename)

        #End
        dst.write('/* Approx. %.1f KiB */\n\n' %(size/1024.0))
        dst.write('#endif\n')
        dst.close()
        self.OnClose_Cb(None)
        return size


class Frame_MainFrame(MainFrame):
    fontinfo_onselect = []
    fontinfo_list = []

    def __init__(self, parent):
        super(Frame_MainFrame, self).__init__(parent)
        self.listctrl_fontinfo.InsertColumn(0, 'Font', width = 100 )
        self.listctrl_fontinfo.InsertColumn(1, 'Unicode Start', width = 100)
        self.listctrl_fontinfo.InsertColumn(2, 'Unicode End', width = 100)
        self.listctrl_fontinfo.InsertColumn(3, 'ID', width = 0)
        self.dc = wx.ClientDC(self)

    def OnListItemSelect_Cb( self, event ):
        self.fontinfo_onselect.clear()
        item = self.listctrl_fontinfo.GetFirstSelected()
        while item != -1:
            self.fontinfo_onselect.append(item)
            item = self.listctrl_fontinfo.GetNextSelected(item)

    def ButtonAdd_Cb( self, event ):
        font_name = ''
        frame = Frame_NewFont(parent=self)
        frame.Show()

    def ButtonDelete_Cb( self, event ):
        for item in self.fontinfo_onselect:
            font_dict.pop(self.listctrl_fontinfo.GetItemText(item, 3))
            self.listctrl_fontinfo.DeleteItem(item)

    def Gerenate_Cb( self, event ):  
        global unicode_block_list      

        unicode_block_list = []
        try:
            item = -1
            while True:
                item = self.listctrl_fontinfo.GetNextItem(item)
                if item == -1:
                    break
                unicode_block_list.append((int(self.listctrl_fontinfo.GetItemText(item, 1), 16),\
                                        int(self.listctrl_fontinfo.GetItemText(item, 2), 16), \
                                        font_dict[self.listctrl_fontinfo.GetItemText(item, 3)] ))
            if len(unicode_block_list) == 0:
                raise Exception
        except:
            MessageDialog(self, wx.LOG_Warning, 'No valid font and unicode block')
            return

        font_size = 24
        font_spacing = 1
        try:
            font_size = int(self.InputBox_Size.GetValue())
            if font_size <= 3 or font_size >= 99:
                raise Exception
        except:
            MessageDialog(self, wx.LOG_Warning, 'Invalid size')
            return

        try:
            font_spacing = int(self.InputBox_Spacing.GetValue())
            if font_spacing <= 0 or font_spacing >= 10:
                raise Exception
        except:
            MessageDialog(self, wx.LOG_Warning, 'Invalid spacing')
            return

        filename = self.InputBox_FontName.GetValue()
        if 'Enter a font name' in filename or len(filename) < 1:
            filename = 'M5_Font'
        filename = "%s_%dpx" %(filename, font_size)

        self.Disable()
        self.button_gen.SetLabelText('Generating...')
        frame = Frame_Gerenate(parent=self, font_size = font_size)
        #frame.Show()
        flash_size = frame.Generate(unicode_block_list, font_spacing, font_size, filename)
        MessageDialog(self, wx.LOG_Message, '%s Generated, Approx. %.1f KiB' %(filename, flash_size/1024.0))
        self.Enable()
        self.button_gen.SetLabelText('Gerenate')
        print(('Done, Approx. %.1f KiB' %(flash_size/1024.0)))
        

class Frame_NewFont(NewFont):
    def __init__(self, parent):
        super(Frame_NewFont, self).__init__(parent)
        self.parent = parent
        self.parent.Disable()

    def OnFontChanged_Cb( self, event ):
        global font_name
        font_name = self.fontPicker.GetSelectedFont().GetFaceName()
        self.StaticText_FontFileName.SetLabelText(font_name[0:20])

    def FrameOnClose_Cb( self, event ):
        self.parent.Enable()
        self.Destroy()

    def check_unicode_range(self, unicode_start, unicode_end):
        global list_ctrl_id
        global font_dict

        if unicode_start > unicode_end or unicode_start < 0 or unicode_end > 0xFFFF:
            raise Exception('Invalid Unicode Block: start bigger than end')

        unicode_block_list = []
        item = -1
        while True:
            item = self.parent.listctrl_fontinfo.GetNextItem(item)
            if item == -1:
                break
            unicode_block_list.append((int(self.parent.listctrl_fontinfo.GetItemText(item, 1), 16),\
                                       int(self.parent.listctrl_fontinfo.GetItemText(item, 2), 16)))

        for block in unicode_block_list:
            if unicode_start >= block[0] and unicode_start <= block[1]:
                raise Exception('Conflict Unicode Block: start in other block (0x%04X - 0x%04X)' %(block[0], block[1]))
            if unicode_end >= block[0] and unicode_end <= block[1]:
                raise Exception('Conflict Unicode Block: end in other block (0x%04X - 0x%04X)' %(block[0], block[1]))
            if block[0] >= unicode_start and block[0] <= unicode_end:
                raise Exception('Conflict Unicode Block: other block in this block (0x%04X)' %block[0])
            if block[1] >= unicode_start and block[1] <= unicode_end:
                raise Exception('Conflict Unicode Block: other block in this block (0x%04X)' %block[1])

        self.parent.listctrl_fontinfo.Append([font_name, '0x%04X' %unicode_start, '0x%04X' %unicode_end, '%d' %list_ctrl_id])
        font_dict['%d' %list_ctrl_id] = self.fontPicker.GetSelectedFont()
        list_ctrl_id += 1

    def ButtonOK_Cb( self, event ):
        global font_name
        # global list_ctrl_id
        # global font_dict

        try:
            if len(font_name) <= 0:
                raise Exception('Invalid Font')

            checkboxs = [
                'checkbox_0020_002f',
                'checkbox_0030_0039',
                'checkbox_003a_0040',
                'checkbox_0041_005a',
                'checkbox_005b_0060',
                'checkbox_0061_007a',
                'checkbox_007b_007e',
            ]

            checked = 0
            for checkbox_name in checkboxs:
                checkbox = getattr(self, checkbox_name)
                if checkbox.GetValue():
                    checked += 1
                    unicode_range = checkbox_name.replace('checkbox_', '').split('_')
                    unicode_start = int(f'0x{unicode_range[0]}', 16)
                    unicode_end = int(f'0x{unicode_range[1]}', 16)
                    self.check_unicode_range(unicode_start, unicode_end)

            if not checked > 0 and not self.checkbox_custom.GetValue() and not self.checkbox_parsing.GetValue():
                raise Exception('Please choose least one option')

            if self.checkbox_custom.GetValue():
                unicode_start = int(self.textbox_unicode_start.GetValue(), 16)
                unicode_end = int(self.textbox_unicode_end.GetValue(), 16)
                self.check_unicode_range(unicode_start, unicode_end)

            if self.checkbox_parsing.GetValue():
                characters = self.textbox_characters.GetValue()
                if not characters:
                    raise Exception('Please input least one character')
                else:
                    word_list = []

                    for c in characters:
                        word_list.append(c)

                    word_list = list(set(word_list))

                    for t in word_list:
                        code = int(hex(ord(t)), 16)
                        self.check_unicode_range(code, code)

            self.FrameOnClose_Cb(event)
        except Exception as err:
            MessageDialog(self, wx.LOG_Warning, str(err))

    def ButtonCancel_Cb( self, event ):
        self.FrameOnClose_Cb(event)

    def __del__( self ):
        pass

app = wx.App(False)
frame = Frame_MainFrame(parent=None)
frame.Show()
app.MainLoop()