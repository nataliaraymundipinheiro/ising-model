import matplotlib.pyplot as plt
import numpy as np

from scipy.ndimage import convolve, generate_binary_structure

class Lattice:
    def __init__(self, size=None, lattice=None, ratio_up=0.75) -> None:
        """
        The function initializes a lattice with a specified size and random spin
        values, or copies an existing lattice.
        
        Either the size OR the Lattice can be passed to create new a Lattice.

        PARAMETERS
        ----------
        size: int
            Size of the 2D-lattice sides.
        lattice: Lattice
            Instance of the `Lattice` class. It represents a lattice structure, 
            which is a grid of spins.
        ratio_up: float
            The ratio of "up" spins in the lattice. It is used to initialize the
            lattice with a certain proportion of spins in the "up" state. It
            only needs to be passed if size is input. Defaults to 0.75.
        """

        self.J = 1

        if size is not None and lattice is None:
            self.size = size # Lattice size

            # Ratio of spins that are up compared to down spins
            self.ratio_up = ratio_up
            self.grid = np.random.choice([-1,1],
                                         size=(size, size),
                                         replace=True,
                                         p=[1-ratio_up, ratio_up])
        
        elif size is None and lattice is not None and isinstance(lattice, Lattice):
            self.size = lattice.size
            self.grid = lattice.grid.copy()

        else:
            print('Invalid lattice. Try again.')
            while(1): continue


    def energy(self) -> int:
        """
        The function calculates the energy of the grid based on the spin values
        and their interactions.
        
        RETURNS
        -------
            The energy of the system, which is calculated based on the grid and
            the interaction strength (J) between neighboring spins.
        """
        
        # Create a kernel that has the four neighbors of a spin as a True
        # value, and the other values are False
        kernel = generate_binary_structure(2, 1)
        kernel[1,1] = False
        
        # Perform a convolution between the matrix and the kernel such that
        # we have a new matrix where each location is the sum of all the four
        # neighbors. Then, multiply this matrix by grid and the respective
        # interaction value, finalizing the energy operation.
        conv = - self.J * self.grid * convolve(self.grid, kernel,
                                               mode='constant', cval=0)
        
        # Now that each grid has the value of energy of each spin, sum all of
        # the energies to get the total energy of the lattice.
        return conv.sum()


    def printLattice(self):
        """
        The function prints a lattice grid where each cell is represented by "+"
        if its value is +1, and "-" if its value is -1.
        """

        for row in self.grid:
            row_string = '\t'.join("+" if spin == 1 else "-" for spin in row)
            print(row_string)


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
        