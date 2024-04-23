# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import wx
import frame

app = wx.App()
frame = frame.mainFrame(None, 'Курсовая')

frame.Show()
app.MainLoop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
