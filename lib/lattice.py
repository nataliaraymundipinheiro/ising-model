import matplotlib.pyplot as plt
import numpy as np

from scipy.ndimage import convolve, generate_binary_structure

class Lattice:
    def __init__(self, dim=None, lattice=None) -> None:
        """
        The function initializes a lattice object with a specified dimension and
        lattice configuration, or copies an existing lattice object.
        
        :param dim: The `dim` parameter represents the dimensions of the lattice. It
        specifies the size of the grid on which the lattice is defined
        :param lattice: The `lattice` parameter is an instance of the `Lattice`
        class
        """

        self.J = 1
        self.b = 0.7

        if dim is not None and lattice is None:
            self.dim = dim # Lattice dimensions

            # Ratio of spins that are up compared to down spins
            ratio_up = 0.75
            self.grid = np.random.choice([-1,1],
                                         size=(dim,dim),
                                         replace=True,
                                         p=[1-ratio_up, ratio_up])
        
        elif dim is None and lattice is not None and isinstance(lattice, Lattice):
            self.dim = lattice.dim
            self.grid = lattice.grid.copy()

        else:
            self.dim = 0
            self.grid = []


    def energy(self) -> int:
        """
        The function calculates the energy of the grid based on the spin values
        and their interactions.
        
        RETURNS
        -------
            The energy of the system, which is calculated based on the grid and
            the interaction strength (J) between neighboring spins.
        """
        
        kernel = generate_binary_structure(2, 1)
        kernel[1,1] = False
        
        conv = - self.grid * convolve(self.grid, kernel, mode='constant', cval=0)
        return conv.sum()


    def printLattice(self):
        """
        The function prints a lattice grid where each cell is represented by "+"
        if its value is +1, and "-" if its value is -1.
        """

        for row in self.grid:
            row_str = '\t'.join("+" if spin == 1 else "-" for spin in row)
            print(row_str)


    def visualizeLattice(self) -> None:
        """
        Creates a heat map to visualize a grid of spins. 1 represents spin up
        and -1 represents spin down.
        """
        
        # Create a heat map
        plt.imshow(self.grid, cmap='Paired')
        # Set title
        plt.title('Spin Grid')
        # Add colorbar
        plt.clim(-1,1)
        plt.colorbar()

        plt.show()
        