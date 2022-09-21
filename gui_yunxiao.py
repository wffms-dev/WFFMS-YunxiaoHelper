#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import wx
import yunxiao as yx

APP_TITLE = "计算机辅助云校云平台兼容选课"

class YunxiaoMainFrame( wx.Frame):
    textbox_account = None
    textbox_password = None
    button_login = None
    yunxiao = None

    list_courses = None

    def __init__( self, parent, title):
        super( YunxiaoMainFrame, self).__init__( parent, title=title, size=( 550, 400))

        self.CreateStatusBar( number=3);
        self.SetStatusText( "计算机辅助选课图形界面版", 0)
        self.SetStatusText( "尚未登录", 1)
        self.SetStatusText( "", 2)

        panel2 = wx.Panel( self)
        panel1 = wx.Panel( panel2)
        panel_down = wx.Panel( panel2)
        hbox = wx.BoxSizer( wx.HORIZONTAL)
        vbox = wx.BoxSizer( wx.VERTICAL)
        hbox_down = wx.BoxSizer( wx.HORIZONTAL)

        label_account = wx.StaticText( panel1, -1, label="账号：")
        label_password = wx.StaticText( panel1, -1, label="密码：")

        self.textbox_account = wx.TextCtrl( panel1, -1, size=( 150, 20))
        self.textbox_password = wx.TextCtrl( panel1, -1, size=( 150, 20), style=wx.TE_PASSWORD)

        self.button_login = wx.Button( panel1, label="登录")
        self.Bind( wx.EVT_BUTTON, self.DidLoginButtonPressed, self.button_login)

        self.list_courses = wx.ListCtrl( panel_down, size=( 400, 200), style=wx.LC_REPORT)

        hbox.Add( label_account, 0, wx.ALL | wx.EXPAND, 5)
        hbox.Add( self.textbox_account, 0, wx.ALL | wx.EXPAND, 5)
        hbox.Add( label_password, 0, wx.ALL | wx.EXPAND, 5)
        hbox.Add( self.textbox_password, 0, wx.ALL | wx.EXPAND, 5)
        hbox.Add( self.button_login, 0, wx.ALL | wx.EXPAND, 5)

        vbox.Add( panel1, 0)
        vbox.Add( panel_down, 1, wx.EXPAND)

        hbox_down.Add( self.list_courses, 0, wx.EXPAND)
        #vbox.Add( wx.TextCtrl( panel2, style=wx.TE_MULTILINE))

        #for i in range( 3):
        #    self.list_courses.InsertColumn( i, "Column {0}".format( i))
        list_columns = [ "编号", "活动名", "活动ID", "开始时间", "已开始？", "已结束？"]
        for i in range( len( list_columns)):
            iw = 50 # item width
            if( i == 1):
                iw = 100
            self.list_courses.InsertColumn( i, list_columns[i], width = iw)

        panel1.SetSizer( hbox)
        panel2.SetSizer( vbox)
        panel_down.SetSizer( hbox_down)

        # FIXME: delete debug code
        # self.list_courses.Append( [ 1, 2, 3, 4, 5, 6])
        index = self.list_courses.InsertItem( 0, "00")
        self.list_courses.SetItem( index, 1, "没有选课")
        self.list_courses.SetItem( index, 2, "0")
        self.list_courses.SetItem( index, 3, "1919/8/10 11:45:14")
        self.list_courses.SetItem( index, 4, "NO")
        self.list_courses.SetItem( index, 5, "YES")

        panel_down.Fit()
        panel2.Fit()
        self.Show()
    
    def DidLoginButtonPressed( self, event):
        # self.SetStatusText( "正在登录", 1)
        try:
            self.yunxiao = yx.YunXiaoHelper( self.textbox_account.Value, self.textbox_password.Value)
        except:
            self.textbox_account.Enable()
            self.textbox_password.Enable()
            self.button_login.Enable()
            self.SetStatusText( "登录失败", 1)
            return 1
        self.textbox_account.Disable()
        self.textbox_password.Disable()
        self.button_login.Disable()
        self.SetStatusText( "登录完成", 1)
        self.UpdateCourseStatus()

    def UpdateCourseStatus( self):
        courses = self.yunxiao.GetCourse()
        count = len( courses)
        if( count == 0):
            self.SetStatusText( "暂无可选课程", 2)
            self.list_courses.ClearAll()
        else:
            hint = "可选课程数：{0}".format( count)
            self.SetStatusText( hint, 2)
            self.list_courses.ClearAll()

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