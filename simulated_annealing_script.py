from sys import argv

from helpers import classes, functions
from helpers.score import score

from algorithms import make_schedule, temperature
from algorithms.simulated_annealing import simulated_annealing

def main(iters=None):
    """
    Run the simulated_annealing algorithm, with the linear temperature function,
    starting at a random schedule. The data is saved in
    results/simulated_annealing.txt. The score of the initial and final
    schedules is printed.

    A commandline integer may be issued to set the number of iterations.
    The default value is 100000 which takes approximately 10 minutes.
    """
    courses, halls, students = functions.init_data()

    schedule = make_schedule.random_sample(courses, halls)
    print(score(schedule, courses))

    if iters:
        new_schedule = simulated_annealing(schedule, courses, halls, \
                temperature.linear, total_iters=iters)
    else:
        new_schedule = simulated_annealing(schedule, courses, halls, \
                temperature.linear)
    print(score(new_schedule, courses))


if __name__ == "__main__":
    if len(argv) > 1:
        try:
            iters = int(argv[1])
        except ValueError:
            iters = 0
    if iters > 0:
        main(iters)
    else:
        main()
