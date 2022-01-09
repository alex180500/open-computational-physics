import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import numpy as np
import cv2


def plotting_data(folder, column, ylabel):
    """
    Computes the temperature field with an explicit algorithm for nt
    time steps. The algorithm uses a FTCS scheme with Dirichelet boundary 
    conditions by default, with user-inputtable Neumann (zero-gradient)
    boundary conditions at any side (N, S, W, E).

    Parameters
    ----------
    folder : str
        2D array containing the initial temperature field as float data.
    column : int
        number of time steps to integrate.
    sigma_x : float
        constant present in the FTCS method for the x axis (alpha*dt/dx^2)
    sigma_y : float
        constant present in the FTCS method for the y axis (alpha*dt/dy^2)
    """
    data = np.loadtxt(f'{folder}/output.txt', usecols=column)
    plt.figure(figsize=(6, 5))
    plt.plot(data)
    plt.xlabel('Step')
    plt.ylabel(ylabel)
    plt.grid()
    plt.xlim(0, data.size)
    plt.ticklabel_format(style='sci', axis='both', scilimits=(0, 0))
    plt.tight_layout()
    plt.show()


def show_animation(folder, title):
    vid_capture = cv2.VideoCapture(f'{folder}/untitled.mpg')
    while(vid_capture.isOpened()):
        ret, frame = vid_capture.read()
        if ret:
            cv2.imshow(title, frame)
            key = cv2.waitKey(20)
            if cv2.getWindowProperty(title, cv2.WND_PROP_VISIBLE) < 1:        
                break
            if key == 27 or key == ord('q'):
                break  # esc or q to quit
        else:
            break
    vid_capture.release()
    cv2.destroyAllWindows()


class gui_frame(ttk.Frame):
    def __init__(self, parent, T, rho, folder):
        super().__init__(parent)

        self.T = T
        self.rho = rho
        self.folder = folder

        im = Image.open(f'{folder}/rdf.png')
        im = im.resize((350, 350))
        self.rdf = ImageTk.PhotoImage(im)

        self.my_font = tkFont.Font(size=18)

        self.option_list = {'Potential Energy': 2, 'Kinetic Energy': 3,
                            'Total Energy': 4, 'Energy Drift': 5,
                            'Temperature': 6, 'Pressure': 7}
        self.base_option = 'Potential Energy'
        self.plot_value = tk.StringVar()

        self.setup_widgets()

    def md_plotter(self):
        print(f'Plotting: {self.plot_value.get()}')
        col = self.option_list[self.plot_value.get()]
        plotting_data(self.folder, col, self.plot_value.get())

    def md_animation(self):
        print(f'Playing video animation for T={self.T} and rho={self.rho}')
        show_animation(self.folder, f'Animation for T={self.T}, rho={self.rho}')

    def setup_widgets(self):
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
    root = tk.Tk()
    root.title('Testing Azure')
    root.tk.call('source', 'ttk-theme/azure.tcl')
    root.tk.call('set_theme', 'light')

    gui = gui_frame(root, 0.5, 0.1, 'data/T05_r01')
    gui.pack(fill='both', expand=True)

    root.mainloop()
