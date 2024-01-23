import numba
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm
from lattice import Lattice

class IsingModel:
    def __init__(self, dim=None, lattice=None, steps=100) -> None:
        self.lattice = Lattice(dim=dim, lattice=lattice)
        self.steps = steps


    def metropolis(self) -> None:
        self.lattice.visualizeLattice()
        energies = []
        spins = []
        for _ in tqdm(range(self.steps)):
            self.recursive()
            energies.append(self.lattice.energy())
            spins.append(self.lattice.grid.sum())

        fig, axs = plt.subplots(1, 2, figsize=(12,4))
        axs[0].plot(np.array(energies))
        axs[0].set_xlabel('Time Steps')
        axs[0].set_ylabel('Energy')
        axs[0].grid()
        axs[1].plot(np.array(spins)/50**2)
        axs[1].set_xlabel('Time Steps')
        axs[1].set_ylabel('Net Spin')
        axs[1].set_ylim(-1,1)
        axs[1].grid()
        fig.tight_layout()
        fig.suptitle(r'Evolution of Energy for $\beta = 0.7$', y=1.07, size=18)
        plt.show()



    def recursive(self) -> None:
        final = Lattice(dim=None, lattice=self.lattice)
        # Pick random position in grid
        x, y = np.random.randint(low=0, high=final.dim, size=2, dtype=int)
        # Flip the spin at position
        final.grid[x,y] *= -1

        dE = final.energy() - self.lattice.energy()

        # We flip the spin if the energy decreases or stays the same, or if the
        # energy increases, there's a certain probability that we change to that
        # state
        if (dE <= 0) or (dE > 0 and np.exp(-self.lattice.b * dE) > np.random.random()):          
            self.lattice.grid[x,y] = final.grid[x,y]


ising = IsingModel(dim=50, lattice=None, steps=100000)
ising.metropolis()
ising.lattice.visualizeLattice()

    