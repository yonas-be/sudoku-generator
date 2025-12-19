# sudoku-generator

A Python Sudoku generator that creates **unique puzzles** and exports them as PDFs.  
Supports difficulty levels, random seeds, and optional solution pages.

---

## Features

- Generates valid Sudokus with exactly one solution
- Difficulty levels: easy, medium, hard, hardcore
- Seed-based generation (reproducible puzzles)
- Export to PDF
- Optional interactive PDF input fields
- Optional solution page

---

## Requirements

- Python 3.10+
- `reportlab`

Install dependencies:
pip install reportlab

---

## Usage

### Generate a basic puzzle
run in cmd:
python generator.py

### More generating options
use **--difficulty** {"easy", "medium", "hard", or "hardcore"}  (do not use hardcore; it tries until 60 numbers are removed. This leads to the algorithm taking an insane amount of time)
use **--with-solution** to add the solution on the next page
use **--text-fields** to add text fields in pdf
use **--seed** or **-s** to input your custom seed (e.g. for generating a solution for the same puzzle later)
use **--output** or **-o** to set a file name and location

---

## How it works

1. Generate a fully solved Sudoku
2. Remove numbers while ensuring a unique solution
3. Use random seed for reproducibility
4. Export puzzle to PDF

---

## License

MIT License

