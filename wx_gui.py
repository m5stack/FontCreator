# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"M5-FontCreator", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		fgSizer1 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.listctrl_fontinfo = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,220 ), wx.LC_HRULES|wx.LC_REPORT|wx.LC_SORT_ASCENDING )
		bSizer3.Add( self.listctrl_fontinfo, 0, wx.ALL|wx.EXPAND, 5 )


		fgSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )

		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		self.button_add = wx.Button( self, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.button_add, 0, wx.ALL|wx.EXPAND, 5 )

		self.button_delete = wx.Button( self, wx.ID_ANY, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.button_delete, 0, wx.ALL|wx.EXPAND, 5 )

		fgSizer51 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer51.SetFlexibleDirection( wx.BOTH )
		fgSizer51.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, u"Font Spacing", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText21.Wrap( -1 )

		fgSizer51.Add( self.m_staticText21, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.InputBox_Spacing = wx.TextCtrl( self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 25,-1 ), 0 )
		self.InputBox_Spacing.SetMaxLength( 1 )
		self.InputBox_Spacing.SetMinSize( wx.Size( 25,-1 ) )
		self.InputBox_Spacing.SetMaxSize( wx.Size( 25,-1 ) )

		fgSizer51.Add( self.InputBox_Spacing, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

		self.m_staticText211 = wx.StaticText( self, wx.ID_ANY, u"Font Size(px)", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText211.Wrap( -1 )

		fgSizer51.Add( self.m_staticText211, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.InputBox_Size = wx.TextCtrl( self, wx.ID_ANY, u"24", wx.DefaultPosition, wx.Size( 25,-1 ), 0 )
		self.InputBox_Size.SetMaxLength( 2 )
		self.InputBox_Size.SetMinSize( wx.Size( 25,-1 ) )
		self.InputBox_Size.SetMaxSize( wx.Size( 25,-1 ) )

		fgSizer51.Add( self.InputBox_Size, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer5.Add( fgSizer51, 1, wx.EXPAND, 5 )

		self.InputBox_FontName = wx.TextCtrl( self, wx.ID_ANY, u"Enter a font name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.InputBox_FontName.SetMaxLength( 20 )
		bSizer5.Add( self.InputBox_FontName, 0, wx.ALL, 5 )

		self.button_gen = wx.Button( self, wx.ID_ANY, u"Gerenate", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.button_gen, 0, wx.ALL|wx.EXPAND, 5 )


		fgSizer1.Add( bSizer5, 1, wx.EXPAND, 5 )


		bSizer1.Add( fgSizer1, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.listctrl_fontinfo.Bind( wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelect_Cb )
		self.button_add.Bind( wx.EVT_BUTTON, self.ButtonAdd_Cb )
		self.button_delete.Bind( wx.EVT_BUTTON, self.ButtonDelete_Cb )
		self.button_gen.Bind( wx.EVT_BUTTON, self.Gerenate_Cb )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnListItemSelect_Cb( self, event ):
		event.Skip()

	def ButtonAdd_Cb( self, event ):
		event.Skip()

	def ButtonDelete_Cb( self, event ):
		event.Skip()

	def Gerenate_Cb( self, event ):
		event.Skip()


###########################################################################
## Class NewFont
###########################################################################

class NewFont ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"NewFont", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		fgSizer4 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		bSizer9 = wx.BoxSizer( wx.VERTICAL )

		fgSizer3 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.fontPicker = wx.FontPickerCtrl( self, wx.ID_ANY, wx.Font( 24, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.fontPicker.SetMaxPointSize( 100 )
		fgSizer3.Add( self.fontPicker, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.StaticText_FontFileName = wx.StaticText( self, wx.ID_ANY, u"Please Select Font", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.StaticText_FontFileName.Wrap( -1 )

		fgSizer3.Add( self.StaticText_FontFileName, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer9.Add( fgSizer3, 1, wx.EXPAND, 5 )

		fgSizer2 = wx.FlexGridSizer( 0, 4, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Unicode Block", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		fgSizer2.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.textbox_unicode_start = wx.TextCtrl( self, wx.ID_ANY, u"0x0000", wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.textbox_unicode_start.SetMaxLength( 6 )
		fgSizer2.Add( self.textbox_unicode_start, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"to", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		fgSizer2.Add( self.m_staticText9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.textbox_unicode_end = wx.TextCtrl( self, wx.ID_ANY, u"0x0000", wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.textbox_unicode_end.SetMaxLength( 6 )
		fgSizer2.Add( self.textbox_unicode_end, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer9.Add( fgSizer2, 1, wx.EXPAND, 5 )


		fgSizer4.Add( bSizer9, 1, wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		self.m_button8 = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_button8, 0, wx.ALL, 5 )

		self.m_button9 = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_button9, 0, wx.ALL, 5 )


		fgSizer4.Add( bSizer10, 1, wx.EXPAND, 5 )


		bSizer6.Add( fgSizer4, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer6 )
		self.Layout()
		bSizer6.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.FrameOnClose_Cb )
		self.fontPicker.Bind( wx.EVT_FONTPICKER_CHANGED, self.OnFontChanged_Cb )
		self.m_button8.Bind( wx.EVT_BUTTON, self.ButtonOK_Cb )
		self.m_button9.Bind( wx.EVT_BUTTON, self.ButtonCancel_Cb )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def FrameOnClose_Cb( self, event ):
		event.Skip()

	def OnFontChanged_Cb( self, event ):
		event.Skip()

	def ButtonOK_Cb( self, event ):
		event.Skip()

	def ButtonCancel_Cb( self, event ):
		event.Skip()


###########################################################################
## Class Gerenate
###########################################################################

class Gerenate ( wx.Frame ):

	def __init__( self, parent, font_size ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u" ", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( -1,-1 ), wx.Size( -1,-1 ) )
		self.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
		self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )


		bSizer7.Add( ( 180, font_size), 1, wx.EXPAND, 5 )

		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 0,0 ), 0 )
		self.m_staticText8.Wrap( -1 )

		self.m_staticText8.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
		self.m_staticText8.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )

		bSizer7.Add( self.m_staticText8, 0, wx.ALL, 5 )


		self.SetSizer( bSizer7 )
		self.Layout()
		bSizer7.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose_Cb )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnClose_Cb( self, event ):
		event.Skip()


