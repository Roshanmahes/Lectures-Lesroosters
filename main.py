from helpers import classes, functions, state_space
from helpers.score import score

import algorithms.make_schedule as make_schedule
from algorithms.hill_climb import hill_climb
import algorithms.temperature as temperature
from algorithms.simulated_annealing import simulated_annealing

def main():
    """
    Executes main.py.
    """
    courses, halls, students = functions.init_data()

    # run some algorithms here
    # for example:
    # print(state_space.calculate(courses, len(halls)))
    # to calculate and print the state_space or
    # print(score(make_schedule.random_sample(courses, halls), courses))
    # to print the score of a random schedule

if __name__ == "__main__":
    main()
