import numba
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm
from lib.lattice import Lattice

class IsingModel:
    def __init__(self, size=None, lattice=None, beta=0.7, steps=1000, ratio_up=0.75) -> None:
        """
        Initializes an object with specified size or lattice configuration, beta
        value, number of steps, and ratio of up spins (if size is specified).
        
        PARAMETERS
        ----------
        size: int
            Size of the 2D-lattice sides.
        lattice: Lattice
            Instance of the `Lattice` class. It represents a lattice structure, 
            which is a grid of spins.
        beta: float
            Inverse temperature in the simulation. The formula is given by 1/kT.
            Defaults to 0.7.
        steps: int
            Number of steps that will be performed in the simulation. Defaults
            to 1000.
        ratio_up: float
            The ratio of "up" spins in the lattice. It is used to initialize the
            lattice with a certain proportion of spins in the "up" state. It
            only needs to be passed if size is input. Defaults to 0.75.
        """

        self.lattice = Lattice(size=size, lattice=lattice, ratio_up=ratio_up)
        self.beta = beta
        self.steps = steps


    def metropolis(self) -> None:  # sourcery skip: extract-duplicate-method
        """
        Performs the Metropolis algorithm to simulate the evolution of energy
        and net spin of a lattice, and then plots the results.
        """

        # Visualize how the lattice starts
        self.lattice.visualizeLattice()

        # Create an array to save the energies and the net spin of the lattice
        energies = []
        net_spin = []
        
        for _ in tqdm(range(self.steps)):
            self.recursive()
            energies.append(self.lattice.energy())
            net_spin.append(self.lattice.grid.sum())

        # Plot the energies and the spins
        fig, axs = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle(rf'Evolution of Energy and Net Spin for $\beta = {self.beta}$', y=0.95, fontsize=16)

        # Energies
        axs[0].plot(np.array(energies))
        axs[0].set_title("Energy vs. Time")
        axs[0].set_xlabel('Time Steps')
        axs[0].set_ylabel('Energy')
        axs[0].grid()

        # Spins
        axs[1].plot(np.array(net_spin)/50**2)
        axs[1].set_title("Net Spin vs. Time")
        axs[1].set_xlabel('Time Steps')
        axs[1].set_ylabel('Net Spin')
        axs[1].grid()
        axs[1].set_ylim(-1,1)

        # Customize
        fig.tight_layout()
        plt.show()



    def recursive(self) -> None:
        """
        Randomly flips a spin in a lattice and determines whether to keep the
        new state based on the change in energy and a probability calculation.
        """

        # Create the next possible lattice
        final = Lattice(size=None, lattice=self.lattice)

        # Pick random position in grid
        x, y = np.random.randint(low=0, high=final.size, size=2, dtype=int)
        # Flip the spin at position
        final.grid[x,y] *= -1

        dE = final.energy() - self.lattice.energy()

        # We flip the spin if the energy decreases or stays the same, or if the
        # energy increases, there's a certain probability that we change to that
        # state
        if (dE <= 0) or (dE > 0 and np.exp(-self.beta * dE) > np.random.random()):
            self.lattice.grid[x,y] = final.grid[x,y]

    