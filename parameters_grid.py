import wx


class parametersGrid(wx.FlexGridSizer):
    class reset:
        def __init__(self, a):
            self.a = a

        def __call__(self, *args, **kwargs):
            self.a.value[1].SetValue(self.a.value[2])

    def __init__(self, parent, parameters_enum):
        super().__init__(3, gap=wx.Size(25, 10))

        for i in parameters_enum:
            button = wx.BitmapButton(parent, bitmap=wx.ArtProvider.GetBitmap(wx.ART_REDO))
            i.value[1].SetValue(i.value[3])
            self.AddMany([wx.StaticText(parent, label=i.value[0]), i.value[1], button])
            parent.Bind(wx.EVT_BUTTON, self.reset(i), button)
