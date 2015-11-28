import os
import legofy
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import tkinter.messagebox as tkmsg

LEGO_PALETTE = ('none', 'solid', 'transparent', 'effects', 'mono', 'all', )

class LegofyGui(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wm_title("Legofy!")
        self.iconbitmap(os.path.dirname(os.path.realpath(__file__)) + '/assets/brick.ico')
        self.resizable(False, False)
        self.body = LegofyGuiMainFrame(self)
        self.body.grid(row=0, column=0, padx=10, pady=10)


class LegofyGuiMainFrame(tk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.chosenFile = None
        self.chosenFilePath = tk.StringVar()

        self.pathField = tk.Entry(self, width=40, textvariable=self.chosenFilePath, state=tk.DISABLED)
        self.pathField.grid(row=0, column=0, padx=10)

        self.selectFile = tk.Button(self, text="Choose file...", command=self.choose_a_file)
        self.selectFile.grid(row=0, column=1)

        self.groupFrame = tk.LabelFrame(self, text="Params", padx=5, pady=5)
        self.groupFrame.grid(row=1, column=0, columnspan=2, )

        self.colorPaletteLabel = tk.Label(self.groupFrame, text = 'Color Palette')
        self.colorPaletteLabel.grid(row=0, column=0 )

        self.colorPalette = ttk.Combobox(self.groupFrame)
        self.colorPalette['values'] = LEGO_PALETTE
        self.colorPalette.current(0)
        self.colorPalette.grid(row=0, column=1)

        self.brickNumberScale = tk.Scale(self.groupFrame, from_=1, to=200, orient=tk.HORIZONTAL, label="Number of bricks (longer edge)", length=250)
        self.brickNumberScale.set(30)
        self.brickNumberScale.grid(row=1, column=0, columnspan=2, )

        self.convertFile = tk.Button(text="Legofy this image!", command=self.convert_file)
        self.convertFile.grid(row=2, column=0, columnspan=2)


    def choose_a_file(self):

        options = {}
        options['defaultextension'] = '.jpg'
        options['filetypes'] = [('JPEG', '.jpg'),
                                ('GIF', '.gif'),
                                ('PNG', '.png'),]
        options['initialdir'] = os.path.realpath("\\")
        options['initialfile'] = ''
        options['parent'] = self
        options['title'] = 'Choose a file'

        self.chosenFile = filedialog.askopenfile(mode='r', **options)
        if self.chosenFile:
            self.chosenFilePath.set(self.chosenFile.name)


    def convert_file(self):
        try:
            if self.chosenFile is not None:

                palette = self.colorPalette.get()

                if palette in LEGO_PALETTE and palette != 'none':
                    legofy.main(self.chosenFile.name, size=self.brickNumberScale.get(), palette_mode=palette)
                else:
                    legofy.main(self.chosenFile.name, size=self.brickNumberScale.get())

                tkmsg.showinfo("Success!", "Your image has been legofied!")
            else:
                tkmsg.showerror("File not found", "Please select a file before legofying")
        except Exception as e:
            tkmsg.showerror("Error", str(e))



if __name__ == '__main__':
    app = LegofyGui()
    app.mainloop()
