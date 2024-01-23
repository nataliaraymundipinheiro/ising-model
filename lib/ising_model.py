import numpy as np

from lattice import Lattice

class IsingModel:
    def __init__(self, dim) -> None:
        self.lattice = Lattice(dim=dim, lattice=None)


    def start(self) -> None:
        ...


    def recursive(self) -> None:
        temp = Lattice(dim=None, lattice=self.lattice)
        x, y = np.random.randint(low=0, high=temp.dim, size=2, dtype=int)
        temp[x,y] = 1 if temp[x,y] == -1 else -1

        energy_u = self.lattice.energy()
        p_u_to_v = ...
        
        energy_v = temp.energy()
        p_v_to_u = ...

        if temp.energy() > self.lattice.energy():
            p_u_to_v = np.exp(-self.lattice.b * (energy_v - energy_u))
            p_v_to_u = 1

            
        else: 
            p_u_to_v = 1
            p_v_to_u = np.exp(-self.lattice.b * (energy_v - energy_u))
        




ising = IsingModel(10)
# ising.printLattice()
ising.recursive()
# ising.printLattice()

    