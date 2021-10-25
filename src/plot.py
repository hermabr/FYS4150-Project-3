import numpy as np
import pandas as pd
import seaborn as sns
from pandas.core.frame import DataFrame
import argparse

import matplotlib
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

sns.set()


def side_by_side_plot(infile_1, infile_2, outfile=None):
    fig, ax = plt.subplots(1, 2)
    #  fig.suptitle(title)
    df1 = pd.read_csv(infile_1)
    df2 = pd.read_csv(infile_2)

    ax[0].plot(df1.x, df1.y, df1.z)
    #  ax[1].plot(df2.x, df2.y, df2.z)
    #  ax[0].set_title(plot_one_title)
    #  for x_data, y_data, label in zip(plot_one_x_data, plot_one_y_data, plot_one_labels):
    #  sns.lineplot(x=x_data, y=y_data, label=label, ax=ax[0])
    #  ax[0].set(xlabel=plot_one_x_label, ylabel=plot_one_y_label)

    #  ax[1].set_title(plot_two_title)
    #  for x_data, y_data, label in zip(plot_two_x_data, plot_two_y_data, plot_two_labels):
    #  sns.lineplot(x=x_data, y=y_data, label=label, ax=ax[1])
    #  ax[1].set(xlabel=plot_two_x_label, ylabel=plot_two_y_label)

    #  plt.legend()
    #  if outfile:
    #      plt.savefig(f"data/{outfile.replace(' ', '_')}")
    plt.show()


# TODO: Axis names
def plot_3d_solution(ax, filename: str, label: str):
    """Plot the curve described in a file on `ax`, in 3d.

    Arguments:
        ax: Axes instance to plot on. Must be Axes3D.
        filename: Name of file to read. See the function `get_solution` for
                  details on format.
        label: Label to put on plot.
    """
    #  _, x, y, z = get_solution(filename)
    df = pd.read_csv(f"data/{filename}.csv")
    ax.plot(df.x, df.y, df.z, label=label)


def relative_err(computed: DataFrame, expected: DataFrame):
    return np.sqrt(
        (computed["x"] - expected["x"]) ** 2
        + (computed["y"] - expected["y"]) ** 2
        + (computed["z"] - expected["z"]) ** 2
        / (computed["x"] * 2 + computed["y"] * 2 + computed["z"] ** 2)
    )

def absolute_error(computed: DataFrame, expected: DataFrame):
    return np.sqrt(
        (computed["x"] - expected["x"]) ** 2
        + (computed["y"] - expected["y"]) ** 2
        + (computed["z"] - expected["z"]) ** 2
    )


def plot_error():
    for filename, method_name in zip(["data/rk4h=", "data/feh="],
                                     ["Runge Kutta 4", "Forward Euler"]):
        for h in ["1e-4", "5e-2", "1e-1", "5e-1", "1"]:
            df_a = pd.read_csv(f"data/analyticalh={h}.csv")
            df_num = pd.read_csv(f"{filename}{h}.csv")
            epsilon = relative_err(df_num, df_a)

            t = np.linspace(0, 100, len(df_a))
            plt.plot(t, epsilon, label=h)
        plt.title(f"Relative error of {method_name}")
        plt.ylabel("Error (log)")
        plt.xlabel("Time ($\\mu s$)")
        plt.yscale("log")
        plt.legend()
        plt.savefig(f"data/{method_name.lower().replace(' ', '_')}_relativeError.pdf")
        plt.close()

def plot_convergence_rate():
    for filename, method_name in zip(["data/rk4h=", "data/feh="],
                                     ["Runge Kutta 4", "Forward Euler"]):

        # Find max error for each h
        max_delta = []
        h_list = ["1", "5e-1", "1e-1", "5e-2", "1e-4"]
        for h in h_list:
            df_a = pd.read_csv(f"data/analyticalh={h}.csv")
            df_num = pd.read_csv(f"{filename}{h}.csv")
            delta = absolute_error(df_num, df_a)
            max_delta.append(max(delta))

        fh_list = [float(h) for h in h_list]

        r_err = 1/4 * sum([
            np.log(max_delta[i]/max_delta[i-1])/np.log(fh_list[i]/fh_list[i-1])
            for i in range(1, 5)])

        plt.plot(fh_list, max_delta)
        plt.xlabel("Step size (log, $\\mu s$)")
        plt.gca().invert_xaxis()
        plt.ylabel("Max absolute error (log)")
        plt.xscale("log")
        plt.yscale("log")
        plt.title(f"Convergence rate for {method_name} ($r_{'{err}'} = {r_err:.3g}$)")
        plt.savefig(f"data/{method_name.lower().replace(' ', '_')}_convergence.pdf")
        plt.close()

#  """Plot particles movement, and error where we have an analytical solution.
#  """
#
#  import matplotlib
#  from matplotlib import cm
#  from mpl_toolkits.mplot3d import Axes3D
#  import matplotlib.pyplot as plt
#  import numpy as np
#  import pandas as pd
#
#
#  def get_solution(filename: str) -> np.ndarray:
#      """Reads data from data/<filename>.csv.
#
#      Arguments:
#          filename: Name of file in `data`-folder, without the .csv file ending.
#                    Data must be on a format that np.read_csv can read, with the
#                    first column being time, and the next three columns being x, y
#                    and z positions.
#
#      Return:
#          Array with all values.
#      """
#      #  return np.read_csv(f"data/{filename}.csv")
#      #  import os
#
#      return pd.read_csv(f"data/{filename}.csv")
#
#
#
#
#  def plot_relative_error(
#      ax: matplotlib.axes, analytical_filename: str, numerical_filename: str, label: str
#  ):
#      """Plot the total relative error of numerical solution.
#
#      Total relative error is the sum of relative errors for each axis.
#
#      Arguments:
#          ax: Axes instance to plot on.
#          analytical_filename: Name of file to read, with analytical solution. See
#                               the function `get_solution` for details on format.
#          numerical_filename: Name of file to read, with numerical solution. See
#                              the function `get_solution` for details on format.
#          label: Label to put on plot.
#      """
#      t, analytical_x, analytical_y, analytical_z = get_solution(analytical_filename)
#      _, numerical_x, numerical_y, numerical_z = get_solution(numerical_filename)
#
#      total_error = np.sum(
#          relative_error(analytical_x, numerical_x)
#          + relative_error(analytical_y, numerical_y)
#          + relative_error(analytical_z, numerical_z),
#          axis=0,
#      )
#
#      plt.plot(t, total_error, label=label)
#
#
#  def relative_error(exact: np.ndarray, approximated: np.ndarray) -> np.ndarray:
#      """Computes the relative error.
#
#      Arguments:
#          exact: Exact computed.
#          approximated: An approximate array.
#
#      Return:
#          Relative error.
#      """
#      return np.abs((exact - approximated) / exact)
#


def plot_all_solutions():
    fig = plt.figure()
    ax = Axes3D(fig)
    plot_3d_solution(ax, "analytical_positons", "Analytical solution")
    plot_3d_solution(ax, "forward_euler_one_particle", "Forward Euler solution")
    plot_3d_solution(ax, "runge_kutta_positons_one_particle", "Runge-Kutta 4 solution")
    plt.legend()
    plt.savefig(f"data/position_estimates.pdf")
    plt.show()


def plot_frequencies_rough():
    fig, axs = plt.subplots(3, sharex=True, sharey=True)
    fig.suptitle(r"Particles left after $500 \mu s$")
    fig.text(0.5, 0.03, r"$\omega_V \, [MHz]$", ha="center", fontsize="small")
    fig.text(
        0.04, 0.5, "#particles", va="center", rotation="vertical", fontsize="small"
    )
    filenames = [
        "amplitude0.100000.csv",
        "amplitude0.400000.csv",
        "amplitude0.700000.csv",
    ]
    # fig.xlabel(r"$\omega_V \, [MHz]$")
    fs = ["0,1", "0,4", "0,7"]
    for i in range(3):
        df = pd.read_csv(f"data/{filenames[i]}")
        df.columns = df.columns.str.replace(" ", "_")
        axs[i].set_title(f"Amplitude = {fs[i]}")
        axs[i].plot(df.omega_V, df.particles_left, "o", markersize=2)
    plt.savefig(f"data/particles_left_rough_grained.pdf")
    plt.show()


# TODO!
def plot_frequencies_fine():
    print("NOTE: Fine is not implemented yet")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get plots for the simulation for the penning trap problem"
    )
    parser.add_argument(
        "-s",
        "--solution",
        help="To plot RK4, FE and analytical solution.",
        action="store_true",
    )
    parser.add_argument(
        "-r",
        "--rough",
        help="To plot rough-grained scan of frequencies for particles",
        action="store_true",
    )
    parser.add_argument(
        "-f",
        "--fine",
        help="To plot fine-grained scan of frequencies for particles",
        action="store_true",
    )
    parser.add_argument(
        "-e",
        "--error",
        help="To plot relative error of the Runge-Kutta and Forward-Euler",
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--converge",
        help="To plot convergence rate of the Runge-Kutta and Forward-Euler",
        action="store_true",
    )
    parser.add_argument(
        "-a",
        "--all",
        help="To plot all",
        action="store_true",
    )
    args = parser.parse_args()
    if not any(vars(args).values()):
        parser.print_help()
    if args.solution or args.all:
        plot_all_solutions()
    if args.rough or args.all:
        plot_frequencies_rough()
    if args.fine or args.all:
        plot_frequencies_fine()
    if args.error or args.all:
        plot_error()
    if args.converge or args.all:
        plot_convergence_rate()