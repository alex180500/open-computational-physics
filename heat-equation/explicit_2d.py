# Explicit Euler method for heat equation pde with a cool animation
#
# Author: Alessandro Romancino
# https://github.com/alex180500/open-computational-physics

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation
import argparse

# Argument parsing using the argparse module,
# you can call help by using the '-h' or '--help' flag.
parser = argparse.ArgumentParser(
    description='2D Heat equation PDE solver using Euler method',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('position', type=str, nargs='?',
                    default='ne', help='''Select the position of Neumann conditions
                    in the lattice (zero-gradient) can be "n", "s", "e", "w"
                    or any combination like "ns" or "swe"''')
parser.add_argument('--none', action='store_true',
                    help='Use this arguments to remove all Neumann conditions')
parser.add_argument('-a', type=float, default=1e-4,
                    help='Thermal diffusivity in m^2/s')
parser.add_argument('-nt', type=int, default=500,
                    help='Number of time step to compute')
parser.add_argument('-Tb', type=float, default=100.0,
                    help='Default bath temperature in C')
parser.add_argument('-T0', type=float, default=20.0,
                    help='Default grid temperature in C')
parser.add_argument('-Lx', type=float, default=0.01,
                    help='Grid length of the x axis in meters')
parser.add_argument('-Ly', type=float, default=0.01,
                    help='Grid length of the y axis in meters')
parser.add_argument('-nx', type=int, default=41,
                    help='Number of grid points in the x axis')
parser.add_argument('-ny', type=int, default=41,
                    help='Number of grid points in the y axis')
# arguments passed to the args class
args = parser.parse_args()


def ftcs(T0, nt, sigma_x, sigma_y):
    """
    Computes the temperature field with an explicit algorithm for nt
    time steps. The algorithm uses a FTCS scheme with Dirichelet boundary 
    conditions by default, with user-inputtable Neumann (zero-gradient)
    boundary conditions at any side (N, S, W, E).

    Parameters
    ----------
    T0 : ndarray
        2D array containing the initial temperature field as float data
    nt : int
        Number of time steps to integrate
    sigma_x : float
        Constant present in the FTCS method for the x axis (alpha*dt/dx^2)
    sigma_y : float
        Constant present in the FTCS method for the y axis (alpha*dt/dy^2)

    Returns
    -------
    ndarray
        3D array containing the 2D field at every step.
    """
    # 2d array for every step
    T = T0.copy()
    # shape of the 3d array, first axis represent all the time steps
    shape = (nt,) + T.shape
    # set the final 3d array
    T_evol = np.zeros(shape)
    # cycle for every time step
    for n in range(nt):
        # FTCS algorithm with default Dirichelet conditions
        T[1:-1, 1:-1] = (T[1:-1, 1:-1] +
                         sigma_x * (T[1:-1, 2:] - 2.0 * T[1:-1, 1:-1] + T[1:-1, :-2]) +
                         sigma_y * (T[2:, 1:-1] - 2.0 * T[1:-1, 1:-1] + T[:-2, 1:-1]))
        # check user input for Neumann conditions
        if 'n' in args.position:
            T[-1, :] = T[-2, :]
        if 'e' in args.position:
            T[:, -1] = T[:, -2]
        if 's' in args.position:
            T[0, :] = T[1, :]
        if 'w' in args.position:
            T[:, 0] = T[:, 1]
        # assign the calculated field to the nth time step
        T_evol[n] = T
    return T_evol


# grid spacing in the x direction
dx = args.Lx / (args.nx - 1)
# grid spacing in the y direction
dy = args.Ly / (args.ny - 1)
# define the grid positions
x = np.linspace(0.0, args.Lx, args.nx)
y = np.linspace(0.0, args.Ly, args.ny)
# initial uniform temperature distribution
T0 = np.full((args.ny, args.nx), args.T0)
# reset Neumann conditions if the "--none" argument is used
if args.none:
    args.position = ''
# set boundaries at fixed temperature if not specified
if 'n' not in args.position:
    T0[-1, :] = args.Tb
if 'e' not in args.position:
    T0[:, -1] = args.Tb
if 's' not in args.position:
    T0[0, :] = args.Tb
if 'w' not in args.position:
    T0[:, 0] = args.Tb

# CFL limit is 0.25
sigma = 0.25
# set the minimum for the time step
dt = sigma * min(dx, dy)**2 / args.a
# compute the constant in FTCS
sigma_x = args.a * dt / dx**2
sigma_y = args.a * dt / dy**2
# get the 3d array
T = ftcs(T0, args.nt, sigma_x, sigma_y)

# plotting with animation
fig = plt.figure(figsize=(8.0, 5.0))
# first contour plot
contf = plt.contourf(x, y, T[0], levels=50, cmap=cm.plasma)
# set the ticks in the colorbar (fixed)
ticks = np.linspace(T[0].min(), T[0].max(), 5, endpoint=True)
# plot the fixed colorbar
plt.colorbar(contf, ticks=ticks, format='%.1f', label='Temperature [C]')
# rescale the contour plot to be sized according to Lx and Ly
plt.axis('scaled')


def update(frame):
    # set the contour plot to global
    global contf
    # remove all collections of the contourplot for better speed
    for coll in contf.collections:
        coll.remove()
    # set the contourplot for the frame
    contf = plt.contourf(x, y, T[frame], levels=50, cmap=cm.plasma)
    return contf.collections


# hard coded fps
fps = 24
# animation
animation = FuncAnimation(fig, update, interval=1000/fps, frames=args.nt)
# animation.save('images/animation.mp4', fps=fps)
plt.show()
