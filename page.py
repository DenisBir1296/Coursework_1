import wx
import wx.grid
import locale
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure


class figurePage(wx.Panel):
    def __init__(self, parent, get_x, get_y, check, x_label, y_label, value_name, points_name):
        super().__init__(parent)

        locale.setlocale(locale.LC_ALL, '')

        self.get_x = get_x
        self.get_y = get_y
        self.check = check
        self.grid = False
        self.logScale = False
        self.x_label = x_label
        self.y_label = y_label
        self.value_name = value_name

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        graphicSizer = wx.BoxSizer(wx.VERTICAL)

        self.SetSizer(mainSizer)

        figure = Figure(tight_layout=True)
        self.axes = figure.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasWxAgg(self, wx.ID_ANY, figure)
        navToolbar = NavigationToolbar2Wx(self.canvas)

        graphicSizer.Add(navToolbar)
        graphicSizer.Add(self.canvas, proportion=1, flag=wx.ALL | wx.EXPAND)
        graphicSizer.AddSpacer(40)

        self.table = wx.grid.Grid(self)
        self.defaultColor = self.table.GetDefaultCellTextColour()
        self.table.CreateGrid(10, 1)
        self.table.SetColLabelValue(0, points_name)
        self.table.SetRowLabelSize(0)

        self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.draw, self.table)

        mainSizer.Add(graphicSizer, proportion=1, flag=wx.EXPAND | wx.ALL)
        mainSizer.Add(self.table, flag=wx.TOP | wx.LEFT, border=15)

        self.graphics = [None for i in range(self.table.GetNumberRows())]

    def setGrid(self, grid):
        self.grid = grid
        self.show()
        return self

    def setLogScale(self, logScale):
        self.logScale = logScale
        self.show()
        return self

    def reDraw(self):
        for i in range(self.table.GetNumberRows()):
            self.update_figure(i)
        self.show()

    def draw(self, event):
        row = event.GetRow()
        self.update_figure(row)
        self.show()

    def update_figure(self, numb):
        if self.table.GetCellValue(numb, 0):
            try:
                buff = locale.atof(self.table.GetCellValue(numb, 0))
                if not self.check(buff):
                    raise ValueError
                self.graphics[numb] = self.get_y(buff)
                self.table.SetCellTextColour(numb, 0, self.defaultColor)
            except ValueError:
                self.graphics[numb] = None
                self.table.SetCellTextColour(numb, 0, wx.RED)
        else:
            self.graphics[numb] = None

    def show(self):
        self.axes.cla()
        self.axes.grid(self.grid)
        if self.logScale:
            self.axes.set_yscale('log')
        self.axes.set_xlabel(self.x_label)
        self.axes.set_ylabel(self.y_label)
        for i in range(self.table.GetNumberRows()):
            if self.graphics[i] is not None:
                self.axes.plot(self.get_x(), self.graphics[i], label=(self.value_name + self.table.GetCellValue(i, 0)))
                self.axes.legend()
        self.canvas.draw()
