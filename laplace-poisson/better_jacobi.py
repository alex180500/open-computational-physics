# Fast Jacobi Python application for Laplace-Poisson PDE
#
# Author: Alessandro Romancino
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import argparse

# Argument parsing using the argparse module,
# you can call help by using the '-h' or '--help' flag.
#
# For more information check out the argparse documentation [1]
# [1]: https://docs.python.org/3/library/argparse.html
parser = argparse.ArgumentParser(
    description='Laplace-Poisson differential equation solver using Jacobi iterative method', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# positional optional argument
parser.add_argument('target', type=float, nargs='?',
                    default=1e-8, help='Target precision for the Jacobi method')
# optional float argument
parser.add_argument('-V', type=float, default=100.0,
                    help='Default grid voltage V')
# optional float argument
parser.add_argument('-N', type=int, default=50,
                    help='Number N of grid points in the lattice')
# optional float argument
parser.add_argument('-Q', type=float, default=100.0,
                    help='Default charge value')
# optional boolean argument
parser.add_argument('--capacitor', action='store_true',
                    help='Turns the default voltage to a capacitor')
# optional boolean argument
parser.add_argument('--sinusoidal', action='store_true',
                    help='Turns the default voltage wall to a sinusoidal function')
# optional boolean argument
parser.add_argument('--interactive', action='store_true',
                    help='Interactive charge field')
# arguments passed to the args class
args = parser.parse_args()


def interactive(default_q, n_grid, x_grid, y_grid):
    """Interactive algorithm for charge placement

    An interactive function that plots an NxN grid
    and makes it possible to draw the charge field by moving the mouse
    with left click for +Q charges or right click for -Q charges.
    It is possible to clear mistakes by holding the middle mouse button
    This function was made by referring to the Matplotlib API [1]
    and a stackoverflow question [2].

    [1]: https://matplotlib.org/stable/api/backend_bases_api.html
    [2]: https://stackoverflow.com/questions/31248228/matplotlib-b1-motion-mouse-motion-with-key-held-down-equivalent

    Parameters
    ----------
    p : ndarray
        2D array containing the initial system as float data.
    l2_target : float
        Convergence target for the iterative process.

    Returns
    -------
    ndarray
        2D array containing the system after the iterative process.
    int
        number of iteration steps of the algorithm.
    """
    # starting field is initialized to 0
    field = np.zeros([n_grid+1, n_grid+1], dtype=float)
    # the field is plotted initially
    plt.figure(figsize=[8, 8])
    plt.scatter(x_grid, y_grid, s=10, c=field, cmap=cm.plasma,
                vmin=-default_q, vmax=default_q)

    def mouse_drag(event):
        # rounded mouse coordinates
        x_coord, y_coord = round(event.xdata), round(event.ydata)
        # 1 for left click (+Q charge)
        if event.button == 1:
            field[y_coord, x_coord] = default_q
        # 2 for middle click (erase or 0 charge)
        elif event.button == 2:
            field[y_coord, x_coord] = 0
        # 3 for right click (-Q charge)
        elif event.button == 3:
            field[y_coord, x_coord] = -default_q
        # redraw the plot after every event
        plt.clf()
        plt.scatter(x_grid, y_grid, s=10, c=field, cmap=cm.plasma,
                    vmin=-default_q, vmax=default_q)
        plt.draw()

    # initialize the event function
    id_mouse = plt.connect('motion_notify_event', mouse_drag)
    plt.show()
    return field


def l2_diff(p, pn):
    """l2 norm difference.

    Computes the l2 norm of the difference of the two arrays.

    Parameters
    ----------
    p : ndarray
        1D array containing float data.
    pn : ndarray
        1D array containing float data.

    Returns
    -------
    float
        l2 norm of the difference of the two arrays.

    """
    return np.sqrt(np.sum((p - pn)**2)/np.sum(pn**2))


def laplace(p_new, l2_target):
    """Laplace algorithm vectorized implementation.

    Computes the Laplace algorithm for the potential with a vectorized
    method using numpy. The method is based on 'Essential skills for
    reproducible research computing' [1], 'Numerical methods for partial
    differential equations' [2] and my course notes.

    [1]: https://barbagroup.github.io/essential_skills_RRC/laplace/1/
    [2]: https://aquaulb.github.io/book_solving_pde_mooc/solving_pde_mooc/notebooks/05_IterativeMethods/05_01_Iteration_and_2D.html

    Parameters
    ----------
    p : ndarray
        2D array containing the initial system as float data.
    l2_target : float
        Convergence target for the iterative process.

    Returns
    -------
    ndarray
        2D array containing the system after the iterative process.
    int
        number of iteration steps of the algorithm.
    """
    # set the norm to 1
    l2norm = 1
    # initialize an empty array like the starting one for the iteration
    p_old = np.empty_like(p_new)
    # set the iteration counter
    iter = 0
    # while cycle until the target
    while l2norm > l2_target:
        # reset the old array to the new one
        np.copyto(p_old, p_new)
        # iterative process
        p_new[1:-1, 1:-1] = .25 * (p_old[1:-1, 2:] + p_old[1:-1, :-2]
                                   + p_old[2:, 1:-1] + p_old[:-2, 1:-1] + charge[1:-1, 1:-1])
        # compute the l2 norm
        l2norm = l2_diff(p_new, p_old)
        # add to the iteration
        iter += 1
    return p_new, iter


# variables initialization using argparse
N = args.N
V = args.V
q = args.Q
target = args.target
# grid for the interactive method and for final plotting
x = np.arange(N+1)
y = np.arange(N+1)
X, Y = np.meshgrid(x, y)

# starting potential phi
if args.capacitor:
    # if the flag '--capacitor' is used the potential at the borders is
    # set to -V and +V to simulate a capacitor-like potential
    phi = np.zeros([N+1, N+1], dtype=float)
    phi[:, -1] = -V
    phi[:, 0] = V
elif args.sinusoidal:
    # simple sinusoidal function at one border
    phi = np.zeros([N+1, N+1], dtype=float)
    phi[:, -1] = 0.5*V*np.sin(1.5*np.pi*x/x[-1])
else:
    # by default a flat potential is used
    phi = np.full([N+1, N+1], V, dtype=float)


# charge field for the simulation,
# an empty field with one charge in the middle is chosen
# when the flag '--interactive' is not used.
if args.interactive:
    # start the interactive method
    charge = interactive(q, N, X, Y)
else:
    # empty field with one charge in the middle
    charge = np.zeros([N+1, N+1], dtype=float)
    charge[N//2, N//2] = q

# call the main laplace function
phi, _ = laplace(phi.copy(), target)
# 3d plotting of the final potential
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(projection='3d')
surf = ax.plot_surface(X, Y, phi, rstride=1, cstride=1,
                       linewidth=0, cmap=cm.plasma)
plt.show()
