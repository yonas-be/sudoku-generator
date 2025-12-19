# Code to export a Sudoku to pdf file

from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime

def export_to_pdf(
        grid,
        solution = [],
        filename="sudoku.pdf",
        enable_text_fields: bool = False,
        show_solution: bool = False,
        difficulty: str = "medium",
        seed: int | None = None
):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Margins
    margin = 100
    grid_size = min(width, height) - 2 * margin
    cell_size = grid_size / 9

    # Puzzle spacing to the top of the page
    top_spacing = 100

    # ---- Page 1: Puzzle ----
    def draw_header(title, difficulty, seed):
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.darkgrey)
        c.drawString(50, height - 30, f"Difficulty: {difficulty.upper()}")
        c.drawRightString(width - 50, height - 30, f"Seed: {seed}")
        c.drawCentredString(width / 2, height - 30, f"Generated: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width / 2, height - 70, title)

    def draw_grid(side_margin, grid_size, cell_size, top_spacing):
        for i in range(10):
            line_width = 2 if i % 3 == 0 else 0.8
            c.setLineWidth(line_width)
            y = height - top_spacing - i * cell_size
            x = side_margin + i * cell_size
            c.line(side_margin, y, side_margin + grid_size, y)
            c.line(x, height - top_spacing, x, height - top_spacing - grid_size)

    draw_header("Sudoku", difficulty, seed)
    draw_grid(margin, grid_size, cell_size, top_spacing)

    # Draw numbers
    for r in range(9):
        for c_col in range(9):

            if grid[r][c_col] != 0:
                c.setFont("Helvetica", int(cell_size / 1.7))
                num = grid[r][c_col]
                x = margin + c_col * cell_size + cell_size / 3
                y = height - top_spacing - (r + 1) * cell_size + cell_size / 4
                c.drawString(x, y, str(num))

            if enable_text_fields:
                if grid[r][c_col] == 0:     #add text input field
                    field_size = cell_size * 0.8
                    offset = (cell_size - field_size) / 2
                    x = margin + c_col * cell_size + offset
                    y = height - top_spacing - (r + 1) * cell_size + offset

                    c.acroForm.textfield(
                        name=f"cell_{r}_{c_col}",
                        x=x,
                        y=y,
                        width=field_size,
                        height=field_size,
                        borderStyle='solid',  # or 'none'
                        borderColor=colors.black,  # only if using a border
                        fillColor=colors.lightgrey,
                        forceBorder=True,  # ensures border is drawn if borderStyle is set
                        fontSize=int(field_size * 0.8),
                        maxlen=1
                    )

    c.showPage()  # finish page 1


    # ---- Page 2: Solution ----
    if show_solution:
        draw_header("Solution", difficulty, seed)
        draw_grid(margin, grid_size, cell_size, top_spacing)

        c.setFont("Helvetica", int(cell_size / 1.7))
        for r in range(9):
            for c_col in range(9):
                if grid[r][c_col] != 0:
                    num = grid[r][c_col]
                    x = margin + c_col * cell_size + cell_size / 3
                    y = height - top_spacing - (r + 1) * cell_size + cell_size / 4
                    c.drawString(x, y, str(num))

                else:   # Number from solution
                    c.setFillColor(colors.green)
                    num = solution[r][c_col]
                    x = margin + c_col * cell_size + cell_size / 3
                    y = height - top_spacing - (r + 1) * cell_size + cell_size / 4
                    c.drawString(x, y, str(num))
                    c.setFillColor(colors.black)

        c.setFont("Helvetica", 10)
        c.setFillColor(colors.lightgrey)
        c.drawRightString(width - 20, 20, f"seed {seed}")
        c.setFillColor(colors.black)

        c.showPage()  # finish page 2

    c.save()