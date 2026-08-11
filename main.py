from pdf_template import PDF_TEMPLATE
from pdf_object import PIXEL_OBJ


# ==========================================
# SETTINGS
# ==========================================

GRID_WIDTH = 20
GRID_HEIGHT = 20

PX_SIZE = 20

GRID_OFF_X = 100
GRID_OFF_Y = 180


# ==========================================
# LOAD SNAKE JAVASCRIPT
# ==========================================

with open("snake.js", "r") as file:

    game_js = file.read()


# Replace JavaScript constants

game_js = game_js.replace(
    "GRID_WIDTH",
    str(GRID_WIDTH)
)

game_js = game_js.replace(
    "GRID_HEIGHT",
    str(GRID_HEIGHT)
)


# ==========================================
# PDF OBJECTS
# ==========================================

fields = []

obj_idx = 50


# ==========================================
# CREATE PIXELS
# ==========================================

for x in range(GRID_WIDTH):

    for y in range(GRID_HEIGHT):

        pixel = PIXEL_OBJ

        pixel = pixel.replace(
            "###IDX###",
            str(obj_idx)
        )

        pixel = pixel.replace(
            "###X###",
            str(x)
        )

        pixel = pixel.replace(
            "###Y###",
            str(y)
        )

        pixel = pixel.replace(
            "###RECT###",
            f"{GRID_OFF_X + x * PX_SIZE} "
            f"{GRID_OFF_Y + y * PX_SIZE} "
            f"{GRID_OFF_X + (x + 1) * PX_SIZE} "
            f"{GRID_OFF_Y + (y + 1) * PX_SIZE}"
        )

        fields.append(pixel)

        obj_idx += 1


# ==========================================
# FIELD LIST
# ==========================================

field_list = " ".join(
    f"{i} 0 R"
    for i in range(50, obj_idx)
)


# ==========================================
# BUILD PDF
# ==========================================

pdf = PDF_TEMPLATE

pdf = pdf.replace(
    "###FIELD_LIST###",
    field_list
)

pdf = pdf.replace(
    "###GAME_JS###",
    game_js
)

pdf = pdf.replace(
    "###FIELD_OBJECTS###",
    "\n".join(fields)
)


# ==========================================
# WRITE PDF
# ==========================================

with open("snake.pdf", "w") as file:

    file.write(pdf)


print("snake.pdf created")