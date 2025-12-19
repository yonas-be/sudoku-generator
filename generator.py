import time
import random
import argparse
import copy

from exportpdf import export_to_pdf
from sudokulogic import generate, solve

#-----------------------------
# Global variables
#-----------------------------
SOLUTIONS = 0

#-----------------------------
# Functions
#-----------------------------

def main():
    parser = argparse.ArgumentParser(description="Sudoku generator -> PDF")
    parser.add_argument(
        "--difficulty", "-d",
        choices=["easy", "medium", "hard", "hardcore"],
        default="medium"
    )
    parser.add_argument(
        "--output", "-o",
        default="sudoku.pdf"
    )
    parser.add_argument(
        "--text-fields",
        action="store_true",
        help="Add PDF text fields to solve on computer"
    )
    parser.add_argument(
        "--with-solution",
        action="store_true",
        help="Include a second page with the solution"
    )
    parser.add_argument(
        "--seed", "-s",
        type=int,
        help="Seed for random number generator"
    )

    args = parser.parse_args()

    if args.seed is None:
        args.seed = random.randint(1000000000000000, 9999999999999999)
    random.seed(args.seed)

    print(f"Generating...")
    start = time.time()
    p = generate(args.difficulty)
    end = time.time()

    solution = copy.deepcopy(p)
    if args.with_solution:
        solve(solution)

    export_to_pdf(p, solution, args.output, args.text_fields, args.with_solution, args.difficulty, args.seed)

    print(f"Saved {args.output} (difficulty={args.difficulty}, solution page={'yes' if args.with_solution else 'no'}, text fields={'yes' if args.text_fields else 'no'}, seed={args.seed})")
    print(f"Generator took " + str(round(end - start, 3)) + " seconds to generate the puzzle.")


if __name__ == "__main__":
    main()