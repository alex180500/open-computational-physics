# Better Jacobi, an interactive Laplace-Poisson PDE numerical solver

<img src="images/capacitor.png" height="250"/> <img src="images/single_charge.png" height="250"/> <img src="images/custom.png" height="250"/>

Better Jacobi is a *Python* script implementing a vectorized [**Jacobi method**](https://en.wikipedia.org/wiki/Jacobi_method) for the [Laplace-Poisson](https://en.wikipedia.org/wiki/Poisson%27s_equation) partial differential equation.

## How do I use the interactive interface?

Just hold the left mouse button and draw in the grid canvas (which by default has a 50x50 size).

Left mouse button draws +default_Q charges with a default charge value denoted by the `-Q` flag, right mouse button draws -default_Q charges.

You can use the middle mouse button to erase (set to 0) the field charge.

## Examples

For the interactive version run
```console
$ python better_jacoby.py --interactive
```

For the other flags and options check out the help page or the code itself (which is thoroughly commented)
```console
$ python better_jacoby.py -h
```

## References

The argument parsing via command line is done using the **argparse** module, please refer to the [official documentation](https://docs.python.org/3/library/argparse.html) and this great [Stack Overflow answer](https://stackoverflow.com/questions/20063/whats-the-best-way-to-parse-command-line-arguments).

The interactive function was made by referring to the [Matplotlib API](https://matplotlib.org/stable/api/backend_bases_api.html) and another amazing [Stack Overflow topic](https://stackoverflow.com/questions/31248228/matplotlib-b1-motion-mouse-motion-with-key-held-down-equivalent).

The implementation of the vectorized Jacobi method and in general of the Laplace-Poisson algorithm is based on [**Essential skills for reproducible research computing**](https://barbagroup.github.io/essential_skills_RRC/laplace/1/) from *Universidad Técnica Federico Santa María* and also on [**Numerical methods for partial differential equations**](https://aquaulb.github.io/book_solving_pde_mooc/solving_pde_mooc/notebooks/05_IterativeMethods/05_01_Iteration_and_2D.html) by *Bernard Knaepen* and *Yelyzaveta Velizhanina*.

## Dependencies

  * **Python 3**
  * **Matplotlib**
  * **Numpy**