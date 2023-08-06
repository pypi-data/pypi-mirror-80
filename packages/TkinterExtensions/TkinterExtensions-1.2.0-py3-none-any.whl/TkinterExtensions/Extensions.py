# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------
from abc import ABC
from typing import Dict

from .Widgets import *




__all__ = [
        'ButtonGrid', 'NumPad',
        ]


class ButtonGrid(TkinterFrame, ABC):
    __buttons: Dict[int, TkinterButton] = { }
    def __init__(self, *, master: TkinterFrame, rows: int = None, cols: int = None, NumberOfButtons: int = None, **kwargs):
        """
            :param kwargs: TkinterButton kwargs
        """
        assert (isinstance(master, TkinterFrame))
        TkinterFrame.__init__(self, master=master)
        self._rows = rows or len(self.ButtonTitles)
        self._cols = cols or 1
        self._NumberOfButtons = NumberOfButtons or self._rows * self._cols

        if len(self.ButtonCommands) != self._NumberOfButtons:
            raise ValueError(f"len(self.ButtonCommands) [ {len(self.ButtonCommands)} ]  does not Match self._NumberOfButtons [ {self._NumberOfButtons} ]")
        if len(self.ButtonTitles) != self._NumberOfButtons:
            raise ValueError(f"len(self.ButtonTitles) [ {len(self.ButtonTitles)} ]  does not Match self._NumberOfButtons [ {self._NumberOfButtons} ]")

        self._MakeGrid(kwargs)
    def _MakeGrid(self, kwargs: dict):
        for r in range(self._rows): self.grid_rowconfigure(r, weight=1)
        for c in range(self._cols): self.grid_columnconfigure(c, weight=1)

        r = 0
        c = 0
        for i in range(self._NumberOfButtons):
            if c >= self._cols:
                r += 1
                c = 0
            self.__buttons[i] = TkinterButton(self, Text=self.ButtonTitles[i], **kwargs)
            self.__buttons[i].grid(row=r, column=c)
            self.__buttons[i].SetCommand(self.ButtonCommands[i])
            c += 1

    def HideAll(self):
        for w in self.__buttons.values(): w.hide()
    def ShowAll(self):
        for w in self.__buttons.values(): w.show()

    def UpdateText(self, Titles: dict = None):
        if Titles is None: Titles = self.ButtonTitles
        if len(Titles) != self._NumberOfButtons: raise ValueError("len(Titles) Doesn't Match NumberOfButtons")

        for i in range(self._NumberOfButtons):
            self.__buttons[i].txt = Titles[i]
    def UpdateCommands(self, commands: dict = { }, kwz: dict = { }, z: dict = { }):
        if len(commands) != self._NumberOfButtons: raise ValueError("len(commands) Doesn't Match NumberOfButtons")

        for i, Command in commands.items():
            widget = self.__buttons[i]
            if i in kwz and kwz[i] is not None and Command:
                widget.cmd = lambda x=kwz[i]: Command(**x)
                widget.configure(command=widget.cmd)
            elif i in z and z[i] is not None and Command:
                widget.cmd = lambda x=z[i]: Command(x)
                widget.configure(command=widget.cmd)
            elif Command:
                widget.configure(command=Command)

    @property
    def ButtonTitles(self) -> dict: raise NotImplementedError()
    @property
    def ButtonCommands(self) -> dict: raise NotImplementedError()





class NumPad(TkinterFrame, ABC):
    """
    delete, slash, star, minus,
    7,      8,     9,    +
    4,      5,     6,    +
    1,      2,     3,    enter
    0,      0,     .,    enter
    """
    __Default: str
    __Checking: str
    __filler: str
    __password: str = None
    KillCondition: bool

    _Colors: dict
    _Entry: TkinterEntry
    _Num0: TkinterButton
    _Num1: TkinterButton
    _Num2: TkinterButton
    _Num3: TkinterButton
    _Num4: TkinterButton
    _Num5: TkinterButton
    _Num6: TkinterButton
    _Num7: TkinterButton
    _Num8: TkinterButton
    _Num9: TkinterButton
    _DOT: TkinterButton
    _Backspace: TkinterButton
    _Enter: TkinterButton
    def __init__(self, master, IsPassword: bool = False, ButtonColors: dict = None,
                 numFont: str = None, entryFont: str = None, controlFont: str = None,
                 default='', checking='', filler: str = '•', **kwargs):
        self._isPassword = IsPassword
        self._Colors = ButtonColors
        self._numFont = numFont
        self._entryFont = entryFont
        self._controlFont = controlFont
        self.__Default = default
        self.__Checking = checking
        self.__filler = filler
        super().__init__(master=master, **kwargs)
        self.Create_Widgets()

    # noinspection DuplicatedCode
    def Create_Widgets(self, columnOffset: float = 0.02, rowOffset: float = 0.02):
        """ Password entry from CreateNumPad """
        singleWidth = 0.23
        singleHeight = 0.19
        columnPos = [round(columnOffset + singleWidth * i + 0.0175 * i, 4) for i in range(4)]
        rowPos5 = [rowOffset if i == 0 else round((singleHeight + .01) * i - rowOffset, 4) for i in range(5)]

        self._Entry = TkinterEntry(master=self, font=self._entryFont, Color=self._Colors).Place(relx=columnPos[0], rely=rowPos5[0], relwidth=0.97, relheight=singleHeight * 0.75)

        self._Num7 = TkinterButton(self, Color=self._Colors, Text='7',
                                   font=self._numFont).SetCommand(self.PushedNumber, z='7').Place(relx=columnPos[0], rely=rowPos5[1],
                                                                                                  relwidth=singleWidth, relheight=singleHeight)  # 7

        self._Num8 = TkinterButton(self, Color=self._Colors, Text='8',
                                   font=self._numFont).SetCommand(self.PushedNumber, z='8').Place(relx=columnPos[1], rely=rowPos5[1],
                                                                                                  relwidth=singleWidth, relheight=singleHeight)  # 8

        self._Num9 = TkinterButton(self, Color=self._Colors, Text='9',
                                   font=self._numFont).SetCommand(self.PushedNumber, z='9').Place(relx=columnPos[2], rely=rowPos5[1],
                                                                                                  relwidth=singleWidth, relheight=singleHeight)  # 9

        self._Num4 = TkinterButton(self, Color=self._Colors, Text='4',
                                   font=self._numFont).SetCommand(self.PushedNumber, z='4').Place(relx=columnPos[0], rely=rowPos5[2],
                                                                                                  relwidth=singleWidth, relheight=singleHeight)  # 4
        self._Num5 = TkinterButton(self, Color=self._Colors, Text='5',
                                   font=self._numFont).SetCommand(self.PushedNumber, z='5').Place(relx=columnPos[1], rely=rowPos5[2],
                                                                                                  relwidth=singleWidth, relheight=singleHeight)  # 5
        self._Num6 = TkinterButton(self, Color=self._Colors, Text='6',
                                   font=self._numFont).SetCommand(self.PushedNumber, z='6').Place(relx=columnPos[2], rely=rowPos5[2],
                                                                                                  relwidth=singleWidth, relheight=singleHeight)  # 6

        self._Num1 = TkinterButton(self, Color=self._Colors, Text='1',
                                   font=self._numFont).SetCommand(self.PushedNumber, z='1').Place(relx=columnPos[0], rely=rowPos5[3],
                                                                                                  relwidth=singleWidth, relheight=singleHeight)  # 1
        self._Num2 = TkinterButton(self, Color=self._Colors, Text='2',
                                   font=self._numFont).SetCommand(self.PushedNumber, z='2').Place(relx=columnPos[1], rely=rowPos5[3],
                                                                                                  relwidth=singleWidth, relheight=singleHeight)  # 2
        self._Num3 = TkinterButton(self, Color=self._Colors, Text='3',
                                   font=self._numFont).SetCommand(self.PushedNumber, z='3').Place(relx=columnPos[2], rely=rowPos5[3],
                                                                                                  relwidth=singleWidth, relheight=singleHeight)  # 3

        self._Num0 = TkinterButton(self, Color=self._Colors, Text='0',
                                   font=self._numFont).SetCommand(self.PushedNumber, z='0').Place(relx=columnPos[0], rely=rowPos5[4],
                                                                                                  relwidth=singleWidth * 2.1, relheight=singleHeight)  # 0
        self._DOT = TkinterButton(self, Color=self._Colors, Text='.',
                                  font=self._numFont).SetCommand(self.PushedNumber, z='.').Place(relx=columnPos[2], rely=rowPos5[4],
                                                                                                 relwidth=singleWidth, relheight=singleHeight)  # .

        self._Backspace = TkinterButton(self, Color=self._Colors, Text='Delete', font=self._controlFont).SetCommand(self.BackspaceCMD)
        self._Backspace.Place(relx=columnPos[3], rely=rowPos5[1], relwidth=singleWidth * 0.95, relheight=singleHeight * 2.05)  # backspace

        self._Enter = TkinterButton(self, Color=self._Colors, Text='Enter', font=self._controlFont).SetCommand(self.EnterCMD)
        self._Enter.Place(relx=columnPos[3], rely=rowPos5[3], relwidth=singleWidth * 0.95, relheight=singleHeight * 2.05)

        self._AdjustPhotos()

    def show(self, *args, **kwargs):
        """        Shows the current Frame.        """
        self.DeleteCMD()
        super().show(*args, **kwargs)

    def PushedNumber(self, Number):
        if self.EntryText == self.__Default or self.EntryText == self.__Checking: self.EntryText = ''

        self.EntryText = self.EntryText + Number
    def DeleteCMD(self): self.EntryText = self.__Default
    def EnterCMD(self, *args, ThreadName: str = 'NumPad.EnterCMD', **kwargs):  raise NotImplementedError()
    def BackspaceCMD(self):
        if self.EntryText == self.__Default or self.EntryText == self.__Checking: self.EntryText = ''

        value = self.EntryText
        self.EntryText = value[:-1]

    @property
    def EntryText(self) -> str: return self.__password if self._isPassword else ''
    @EntryText.setter
    def EntryText(self, v: str):
        if self._isPassword:
            if v == self.__Default or v == self.__Checking:
                self.__password = ''

            self.__password += v
            self._Entry.txt = self.__filler * len(v)

        else:
            self._Entry.txt = v
    def _AdjustPhotos(self): raise NotImplementedError()
