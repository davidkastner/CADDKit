"""Generalizable script for plotting the PES of an xyz trajectory."""

import matplotlib.pyplot as plt
import numpy as np
import csv
import time

HARTREE_TO_KCAL = 627.509

def write_energies_to_csv(energies_by_file, energies_hartrees_by_file, filename="energy_plot_data.csv"):
    """
    Write the energies to a CSV file.

    Parameters
    ----------
    energies_by_file : dict
        A dictionary with filenames as keys and corresponding energies as values in kcal/mol.
    energies_hartrees_by_file : dict
        A dictionary with filenames as keys and corresponding energies as values in Hartrees.
    filename : str
        The name of the output CSV file.
    """
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename", "Frame", "Energy (Hartrees)", "Energy (kcal/mol)"])
        for file, energies_kcal in energies_by_file.items():
            for frame, energy_kcal in enumerate(energies_kcal):
                energy_hartrees = energies_hartrees_by_file[file][frame]
                writer.writerow([file, frame, energy_hartrees, energy_kcal])

def parse_energy(line, software):
    """
    Parse the energy from a line based on the software used.

    Parameters
    ----------
    line : str
        Line from the file containing energy information.
    software: str
        The software used for the calculation.

    Returns
    -------
    float
        The energy extracted from the line, in Hartrees.

    """
    if software == "ORCA-MEP" or software == "ORCA-IRC":
        energy_str = line.split()[5]
    elif software == "ORCA":
        energy_str = line.split()[4]
    elif software == "TeraChem-scan":
        energy_str = line.split()[4]
    elif software == "TeraChem-opt":
        energy_str = line.split()[0]
    elif software == "TeraChem-NEB":  # <-- ADDED BLOCK
        energy_str = line.split()[0]
    else:
        raise ValueError(f"Unsupported software: {software}")

    return float(energy_str)


def get_trajectory_energies(filename, software):
    """
    Parse the energies from an xyz trajectory file.

    Parameters
    ----------
    filename : str
        Path to the trajectory file.
    software: str
        Software used for the calculation.

    Returns
    -------
    tuple
        First value is a list of energies for each frame, in kcal/mol, relative to the first frame.
        Second value is the first frame energy in kcal/mol.
        Third value is a list of absolute energies in Hartrees.

    """
    energies_hartrees = []
    with open(filename, "r") as f:
        while True:
            line = f.readline()
            if not line:
                break  # end of file

            atom_count = int(line.strip())
            # next line should contain energy
            energy_line = f.readline().strip()
            # parse and append energy
            energies_hartrees.append(parse_energy(energy_line, software))
            # skip atom lines
            for _ in range(atom_count):
                f.readline()

    # convert energies to kcal/mol and subtract first energy to make it relative
    first_energy = energies_hartrees[0] * HARTREE_TO_KCAL
    energies_kcal = [(e - energies_hartrees[0]) * HARTREE_TO_KCAL for e in energies_hartrees]

    return energies_kcal, first_energy, energies_hartrees


def identify_software(line):
    """
    Identify the software used for the calculation from a line.

    Parameters
    ----------
    line : str
        Line from the file.

    Returns
    -------
    str
        Identifier of the software used for the calculation.
    """
    if "ORCA-job qmscript_MEP" in line:
        return "ORCA-MEP"
    elif "ORCA-job qmscript_IRC_Full" in line:
        return "ORCA-IRC"
    elif "ORCA-job qmscript" in line:
        return "ORCA"
    elif "Converged     Job" in line:
        return "TeraChem-scan"
    elif "TeraChem" in line:
        return "TeraChem-opt"
    # BELOW IS THE ONLY OTHER CHANGE: check if line is purely a float => TeraChem NEB
    elif line.strip().replace('.', '', 1).replace('-', '', 1).isdigit():
        return "TeraChem-NEB"
    else:
        raise ValueError(f"Could not identify software from line: {line}")


def format_plot() -> None:
    """
    General plotting parameters for the Kulik Lab.

    """
    font = {"family": "sans-serif", "weight": "bold", "size": 10}
    plt.rc("font", **font)
    plt.rcParams["xtick.major.pad"] = 5
    plt.rcParams["ytick.major.pad"] = 5
    plt.rcParams["axes.linewidth"] = 2
    plt.rcParams["xtick.major.size"] = 7
    plt.rcParams["xtick.major.width"] = 2
    plt.rcParams["ytick.major.size"] = 7
    plt.rcParams["ytick.major.width"] = 2
    plt.rcParams["xtick.direction"] = "in"
    plt.rcParams["ytick.direction"] = "in"
    plt.rcParams["xtick.top"] = True
    plt.rcParams["ytick.right"] = True
    plt.rcParams["svg.fonttype"] = "none"


def collect_data():
    """
    Collect energies from the files and decide whether to plot relative to lowest energy.

    Returns
    -------
    dict
        A dictionary with filenames as keys and corresponding energies as values in kcal/mol.
    float
        The minimum first frame energy.
    bool
        Whether to plot energies relative to the lowest energy.
    dict
        A dictionary with filenames as keys and corresponding absolute energies as values in Hartrees.

    """
    filenames_input = input(
        "   > What trajectories would you like to plot (omit .xyz extension)? "
    ).split(",")
    filenames = [f"{name.strip()}.xyz" for name in filenames_input]

    energies_by_file = {}
    energies_hartrees_by_file = {}
    first_energies = []

    for filename in filenames:
        with open(filename, "r") as f:
            # read two lines to get to the software info
            f.readline()
            software_line = f.readline()
            software = identify_software(software_line)

        energies_kcal, first_energy, energies_hartrees = get_trajectory_energies(filename, software)
        energies_by_file[filename] = energies_kcal
        energies_hartrees_by_file[filename] = energies_hartrees
        first_energies.append(first_energy)

    min_first_energy = min(first_energies)
    plot_relative_to_lowest = (
        len(filenames) > 1
        and input("   > Plot energies relative to absolute energies? (yes/no) ") == "yes"
    )

    return energies_by_file, min_first_energy, plot_relative_to_lowest, energies_hartrees_by_file


def plot_data(energies_by_file, min_first_energy, plot_relative_to_lowest, dim_list):
    """
    Plot the collected energies.

    Parameters
    ----------
    energies_by_file : dict
        A dictionary with filenames as keys and corresponding energies as values.
    min_first_energy : float
        The minimum first frame energy.
    plot_relative_to_lowest : bool
        Whether to plot energies relative to the lowest energy.
    """

    format_plot()
    fig, ax = plt.subplots(figsize=(dim_list[0], dim_list[1]))
    
    max_energy = float('-inf')
    max_energy_info = (0, 0)  # To store filename and frame for highest energy point

    for idx, (filename, energies) in enumerate(energies_by_file.items()):

        if plot_relative_to_lowest:
            # make energies relative to the first frame with the lowest energy
            energies = [
                e - (first_energies[filenames.index(filename)] - min_first_energy)
                for e in energies
            ]

        # Plotting the energy line
        ax.plot(
            range(len(energies)),
            energies,
            marker="o",
            linestyle="-",
            label=f"{filename} (max {round(max(energies), 2)} kcal/mol)",
            color='b',
        )

        # Check for overall maximum energy to annotate
        local_max_energy = max(energies)
        if local_max_energy > max_energy:
            max_energy = local_max_energy
            max_energy_frame = energies.index(local_max_energy)
            max_energy_info = (filename, max_energy_frame)

    # Annotate the highest point across all plots
    ax.annotate(f"{max_energy:.1f}", (max_energy_info[1], max_energy),
                textcoords="offset points", xytext=(0, 10), ha='center', va='bottom')

    # Extend y-axis to fit annotation
    y_lim = ax.get_ylim()
    ax.set_ylim(y_lim[0], y_lim[1] + (y_lim[1] - y_lim[0]) * 0.1)  # Adding 10% padding at the top

    ax.set_xlabel("NEB frames", weight="bold")
    ax.set_ylabel("Relative energy (kcal/mol)", weight="bold")

    # Save the figure with enough padding
    plt.legend()
    extensions = ["png", "svg"]
    for ext in extensions:
        plt.savefig(
            f"energy_plot.{ext}",
            dpi=600,
            bbox_extra_artists=(plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left"),),
            bbox_inches="tight",
            format=ext,
        )


def plot_energies():
    """
    Main function that combines previous functions to generate the plot.
    """
    print("\n.---------------------------.")
    print("| WELCOME TO ENERGY PLOTTER |")
    print(".---------------------------.\n")
    print("> Generates a plot of an xyz trajectory.")
    print("> Can handle an arbitrary number of xyz trajectories")

    start_time = time.time()  # Used to report the execution speed

    dim = input("   > What dimensions would you like the plot (e.g. 5,4)? ")
    if dim:
        x_dim = int(dim.split(",")[0])
        y_dim = int(dim.split(",")[1])
        dim_list = [x_dim, y_dim]
    else:
        dim_list = [4, 4]


    energies_by_file, min_first_energy, plot_relative_to_lowest, energies_hartrees_by_file = collect_data()
    write_energies_to_csv(energies_by_file, energies_hartrees_by_file)  # Write energies to CSV
    plot_data(energies_by_file, min_first_energy, plot_relative_to_lowest, dim_list)

    total_time = round(time.time() - start_time, 3)  # Seconds to run the function
    job_summary = f"""
        --------------------------ENERGY PLOTTER END--------------------------
        RESULT: Plotted energies for {len(energies_by_file)} number of xyz trajectories.
        OUTPUT: Created a plot called 'energy_plot.png' and a CSV file called 'energy_plot_data.csv' in the current directory.
        TIME: Total execution time: {total_time} seconds.
        --------------------------------------------------------------------\n
        """

    print(job_summary)


if __name__ == "__main__":
    plot_energies()
