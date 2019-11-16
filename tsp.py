import argparse

from src.hameltonian import brute_force, dynamic
from src.tools import load_tsp, plot


def solve(method, filename, do_plot=False):
    """
    Call the requested solve method and display results
    """
    points = load_tsp(filename)
    if method == "brute_force":
        (result, tour) = brute_force(points)
    elif method == "dynamic":
        # A lot of memory is needed
        (result, tour) = dynamic(points)

    print(f"Lowest cost: {result}")
    print(f"Optimal tour: {tour}")
    if do_plot:
        plot(points, tour)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(prog="tsp")
    PARSER.add_argument("method", type=str)
    PARSER.add_argument("filename", type=str)
    PARSER.add_argument("-p", "--plot", action="store_true", help="Display plot")
    ARGS = PARSER.parse_args()

    if ARGS.method in ("brute_force", "dynamic"):
        solve(ARGS.method, ARGS.filename, ARGS.plot)
    else:
        print(f"Invalid method {ARGS.method}")
