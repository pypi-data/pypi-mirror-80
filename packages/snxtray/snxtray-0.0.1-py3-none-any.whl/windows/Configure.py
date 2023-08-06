import wx

class Configure(wx.Frame):

    def __init__(self, parent):
        super(Configure, self).__init__(parent, title="Configure SNX", size=(500, 220))
        self.Center()
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)



        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)

        vbox = wx.BoxSizer(wx.VERTICAL)
        cert_box = wx.BoxSizer(wx.HORIZONTAL)

        cert_label = wx.StaticText(panel, label='SNX Cert:')
        cert_label.SetFont(font)
        cert_box.Add(cert_label, flag=wx.RIGHT, border=8)
        file = wx.FilePickerCtrl(panel)
        cert_box.Add(file, proportion=1)
        vbox.Add(cert_box, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        cert_pass_box = wx.BoxSizer(wx.HORIZONTAL)
        cert_pass_label = wx.StaticText(panel, label="Cert Password:")
        cert_pass_text = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        cert_pass_box.Add(cert_pass_label, flag=wx.RIGHT, border=8)
        cert_pass_box.Add(cert_pass_text, proportion=1)
        vbox.Add(cert_pass_box, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        server_box = wx.BoxSizer(wx.HORIZONTAL)

        server_label = wx.StaticText(panel, label="Server:")
        server_text = wx.TextCtrl(panel)

        server_box.Add(server_label, flag=wx.RIGHT, border=8)
        server_box.Add(server_text, proportion=1)
        vbox.Add(server_box, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        pre_up = wx.BoxSizer(wx.HORIZONTAL)
        cert_label = wx.StaticText(panel, label='SNX Cert:')
        cert_label.SetFont(font)
        cert_box.Add(cert_label, flag=wx.RIGHT, border=8)
        file = wx.FilePickerCtrl(panel)
        cert_box.Add(file, proportion=1)
        vbox.Add(cert_box, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        vbox.Add((-1, 25))

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='Ok', size=(70, 30))
        hbox5.Add(btn1, border=8)
        btn2 = wx.Button(panel, label='Close', size=(70, 30))
        hbox5.Add(btn2, flag=wx.LEFT | wx.BOTTOM, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=10)

        panel.SetSizer(vbox)