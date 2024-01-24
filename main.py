from lib.ising_model import IsingModel


def run_simulation():
    """
    Initializes and runs a simulation of the Ising model on a square lattice
    with given dimensions, ratio of up spins, beta value, and number of steps,
    and then visualizes the resulting lattice.
    """

    size = 10       # Square lattice side size
    ratio_up = 0.75 # Ratio of up spins in the lattice
    beta = 0.7      # beta = 1/kT
    steps = 10000   # Number of simulation steps

    # Initialize Ising model
    ising = IsingModel(size=size, lattice=None, beta=beta, steps=steps,
                       ratio_up=ratio_up)
    # Run Metropolis algorithm
    ising.metropolis()
    
    # Visualize final matrix
    ising.lattice.visualizeLattice()


def main():
    # This is the main function where the simulation is executed.
    run_simulation()


if __name__ == "__main__":
    # This condition ensures that the main function is executed only
    # when this script is run directly, and not when imported as a module.
    main()
