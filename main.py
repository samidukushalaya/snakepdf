PDF_FILE_TEMPLATE = """
%PDF-1.6

% Root
1 0 obj
<<
  /AcroForm <<
    /Fields [ ###FIELD_LIST### ]
  >>
  /Pages 2 0 R
  /OpenAction 17 0 R
  /Type /Catalog
>>
endobj

2 0 obj
<<
  /Count 1
  /Kids [
    16 0 R
  ]
  /Type /Pages
>>

%% Annots Page 1 (also used as overall fields list)
21 0 obj
[
  ###FIELD_LIST###
]
endobj

###FIELDS###

%% Page 1
16 0 obj
<<
  /Annots 21 0 R
  /Contents 3 0 R
  /CropBox [
    0.0
    0.0
    612.0
    792.0
  ]
  /MediaBox [
    0.0
    0.0
    612.0
    792.0
  ]
  /Parent 2 0 R
  /Resources <<
  >>
  /Rotate 0
  /Type /Page
>>
endobj

3 0 obj
<< >>
stream
endstream
endobj

17 0 obj
<<
  /JS 42 0 R
  /S /JavaScript
>>
endobj


42 0 obj
<< >>
stream

// Hacky wrapper to work with a callback instead of a string
function setInterval(cb, ms) {
	evalStr = "(" + cb.toString() + ")();";
	return app.setInterval(evalStr, ms);
}

// https://gist.github.com/blixt/f17b47c62508be59987b
var rand_seed = Date.now() % 2147483647;
function rand() {
	return rand_seed = rand_seed * 16807 % 2147483647;
}

var TICK_INTERVAL = ###TICK_INTERVAL###;

// Globals
var pixel_fields = [];
var snake = [];
var dir = { dx: 1, dy: 0 };
var next_dir = { dx: 1, dy: 0 };
var food = { x: 0, y: 0 };
var score = 0;
var interval = 0;
var started = false;

var COLOR_EMPTY = ["RGB", 0.85, 0.85, 0.85];
var COLOR_SNAKE = ["RGB", 0, 0, 0];
var COLOR_HEAD  = ["RGB", 0, 0, 0];
var COLOR_FOOD  = ["RGB", 0.8, 0.15, 0.15];

function set_controls_visibility(state) {
	this.getField("T_input").hidden = !state;
	this.getField("B_up").hidden = !state;
	this.getField("B_down").hidden = !state;
	this.getField("B_left").hidden = !state;
	this.getField("B_right").hidden = !state;
}

function cell_has_snake(x, y) {
	for (var i = 0; i < snake.length; ++i) {
		if (snake[i].x == x && snake[i].y == y) {
			return true;
		}
	}
	return false;
}

function spawn_food() {
	var x, y;
	do {
		x = rand() % ###GRID_WIDTH###;
		if (x < 0) x += ###GRID_WIDTH###;
		y = rand() % ###GRID_HEIGHT###;
		if (y < 0) y += ###GRID_HEIGHT###;
	} while (cell_has_snake(x, y));
	food = { x: x, y: y };
}

function game_init() {
	// Gather references to pixel field objects
	for (var x = 0; x < ###GRID_WIDTH###; ++x) {
		pixel_fields[x] = [];
		for (var y = 0; y < ###GRID_HEIGHT###; ++y) {
			pixel_fields[x][y] = this.getField(`P_${x}_${y}`);
		}
	}

	snake = [
		{ x: 7, y: 7 },
		{ x: 6, y: 7 },
		{ x: 5, y: 7 }
	];
	dir = { dx: 1, dy: 0 };
	next_dir = { dx: 1, dy: 0 };
	score = 0;
	draw_updated_score();
	spawn_food();

	// Hide start button, show controls
	this.getField("B_start").hidden = true;
	set_controls_visibility(true);

	draw();

	// Start timer
	interval = setInterval(game_tick, TICK_INTERVAL);
	started = true;
}

function set_direction(dx, dy) {
	// Disallow reversing directly into ourselves
	if (dx == -dir.dx && dy == -dir.dy) {
		return;
	}
	next_dir = { dx: dx, dy: dy };
}

function handle_input(event) {
	switch (event.change) {
		case 'w': set_direction(0, -1); break;
		case 's': set_direction(0, 1); break;
		case 'a': set_direction(-1, 0); break;
		case 'd': set_direction(1, 0); break;
	}
}

function game_over() {
	app.clearInterval(interval);
	started = false;
	app.alert(`Game over! Score: ${score}`);
	this.getField("B_start").hidden = false;
	set_controls_visibility(false);
}

function step() {
	dir = next_dir;
	var head = snake[0];
	var new_head = { x: head.x + dir.dx, y: head.y + dir.dy };

	// wall collision
	if (new_head.x < 0 || new_head.x >= ###GRID_WIDTH### || new_head.y < 0 || new_head.y >= ###GRID_HEIGHT###) {
		game_over();
		return;
	}

	// self collision
	if (cell_has_snake(new_head.x, new_head.y)) {
		game_over();
		return;
	}

	snake.unshift(new_head);

	if (new_head.x == food.x && new_head.y == food.y) {
		score++;
		draw_updated_score();
		spawn_food();
	} else {
		snake.pop();
	}
}

function draw_updated_score() {
	this.getField("T_score").value = `Score: ${score}`;
}

function draw() {
	for (var x = 0; x < ###GRID_WIDTH###; ++x) {
		for (var y = 0; y < ###GRID_HEIGHT###; ++y) {
			pixel_fields[x][###GRID_HEIGHT### - 1 - y].fillColor = COLOR_EMPTY;
		}
	}
	for (var i = snake.length - 1; i >= 0; --i) {
		var seg = snake[i];
		pixel_fields[seg.x][###GRID_HEIGHT### - 1 - seg.y].fillColor = (i == 0) ? COLOR_HEAD : COLOR_SNAKE;
	}
	pixel_fields[food.x][###GRID_HEIGHT### - 1 - food.y].fillColor = COLOR_FOOD;
}

function game_tick() {
	if (!started) return;
	step();
	if (started) draw();
}

// Hide controls to start with
set_controls_visibility(false);

// Zoom to fit (on FF)
app.execMenuItem("FitPage");

endstream
endobj


18 0 obj
<<
  /JS 43 0 R
  /S /JavaScript
>>
endobj


43 0 obj
<< >>
stream



endstream
endobj

trailer
<<
  /Root 1 0 R
>>

%%EOF
"""

PLAYING_FIELD_OBJ = """
###IDX### obj
<<
  /FT /Btn
  /Ff 1
  /MK <<
    /BG [
      0.8
    ]
    /BC [
      0 0 0
    ]
  >>
  /Border [ 0 0 1 ]
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (playing_field)
  /Type /Annot
>>
endobj
"""

PIXEL_OBJ = """
###IDX### obj
<<
  /FT /Btn
  /Ff 1
  /MK <<
    /BG [
      ###COLOR###
    ]
    /BC [
      0.5 0.5 0.5
    ]
  >>
  /Border [ 0 0 1 ]
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (P_###X###_###Y###)
  /Type /Annot
>>
endobj
"""

BUTTON_AP_STREAM = """
###IDX### obj
<<
  /BBox [ 0.0 0.0 ###WIDTH### ###HEIGHT### ]
  /FormType 1
  /Matrix [ 1.0 0.0 0.0 1.0 0.0 0.0]
  /Resources <<
    /Font <<
      /HeBo 10 0 R
    >>
    /ProcSet [ /PDF /Text ]
  >>
  /Subtype /Form
  /Type /XObject
>>
stream
q
0.75 g
0 0 ###WIDTH### ###HEIGHT### re
f
Q
q
1 1 ###WIDTH### ###HEIGHT### re
W
n
BT
/HeBo 12 Tf
0 g
10 8 Td
(###TEXT###) Tj
ET
Q
endstream
endobj
"""

BUTTON_OBJ = """
###IDX### obj
<<
  /A <<
	  /JS ###SCRIPT_IDX### R
	  /S /JavaScript
	>>
  /AP <<
    /N ###AP_IDX### R
  >>
  /F 4
  /FT /Btn
  /Ff 65536
  /MK <<
    /BG [
      0.75
    ]
    /CA (###LABEL###)
  >>
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (###NAME###)
  /Type /Annot
>>
endobj
"""

TEXT_OBJ = """
###IDX### obj
<<
	/AA <<
		/K <<
			/JS ###SCRIPT_IDX### R
			/S /JavaScript
		>>
	>>
	/F 4
	/FT /Tx
	/MK <<
	>>
	/MaxLen 0
	/P 16 0 R
	/Rect [
		###RECT###
	]
	/Subtype /Widget
	/T (###NAME###)
	/V (###LABEL###)
	/Type /Annot
>>
endobj
"""

STREAM_OBJ = """
###IDX### obj
<< >>
stream
###CONTENT###
endstream
endobj
"""

PX_SIZE = 20
GRID_WIDTH = 15
GRID_HEIGHT = 15
GRID_OFF_X = 180
GRID_OFF_Y = 380
TICK_INTERVAL = 400  # ms per snake step

fields_text = ""
field_indexes = []
obj_idx_ctr = 50


def add_field(field):
	global fields_text, field_indexes, obj_idx_ctr
	fields_text += field
	field_indexes.append(obj_idx_ctr)
	obj_idx_ctr += 1


# Playing field outline
playing_field = PLAYING_FIELD_OBJ
playing_field = playing_field.replace("###IDX###", f"{obj_idx_ctr} 0")
playing_field = playing_field.replace("###RECT###", f"{GRID_OFF_X} {GRID_OFF_Y} {GRID_OFF_X+GRID_WIDTH*PX_SIZE} {GRID_OFF_Y+GRID_HEIGHT*PX_SIZE}")
add_field(playing_field)

for x in range(GRID_WIDTH):
	for y in range(GRID_HEIGHT):
		pixel = PIXEL_OBJ
		pixel = pixel.replace("###IDX###", f"{obj_idx_ctr} 0")
		c = [0.85, 0.85, 0.85]
		pixel = pixel.replace("###COLOR###", f"{c[0]} {c[1]} {c[2]}")
		pixel = pixel.replace("###RECT###", f"{GRID_OFF_X+x*PX_SIZE} {GRID_OFF_Y+y*PX_SIZE} {GRID_OFF_X+x*PX_SIZE+PX_SIZE} {GRID_OFF_Y+y*PX_SIZE+PX_SIZE}")
		pixel = pixel.replace("###X###", f"{x}")
		pixel = pixel.replace("###Y###", f"{y}")
		add_field(pixel)


def add_button(label, name, x, y, width, height, js):
	script = STREAM_OBJ
	script = script.replace("###IDX###", f"{obj_idx_ctr} 0")
	script = script.replace("###CONTENT###", js)
	add_field(script)

	ap_stream = BUTTON_AP_STREAM
	ap_stream = ap_stream.replace("###IDX###", f"{obj_idx_ctr} 0")
	ap_stream = ap_stream.replace("###TEXT###", label)
	ap_stream = ap_stream.replace("###WIDTH###", f"{width}")
	ap_stream = ap_stream.replace("###HEIGHT###", f"{height}")
	add_field(ap_stream)

	button = BUTTON_OBJ
	button = button.replace("###IDX###", f"{obj_idx_ctr} 0")
	button = button.replace("###SCRIPT_IDX###", f"{obj_idx_ctr-2} 0")
	button = button.replace("###AP_IDX###", f"{obj_idx_ctr-1} 0")
	button = button.replace("###NAME###", name if name else f"B_{obj_idx_ctr}")
	button = button.replace("###RECT###", f"{x} {y} {x + width} {y + height}")
	add_field(button)


def add_text(label, name, x, y, width, height, js):
	script = STREAM_OBJ
	script = script.replace("###IDX###", f"{obj_idx_ctr} 0")
	script = script.replace("###CONTENT###", js)
	add_field(script)

	text = TEXT_OBJ
	text = text.replace("###IDX###", f"{obj_idx_ctr} 0")
	text = text.replace("###SCRIPT_IDX###", f"{obj_idx_ctr-1} 0")
	text = text.replace("###LABEL###", label)
	text = text.replace("###NAME###", name)
	text = text.replace("###RECT###", f"{x} {y} {x + width} {y + height}")
	add_field(text)


grid_center_x = GRID_OFF_X + (GRID_WIDTH * PX_SIZE) / 2
grid_center_y = GRID_OFF_Y + (GRID_HEIGHT * PX_SIZE) / 2

# D-pad controls below the grid
add_button("<", "B_left", GRID_OFF_X + 45, GRID_OFF_Y - 100, 50, 50, "set_direction(-1, 0);")
add_button(">", "B_right", GRID_OFF_X + 165, GRID_OFF_Y - 100, 50, 50, "set_direction(1, 0);")
add_button("^", "B_up", GRID_OFF_X + 105, GRID_OFF_Y - 70, 50, 50, "set_direction(0, -1);")
add_button("v", "B_down", GRID_OFF_X + 105, GRID_OFF_Y - 130, 50, 50, "set_direction(0, 1);")

# Start button, centered over the grid
add_button("Start game", "B_start", grid_center_x - 50, grid_center_y - 50, 100, 100, "game_init();")

# Keyboard input (WASD) + score
add_text("Type here for keyboard controls (WASD)", "T_input", GRID_OFF_X, GRID_OFF_Y - 220, GRID_WIDTH * PX_SIZE, 50, "handle_input(event);")
add_text("Score: 0", "T_score", GRID_OFF_X + GRID_WIDTH * PX_SIZE + 10, GRID_OFF_Y + GRID_HEIGHT * PX_SIZE - 30, 100, 30, "")

filled_pdf = PDF_FILE_TEMPLATE.replace("###FIELDS###", fields_text)
filled_pdf = filled_pdf.replace("###FIELD_LIST###", " ".join([f"{i} 0 R" for i in field_indexes]))
filled_pdf = filled_pdf.replace("###GRID_WIDTH###", f"{GRID_WIDTH}")
filled_pdf = filled_pdf.replace("###GRID_HEIGHT###", f"{GRID_HEIGHT}")
filled_pdf = filled_pdf.replace("###TICK_INTERVAL###", f"{TICK_INTERVAL}")

with open("snake.pdf", "w") as pdffile:
	pdffile.write(filled_pdf)

print("done")