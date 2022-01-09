# Gui interface used in phase diagram, please refer to the documentation
#
# Author: Alessandro Romancino
# https://github.com/alex180500/open-computational-physics

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import numpy as np
import cv2


def plotting_data(folder, column, ylabel):
    """
    Plots the data of the chosen column from
    output.txt from the selected folder 

    Parameters
    ----------
    folder : str
        name of the folder of output.txt
    column : int
        column number for plotting
    ylabel : str
        label for the y axis
    """
    data = np.loadtxt(f'{folder}/output.txt', usecols=column)
    plt.figure(figsize=(6, 5))
    plt.plot(data)
    plt.xlabel('Step')
    plt.ylabel(ylabel)
    plt.grid()
    plt.xlim(0, data.size)
    # scientific formatting
    plt.ticklabel_format(style='sci', axis='both', scilimits=(0, 0))
    plt.tight_layout()
    plt.show()


def show_animation(folder, title):
    """
    CV2 simple media player of untitled.mpg from given folder.
    You can press Q, ESC or press the x to quit.

    Parameters
    ----------
    folder : str
        name of the folder of untitled.mpg
    title : str
        window title
    """
    vid_capture = cv2.VideoCapture(f'{folder}/untitled.mpg')
    while(vid_capture.isOpened()):
        ret, frame = vid_capture.read()
        if ret:
            cv2.imshow(title, frame)
            key = cv2.waitKey(20)
            # pressing the x quits the animation
            if cv2.getWindowProperty(title, cv2.WND_PROP_VISIBLE) < 1:        
                break
            # esc or q to quit the animation
            if key == 27 or key == ord('q'):
                break
        else:
            break
    vid_capture.release()
    cv2.destroyAllWindows()


class gui_frame(ttk.Frame):
    def __init__(self, parent, T, rho, folder):
        """
        __init__ method for the gui creation.

        Parameters
        ----------
        parent : tkinter.Tk
            Tk frame to use with themes
        T : float
            Temperature used for the gui
        rho : float
            Density used for the gui
        folder : str
            Data folder
        """
        # activate the themed tkinter frame
        super().__init__(parent)
        # declare some variables
        self.T = T
        self.rho = rho
        self.folder = folder
        # get a premade image for later use
        im = Image.open(f'{folder}/rdf.png')
        im = im.resize((350, 350))
        self.rdf = ImageTk.PhotoImage(im)
        # create a font for the labels
        self.my_font = tkFont.Font(size=18)
        # options and variables for the optionmenu
        self.option_list = {'Potential Energy': 2, 'Kinetic Energy': 3,
                            'Total Energy': 4, 'Energy Drift': 5,
                            'Temperature': 6, 'Pressure': 7}
        self.base_option = 'Potential Energy'
        self.plot_value = tk.StringVar()
        # activate the main function
        self.setup_widgets()

    def md_plotter(self):
        """function for the plot button, gets values from
        the option_list dictionary, the values are the
        specific columns of output.txt to plot."""
        print(f'Plotting: {self.plot_value.get()}')
        col = self.option_list[self.plot_value.get()]
        # calls plotting_data
        plotting_data(self.folder, col, self.plot_value.get())

    def md_animation(self):
        """Function for the animation, just need the folder
        and the name of the window."""
        print(f'Playing video animation for T={self.T} and rho={self.rho}')
        show_animation(self.folder, f'Animation for T={self.T}, rho={self.rho}')

    def setup_widgets(self):
        """The gui is divided in top_frame and bottom_frame.
        Top frame contains labels and the animation button,
        the bottom frame is a label frame with only the plot part."""
        self.top_frame = ttk.Frame(self, padding=(0, 0))
        self.top_frame.grid(row=0, column=0)

        self.image = ttk.Label(self.top_frame, image=self.rdf)
        self.image.grid(row=0, column=0, rowspan=3, padx=(0, 10))

        self.simulation_T = ttk.Label(
            self.top_frame, text=f'T = {self.T}', font=self.my_font)
        self.simulation_T.grid(row=0, column=1, padx=(0, 20), pady=(40, 0))

        self.simulation_rho = ttk.Label(
            self.top_frame, text=f'\u03C1 = {self.rho}', font=self.my_font)
        self.simulation_rho.grid(row=1, column=1, padx=(0, 20))

        self.animation = ttk.Button(
            self.top_frame, text='Show Animation', command=self.md_animation)
        self.animation.grid(row=2, column=1, padx=(0, 20), pady=(0, 40))

        self.bottom_frame = ttk.LabelFrame(
            self, text='Plot Output', padding=(20, 10))
        self.bottom_frame.grid(row=1, column=0, pady=(0, 20), padx=20)

        self.selector = ttk.OptionMenu(
            self.bottom_frame, self.plot_value, self.base_option,
            *self.option_list.keys())
        self.selector.config(width=20)
        self.selector.grid(row=0, column=0, padx=30, pady=10)

        self.plot_button = ttk.Button(self.bottom_frame, text='Plot!',
                                      style='Accent.TButton', command=self.md_plotter)
        self.plot_button.grid(row=0, column=1, padx=30, pady=10)


if __name__ == '__main__':
    # test function for testing the gui, only debug purpose
    root = tk.Tk()
    root.title('Testing Azure')
    root.tk.call('source', 'ttk-theme/azure.tcl')
    root.tk.call('set_theme', 'light')
    gui = gui_frame(root, 0.5, 0.1, 'data/T05_r01')
    gui.pack(fill='both', expand=True)
    root.mainloop()
