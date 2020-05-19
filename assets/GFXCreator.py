from wx_gui import *
import wx
import wx.xrc
import re
import math
import time
import json
import threading
import queue

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

class Thread_Creator (threading.Thread):
    def __init__(self, threadID, q, unicode_block, parent, font_size, font_spacing, filename):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.queue = q
        self.unicode_block = unicode_block
        self.runFlag = True
        self.exit = False
        self.parent = parent
        self.font_size = font_size
        self.font_spacing = font_spacing
        self.filename = filename

    def run(self):
        print("Start Thread " + self.name)
        self.Process()
        print("Exit Thread " + self.name)

    def isExit(self):
        return self.exit

    def Terminate(self):
        self.runFlag = False

    def Process(self):
        frame = Frame_Gerenate(parent = self.parent, font_size = self.font_size)
        # frame.Show()
        flash_size = frame.Generate(self.unicode_block, self.font_spacing, self.font_size, self.filename)
        self.queue.put(('DONE', flash_size))


class Frame_Gerenate(Gerenate):
    def __init__(self, parent, font_size):
        super(Frame_Gerenate, self).__init__(parent)
        self.dc = wx.MemoryDC()
        self.parent = parent
        self.parent.Disable()
        self.bmp = wx.Bitmap(64, 64, depth=1)

    def OnClose_Cb( self, event):
        self.parent.Enable()
        self.Destroy()

    def RenderBitmap(self, unicode, font_size, ud, lr):
        self.dc.SelectObject(self.bmp)
        self.dc.Clear()

        base_offset = (64 - font_size) // 2
        ox = base_offset + lr
        oy = base_offset + ud
        x = self.dc.DrawText(chr(unicode), ox, oy)

        bitmap = []
        for y in range(base_offset, base_offset + font_size):
            line = ''
            for x in range(base_offset, base_offset + font_size):
                color = self.dc.GetPixel(x, y)
                if color.blue != 255:
                    line += '1'
                else:
                    line += '0'
            bitmap.append(line)

        self.dc.SelectObject(wx.NullBitmap)
        self.Bitmap_Render.SetBitmap(self.bmp)
        self.Bitmap_Render.Update()
        self.m_staticText11.SetLabel('0x%04X' %unicode)

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

        total = 0
        for block in blocks:
            total += block[1] - block[0]
        total += len(blocks)

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
        current_index = 0
        for block in blocks:
            block[2].SetPixelSize(wx.Size(0, font_size))
            self.dc.SetFont(block[2])
            print('0x%04X - 0x%04X' %(block[0], block[1]))

            if block[1] - block[0] > 50:
                for i in range(0, len(self.parent.unicode_range_list)):
                    if self.parent.unicode_range_list[i][0] == block[0]:
                        self.parent.listctrl_fontinfo.SetItemBackgroundColour(i, (0, 192, 0))
                    else:
                        self.parent.listctrl_fontinfo.SetItemBackgroundColour(i, (255, 255, 255))

            for unicode in range(block[0], block[1] + 1):
                current_index += 1
                self.parent.button_gen.SetLabelText('%d / %d' %(current_index, total))
                base += 1
                glyph = self.GetBitmapAttribute(self.RenderBitmap(unicode, font_size, block[3], block[4]), unicode, font_spacing, font_size)
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
        if len(blocks) != len(base_list):
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
        self.unicode_block = []
        self.thread = None
        self.queue_info = queue.Queue(100)
        self.filename = None
        self.unicode_range_list = []

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer_CB)

    def OnTimer_CB(self, event):
        if not self.queue_info.empty():
            queue_data = self.queue_info.get()
            print(queue_data)
            if queue_data[0] == 'DONE':
                flash_size = queue_data[1]
                MessageDialog(self, wx.LOG_Message, '%s Generated, Approx. %.1f KiB' %(self.filename, flash_size/1024.0))
                self.Enable()
                self.button_gen.SetLabelText('Gerenate')
                print(('Done, Approx. %.1f KiB' %(flash_size/1024.0)))
                self.timer.Stop()

    def OnListItemSelect_Cb( self, event ):
        self.fontinfo_onselect.clear()
        item = self.listctrl_fontinfo.GetFirstSelected()
        while item != -1:
            self.fontinfo_onselect.append(item)
            item = self.listctrl_fontinfo.GetNextSelected(item)

    def ButtonAdd_Cb( self, event ):
        frame = Frame_NewFont(parent=self)
        frame.Show()

    def ButtonDelete_Cb( self, event ):
        dellist = []
        for item in self.fontinfo_onselect:
            start = int(self.listctrl_fontinfo.GetItemText(item, 1), 16)
            dellist.append(start)
            # end = int(self.listctrl_fontinfo.GetItemText(item, 2))
            self.listctrl_fontinfo.DeleteItem(item)
        
        for d in dellist:
            for x in self.unicode_block:
                if(x[0] == d):
                    self.unicode_block.remove(x)

    def SaveBlock(self):
        data = {}
        for block in self.unicode_block:
            data.setdefault('0x%04X-0x%04X' %(block[0], block[1]), [block[2].GetNativeFontInfoDesc(), block[3], block[4]])

        json_str = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        fstr = './%s.json' %str(time.strftime("%Y%m%d_%H%M%S", time.localtime()))
        f = open(fstr, 'w')
        f.write(json_str)
        f.close()
        return fstr

    def Button_Save_CB( self, event ):
        fstr = self.SaveBlock()
        MessageDialog(self, wx.LOG_Message, 'Success saved as %s' %fstr)

    def FilePicker_Load_CB( self, event ):
        try:
            fpath = self.FilePicker_Load.GetPath()
            f = open(fpath, 'r')
            data = json.loads(f.read())
            f.close()
        except:
            MessageDialog(self, wx.LOG_Error, 'Can not open file %s' %fpath)

        try:
            self.unicode_block = []
            self.listctrl_fontinfo.DeleteAllItems()
            keys = data.keys()
            for key in keys:
                payload = key.split('-')
                start = int(payload[0], 16)
                end = int(payload[1], 16)
                font = wx.Font(data[key][0])
                ud = data[key][1]
                lr = data[key][2]
                self.unicode_block.append([start, end, font, ud, lr])
                self.listctrl_fontinfo.Append([font.GetFaceName(), payload[0], payload[1]])

            self.unicode_range_list = []
            item = -1
            while True:
                item = self.listctrl_fontinfo.GetNextItem(item)
                if item == -1:
                    break
                self.unicode_range_list.append((int(self.listctrl_fontinfo.GetItemText(item, 1), 16),\
                                        int(self.listctrl_fontinfo.GetItemText(item, 2), 16)))
        except:
            MessageDialog(self, wx.LOG_Error, 'Invalid configuration file')

    def Gerenate_Cb( self, event ):
        self.SaveBlock()
        try:
            if len(self.unicode_block) == 0:
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
        self.filename = "%s_%dpx" %(filename, font_size)

        self.Disable()

        self.thread = Thread_Creator(1, self.queue_info, self.unicode_block, self, font_size, font_spacing, self.filename)
        self.thread.start()
        self.timer.Start(50)

class Frame_NewFont(NewFont):
    def __init__(self, parent):
        super(Frame_NewFont, self).__init__(parent)
        self.parent = parent
        self.parent.Disable()

        self.fontsize = 24
        try:
            self.fontsize = int(self.parent.InputBox_Size.GetValue())
            if self.fontsize <= 3 or self.fontsize >= 99:
                raise Exception
        except:
            MessageDialog(self, wx.LOG_Warning, 'Invalid size')
            self.fontsize = 24

        self.offset_UD = 0
        self.offset_LR = 0
        self.preview_unicode = 0x554A
        self.preview_font = self.fontPicker.GetSelectedFont()
        self.font_name = self.preview_font.GetFaceName()
        self.Textctrl_PreviewUnicode.SetValue('0x%04X' %(self.preview_unicode))
        self.Text_Preview.SetLabel(chr(self.preview_unicode))
        self.Render_Preview()

    def Render_Preview(self):
        unicode = self.preview_unicode
        font = self.preview_font
        UD = self.offset_UD
        LR = self.offset_LR
        font.SetPixelSize(wx.Size(0, self.fontsize))

        bmp = wx.Bitmap(64, 64)
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.Clear()

        dc.SetFont(font)
        base_offset = (64 - self.fontsize) // 2
        x = base_offset + LR
        y = base_offset + UD
        dc.DrawText(chr(unicode), x, y)

        xy = base_offset // 2
        wh = 64 - base_offset
        dc.SetPen(wx.Pen("grey",style=wx.SOLID, width = base_offset))
        dc.SetBrush(wx.Brush("grey", wx.TRANSPARENT))
        dc.DrawRectangle(xy, xy, wh, wh)

        dc.SelectObject(wx.NullBitmap)
        
        self.m_bitmap3.SetBitmap(bmp)
        self.m_bitmap3.Update()

    def Textctrl_PreviewUnicode_Ontext_CB( self, event ):
        try:
            unicode = int(self.Textctrl_PreviewUnicode.GetValue(), 16)
            if unicode > 0 and unicode < 0xFFFF:
                self.preview_unicode = unicode
            self.Text_Preview.SetLabel(chr(unicode))
            self.Render_Preview()
        except:
            pass
    
    def Button_Left_CB( self, event ):
        self.offset_LR -= 1
        self.Text_OffsetLR.SetLabel('Offset LR  = %d' %self.offset_LR)
        self.Render_Preview()

    def Button_Up_CB( self, event ):
        self.offset_UD -= 1
        self.Text_OffsetUD.SetLabel('Offset UD = %d' %self.offset_UD)
        self.Render_Preview()

    def Button_Down_CB( self, event ):
        self.offset_UD += 1
        self.Text_OffsetUD.SetLabel('Offset UD = %d' %self.offset_UD)
        self.Render_Preview()

    def Button_Right_CB( self, event ):
        self.offset_LR += 1
        self.Text_OffsetLR.SetLabel('Offset LR  = %d' %self.offset_LR)
        self.Render_Preview()

    def OnFontChanged_Cb( self, event ):
        self.font_name = self.fontPicker.GetSelectedFont().GetFaceName()
        self.offset_LR = 0
        self.offset_UD = 0
        self.preview_font = self.fontPicker.GetSelectedFont()
        self.Text_Preview.SetLabel(chr(self.preview_unicode))
        self.Render_Preview()

    def FrameOnClose_Cb( self, event ):
        self.parent.Enable()
        self.Destroy()

    def ButtonOK_Cb( self, event ):
        try:
            self.parent.InputBox_Size.Disable()
            unicode_start = int(self.textbox_unicode_start.GetValue(), 16)
            unicode_end = int(self.textbox_unicode_end.GetValue(), 16)
            if unicode_start > unicode_end or unicode_start < 0 or unicode_end > 0xFFFF:
                raise Exception('Invalid Unicode Block: start bigger than end')

            unicode_range_list = []
            item = -1
            while True:
                item = self.parent.listctrl_fontinfo.GetNextItem(item)
                if item == -1:
                    break
                unicode_range_list.append((int(self.parent.listctrl_fontinfo.GetItemText(item, 1), 16),\
                                           int(self.parent.listctrl_fontinfo.GetItemText(item, 2), 16)))

            for block in unicode_range_list:
                if unicode_start >= block[0] and unicode_start <= block[1]:
                    raise Exception('Conflict Unicode Block: start in other block (0x%04X - 0x%04X)' %(block[0], block[1]))
                if unicode_end >= block[0] and unicode_end <= block[1]:
                    raise Exception('Conflict Unicode Block: end in other block (0x%04X - 0x%04X)' %(block[0], block[1]))
                if block[0] >= unicode_start and block[0] <= unicode_end:
                    raise Exception('Conflict Unicode Block: other block in this block (0x%04X)' %block[0])
                if block[1] >= unicode_start and block[1] <= unicode_end:
                    raise Exception('Conflict Unicode Block: other block in this block (0x%04X)' %block[1])
            if len(self.font_name) <= 0:
                raise Exception('Invalid Font: %s' %self.font_name)
            self.parent.listctrl_fontinfo.Append([self.font_name, '0x%04X' %unicode_start, '0x%04X' %unicode_end])
            self.parent.unicode_block.append([unicode_start, unicode_end, self.preview_font, self.offset_UD, self.offset_LR])
            self.parent.unicode_range_list = unicode_range_list
            self.FrameOnClose_Cb(event)
        except Exception as err:
            MessageDialog(self, wx.LOG_Warning, str(err))

    def ButtonCancel_Cb( self, event ):
        self.FrameOnClose_Cb(event)

    def __del__( self ):
        pass

queueLock = threading.Lock()


app = wx.App(False)
frame = Frame_MainFrame(parent=None)
frame.Show()
app.MainLoop()