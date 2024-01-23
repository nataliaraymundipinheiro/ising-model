import copy
import itertools
import matplotlib.pyplot as plt
import numpy as np

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
        print(f"Dimension is {dim} and lattice is {lattice}")

        self.J = 1
        self.b = 1

        if dim is not None and lattice is None:
            print("Case 1")
            self.dim = dim # Lattice dimensions
            self.grid = np.random.choice([-1,1], size=(dim,dim), replace=True, p=None)
        
        elif dim is None and lattice is not None and isinstance(lattice, Lattice):
            print("Case 2")
            self.dim = lattice.dim
            self.grid = lattice.grid.copy()

        else:
            print("Case 3")
            self.dim = 0
            self.grid = []

        print("Lattice initialization is complete.\n")


    def energy(self) -> int:
        """
        The function calculates the energy of the grid based on the spin values
        and their interactions.
        
        RETURNS
        -------
            The energy of the system, which is calculated based on the grid and
            the interaction strength (J) between neighboring spins.
        """

        energy = 0

        for i, j in itertools.product(range(self.dim), range(self.dim)):
            spin_energy = 0

            if i > 0:
                spin_energy += self.grid[i-1,j]
            if i + 1 < self.dim:
                spin_energy +=  self.grid[i+1,j]
            if j > 0:
                spin_energy +=  self.grid[i,j-1]
            if j + 1 < self.dim:
                spin_energy +=  self.grid[i,j+1]

            energy += - self.J * self.grid[i,j] * spin_energy

        # Energy is double counted since the same interaction is counted twice
        return energy / 2


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
        fig, ax = plt.subplots()
        
        # Create a heat map
        cax = ax.imshow(self.grid, cmap='Paired')
        # Set title
        ax.set_title('Spin Grid')
        # Add colorbar
        fig.colorbar(cax)

        plt.show()
        