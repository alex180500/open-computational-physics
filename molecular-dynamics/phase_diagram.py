# Interactive python interface for molecular dynamics
#
# Author: Alessandro Romancino
# https://github.com/alex180500/open-computational-physics

import cv2
import matplotlib.pyplot as plt
import numpy as np
from create_gui import gui_frame
import tkinter as tk

# rho values
rho = np.linspace(0.1, 1.0, 4)
# pixel between points over interval for the image
dx = 434/0.1
# position for the grid
rho_grid = 1114 + rho * dx

# same for temperature
temp = np.linspace(0.5, 2.0, 4)
dy = -494/0.25
temp_grid = 5136 + temp * dy

# create grid for plotting
x_grid, y_grid = np.meshgrid(rho_grid, temp_grid)


def onpick(event):
    """
    Interactive function that takes the pick event,
    finds the folder index and activate the gui from create_gui.py
    """
    # indexes are arranged in a linear pattern from 0 to 15
    ind = event.ind[0]
    # get x value of the index
    x_ind = ind % 4
    # get the y index with a floor function
    y_ind = ind // 4
    # a print useful for debugging purposes
    # print('onpick scatter:', ind, rho[x_ind], temp[y_ind])

    # call the root of tkinter
    root = tk.Tk()
    # change tkinter window title
    root.title('Molecular Dynamics Interactive')
    # activate azure theme themed tkinter
    root.tk.call('source', 'ttk-theme/azure.tcl')
    root.tk.call('set_theme', 'light')

    # get folder name from temperature and rho
    folder = 'data/T' + format(temp[y_ind], '.1f').replace('.', '') + \
        '_r' + format(rho[x_ind], '.1f').replace('.', '')
    print(f'folder used = {folder}')

    # activate the gui and loop tkinter
    gui = gui_frame(root, temp[y_ind], rho[x_ind], folder)
    gui.pack(fill='both', expand=True)
    root.mainloop()


# image import of the diagram
image = cv2.imread('LJ_PhaseDiagram.png')
plt.imshow(image)
# scatterplot from the grid
plt.scatter(x_grid, y_grid, picker=True)
# connect to pick_event to activate UI
plt.connect('pick_event', onpick)
# remove axis and improve visibility
plt.axis('off')
plt.tight_layout()
plt.show()
