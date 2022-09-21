#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
from cProfile import label
from threading import Thread
import wx
# import yunxiao as yx
import yunxiao_union as yxu

APP_TITLE = "计算机辅助云校云平台兼容选课"
TEXT_ABOUT = """Yunxiao-Helper
---Original Author---

神楽坂 奈々原/rinscr3003
https://github.com/rinscr3003

---Contributors---

zhongtn
https://github.com/zhongtn

xioi
https://github.com/xioi

---Project repository---
https://github.com/rinscr3003/WFFMS-YunxiaoHelper"""

class YunxiaoAboutFrame( wx.Frame):
    def __init__( self, parent):
        super( YunxiaoAboutFrame, self).__init__( parent, title = "关于" + APP_TITLE, size = ( 400, 400))
        
        tc = wx.TextCtrl( self, size = ( 400, 300), style = wx.TE_MULTILINE | wx.TE_CENTER | wx.TE_READONLY, value = TEXT_ABOUT)
        tc.Fit()

        font = tc.GetFont()
        font.SetPointSize( 15)
        tc.SetFont( font)

        self.Center()
        self.Show()

class YunxiaoMainFrame( wx.Frame):
    textbox_account = None
    textbox_password = None
    button_login = None
    button_refresh = None
    yunxiao = None

    list_courses = None

    def __init__( self, parent, title):
        super( YunxiaoMainFrame, self).__init__( parent, title=title, size=( 550, 400), style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        # 菜单
        menubar = wx.MenuBar()

        menu_help = wx.Menu()
        item_about = menu_help.Append( -1, item = "关于（&A）", helpString = "显示关于页面")

        menubar.Append( menu_help, "帮助（&H）")
        self.SetMenuBar( menubar)
        self.Bind( wx.EVT_MENU, self.DidAboutSelected, item_about)

        # 状态栏
        self.CreateStatusBar( number=3);
        self.SetStatusText( "计算机辅助选课图形界面版", 0)
        self.SetStatusText( "尚未登录，快去登录", 1)
        self.SetStatusText( "", 2)

        # panel & sizer
        panel2 = wx.Panel( self)
        panel1 = wx.Panel( panel2)
        panel_down = wx.Panel( panel2)
        hbox = wx.BoxSizer( wx.HORIZONTAL)
        vbox = wx.BoxSizer( wx.VERTICAL)
        hbox_down = wx.BoxSizer( wx.HORIZONTAL)

        # 账号密码label
        label_account = wx.StaticText( panel1, -1, label="账号：")
        label_password = wx.StaticText( panel1, -1, label="密码：")

        # 账号密码textbox
        self.textbox_account = wx.TextCtrl( panel1, -1, size=( 150, 20))
        self.textbox_password = wx.TextCtrl( panel1, -1, size=( 150, 20), style=wx.TE_PASSWORD)

        # 登录按钮
        self.button_login = wx.Button( panel1, label="登录")
        self.Bind( wx.EVT_BUTTON, self.DidLoginButtonPressed, self.button_login)

        # 课程列表
        self.list_courses = wx.ListCtrl( panel_down, size=( 550, 300), style = wx.LC_REPORT)

        #
        self.button_refresh = wx.Button( self, label = "无课或获取失败，点击刷新")
        self.Bind( wx.EVT_BUTTON, self.DidRefreshPress, self.button_refresh)

        hbox.Add( label_account, 0, wx.ALL | wx.EXPAND, 5)
        hbox.Add( self.textbox_account, 0, wx.ALL | wx.EXPAND, 5)
        hbox.Add( label_password, 0, wx.ALL | wx.EXPAND, 5)
        hbox.Add( self.textbox_password, 0, wx.ALL | wx.EXPAND, 5)
        hbox.Add( self.button_login, 0, wx.ALL | wx.EXPAND, 5)

        vbox.Add( panel1, 0)
        vbox.Add( panel_down, 1, wx.EXPAND)

        hbox_down.Add( self.list_courses, 0, wx.EXPAND)

        list_columns = [ "编号", "活动名", "活动ID", "开始时间", "已开始？", "已结束？"]
        for i in range( len( list_columns)):
            self.list_courses.InsertColumn( i, list_columns[i], width = 150 if i == 1 or i == 3 else 50)
        self.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.DidCourseListSelected, self.list_courses)

        panel1.SetSizer( hbox)
        panel2.SetSizer( vbox)
        panel_down.SetSizer( hbox_down)

        # FIXME: delete debug code
        self.AddCourseInfo( "00", "没有选课", "0", "1919/8/10 11:45:14", False, True)

        panel_down.Fit()
        panel2.Fit()
        panel1.Fit()
        self.list_courses.Fit()

        self.Bind( wx.EVT_SIZE, self.DidSizeChange, self)

        self.Center()
        self.Show()
    
    def DidSizeChange( self, event):
        sb = self.GetStatusBar()
        r1 = sb.GetFieldRect( 2)
        p1 = sb.GetPosition()
        r1.x += p1.x; r1.y += p1.y
        self.button_refresh.SetRect( r1)
        
    def DidAboutSelected( self, event):
        YunxiaoAboutFrame( self)
    
    def AddCourseInfo( self, num, name, id, start, isbegin, isend):
        index = self.list_courses.InsertItem( 0, num)
        self.list_courses.SetItem( index, 1, name)
        self.list_courses.SetItem( index, 2, id)
        self.list_courses.SetItem( index, 3, start)
        self.list_courses.SetItem( index, 4, "NO" if isbegin else "YES")
        self.list_courses.SetItem( index, 5, "NO" if isend else "YES")
    
    def LoginSync( self, username, password):
        try:
            self.yunxiao = yxu.YunXiaoHelper( username, password)
        except:
            wx.CallAfter( self.textbox_account.Enable)
            wx.CallAfter( self.textbox_password.Enable)
            wx.CallAfter( self.button_login.Enable)

            wx.CallAfter( self.SetStatusText, "登录失败", 1)
            return 1
        wx.CallAfter( self.textbox_account.Disable)
        wx.CallAfter( self.textbox_password.Disable)
        wx.CallAfter( self.button_login.Disable)
        wx.CallAfter( self.SetStatusText, "登录完成", 1)
        wx.CallAfter( self.UpdateCourseStatus)
    
    def DidRefreshPress( self, event):
        self.UpdateCourseStatus()

    def DidCourseListSelected( self, event):
        print( event.GetIndex())
    
    def DidLoginButtonPressed( self, event):
        self.SetStatusText( "正在登录", 1)

        username = self.textbox_account.GetValue()
        password = self.textbox_password.GetValue()

        self.textbox_account.Disable()
        self.textbox_password.Disable()
        self.button_login.Disable()

        self.textbox_account.SetValue( username)
        self.textbox_password.SetValue( password)

        thread_login = Thread( None, self.LoginSync, "login", [ username, password])
        thread_login.setDaemon( True)
        thread_login.start()
    
    def GetCoursesSync( self):
        courses = self.yunxiao.GetCourse()
        count = len( courses)
        if count == 0: # 没课或失败
            pass
        else: # 有课
            pass

    def UpdateCourseStatus( self):
        self.button_refresh.Disable()
        """ courses = self.yunxiao.GetCourse()
        count = len( courses)
        if( count == 0):
            self.SetStatusText( "暂无可选课程", 2)
            self.list_courses.ClearAll()
        else:
            hint = "可选课程数：{0}，双击课程以打开".format( count)
            self.SetStatusText( hint, 2)
            self.list_courses.ClearAll() """

class YunxiaoSelectorFrame( wx.Frame):
    yunxiao = None

    def __init__( self, parent, yunxiao):
        super( YunxiaoSelectorFrame, self).__init__( parent, title = "", size = ( 400, 400))
        self.yunxiao = yunxiao

        self.Show()

if __name__ == "__main__":
    app = wx.App()
    frm = YunxiaoMainFrame( None, title=APP_TITLE)
    app.MainLoop()