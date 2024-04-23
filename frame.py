import wx
import enum
import locale
import function
import page
import parameters_grid

class mainFrame(wx.Frame):

    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(1280, 720))

        self.error = 1e-8
        self.numberOfPoints = 300

        self.func = function.mainFunction().set_error(self.error).set_count_of_points(self.numberOfPoints)

        locale.setlocale(locale.LC_ALL, '')

        mainPanel = wx.Panel(self)
        mainBox = wx.BoxSizer(wx.HORIZONTAL)
        parametersBox = wx.BoxSizer(wx.VERTICAL)

        menuBar = wx.MenuBar()

        menuFile = wx.Menu()
        menuFileExitItem = menuFile.Append(wx.ID_SAVEAS, 'Выйти')

        menuEdit = wx.Menu()
        menuEditSettingsItem = menuEdit.Append(wx.ID_SETUP, 'Настройки')

        menuView = wx.Menu()
        self.menuViewGridItem = menuView.Append(wx.ID_ANY, 'Сетка', kind=wx.ITEM_CHECK)
        menuView.AppendSeparator()
        menuViewLineItem = menuView.Append(wx.ID_ANY, 'Линейный масштаб', kind=wx.ITEM_RADIO)
        self.menuViewLogItem = menuView.Append(wx.ID_ANY, 'Логарифмический масштаб', kind=wx.ITEM_RADIO)

        graphicsNotebook = wx.Notebook(mainPanel)

        self.firstPage = page.figurePage(graphicsNotebook, self.func.get_ro, self.func.get_func_on_t,
                                         self.func.check_t, 'Радиус, см', 'Температура, град', 't = ', 'Время, с')
        self.secondPage = page.figurePage(graphicsNotebook, self.func.get_t, self.func.get_func_on_ro,
                                          self.func.check_ro, 'Время, c', 'Температура, град', 'ro = ', 'Радиус, см')

        applyButton = wx.Button(mainPanel, label='Применить')

        fontColor = applyButton.GetForegroundColour()

        class inputParameters(enum.Enum):
            R = 'Радиус, см:', wx.TextCtrl(mainPanel), '12.0', '12.0'
            L = 'Толщина пластины, см:', wx.TextCtrl(mainPanel), '1.0', '1.0'
            K = 'Теплопроводность, Вт/(см*град):', wx.TextCtrl(mainPanel), '0.12', '0.12'
            C = 'Теплоемкость, Дж/(см3*град):', wx.TextCtrl(mainPanel), '2.0', '2.0'
            ALPHA = 'Коэффициент теплоотдачи, Вт/(см2*град):', wx.TextCtrl(mainPanel), '0.001', '0.001'
            T = 'Время, с:', wx.TextCtrl(mainPanel), '500', '500'
            U0 = 'Начальная температура, град:', wx.TextCtrl(mainPanel), '22.0', '22.0'

            def get_value(self):
                try:
                    buff = locale.atof(self.value[1].GetValue())
                    if buff <= 0:
                        raise ValueError
                    self.value[1].SetForegroundColour(fontColor)
                except ValueError:
                    self.value[1].SetForegroundColour(wx.RED)
                    return None
                return buff

        self.inputParameters = inputParameters
        inputFieldsGrid = parameters_grid.parametersGrid(mainPanel, inputParameters)

        graphicsNotebook.InsertPage(0, self.firstPage, '1', select=True)
        graphicsNotebook.InsertPage(1, self.secondPage, '2')

        menuBar.Append(menuFile, 'Файл')
        menuBar.Append(menuEdit, 'Правка')
        menuBar.Append(menuView, 'Вид')

        parametersBox.AddSpacer(80)
        parametersBox.Add(inputFieldsGrid, flag=wx.LEFT, border=25)
        parametersBox.AddStretchSpacer()
        parametersBox.Add(applyButton, flag=wx.RIGHT | wx.BOTTOM | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM, border=30)

        mainBox.Add(parametersBox, flag=wx.EXPAND)
        mainBox.Add(graphicsNotebook, flag=wx.ALL | wx.EXPAND, proportion=1, border=20)

        mainPanel.SetSizer(mainBox)

        self.Bind(wx.EVT_MENU, self.settings, menuEditSettingsItem)
        self.Bind(wx.EVT_BUTTON, self.apply, applyButton)
        self.Bind(wx.EVT_MENU, self.gridSet, self.menuViewGridItem)
        self.Bind(wx.EVT_MENU, self.logViewSet, self.menuViewLogItem)
        self.Bind(wx.EVT_MENU, self.logViewSet, menuViewLineItem)
        self.Bind(wx.EVT_MENU, self.closeWindow, menuFileExitItem)

        self.SetMenuBar(menuBar)
        self.SetMinSize(wx.Size(1000, 600))

    def closeWindow(self, event):
        self.Close()

    def settings(self, event):
        print('settings')
        settingsDialog = wx.Dialog(self, title='Настройки', size=(640, 480))

        settingsBox = wx.BoxSizer(wx.VERTICAL)

        settingsApplyButton = wx.Button(settingsDialog, label='Применить')

        settingsDialog.SetSizer(settingsBox)

        fontColor = self.GetForegroundColour()

        class settingsEnum(enum.Enum):
            COUNT_OF_POINTS = 'Количество точек :', wx.TextCtrl(settingsDialog), '300', str(self.numberOfPoints)
            ERROR = 'Точность :', wx.TextCtrl(settingsDialog), '1e-8', str(self.error)

            def get_value(self):
                try:
                    buff = locale.atof(self.value[1].GetValue())
                    if buff <= 0:
                        raise ValueError
                    self.value[1].SetForegroundColour(fontColor)
                except ValueError:
                    self.value[1].SetForegroundColour(wx.RED)
                    return None
                return buff

        parametersGrid = parameters_grid.parametersGrid(settingsDialog, settingsEnum)

        settingsBox.AddSpacer(60)
        settingsBox.Add(parametersGrid, flag=wx.LEFT, border=20)
        settingsBox.AddStretchSpacer()
        settingsBox.Add(settingsApplyButton, flag=wx.RIGHT | wx.BOTTOM | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM, border=30)

        def applySettings(event):
            error = settingsEnum.ERROR.get_value()
            count = int(settingsEnum.COUNT_OF_POINTS.get_value())
            if (error is not None) & (count is not None):
                self.error = error
                self.numberOfPoints = count

                self.func.set_error(self.error)
                self.func.set_count_of_points(self.numberOfPoints)
                self.firstPage.reDraw()
                self.secondPage.reDraw()

        settingsDialog.Bind(wx.EVT_BUTTON, applySettings, settingsApplyButton)

        settingsDialog.ShowModal()

    def gridSet(self, event):
        self.firstPage.setGrid(self.menuViewGridItem.IsChecked())
        self.secondPage.setGrid(self.menuViewGridItem.IsChecked())

    def logViewSet(self, event):
        self.firstPage.setLogScale(self.menuViewLogItem.IsChecked())
        self.secondPage.setLogScale(self.menuViewLogItem.IsChecked())

    def apply(self, event):
        self.func.set_value(R=self.inputParameters.R.get_value(),
                            l=self.inputParameters.L.get_value(),
                            k=self.inputParameters.K.get_value(),
                            c=self.inputParameters.C.get_value(),
                            alp=self.inputParameters.ALPHA.get_value(),
                            T=self.inputParameters.T.get_value(),
                            U0=self.inputParameters.U0.get_value())
        self.firstPage.reDraw()
        self.secondPage.reDraw()
