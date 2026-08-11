var pixel_fields = [];

var snake = [];

var direction_x = 1;
var direction_y = 0;


/*
 * Initialize PDF fields
 */
function game_init() {

    for (var x = 0; x < GRID_WIDTH; x++) {

        pixel_fields[x] = [];

        for (var y = 0; y < GRID_HEIGHT; y++) {

            pixel_fields[x][y] =
                this.getField("P_" + x + "_" + y);
        }
    }


    /*
     * Starting snake
     */

    snake = [
        [10, 10],
        [9, 10],
        [8, 10]
    ];


    draw();


    /*
     * Move every 400 ms
     */

    app.setInterval(
        "move_snake();",
        400
    );
}


/*
 * Draw one cell
 */
function set_pixel(x, y, state) {

    if (x < 0 ||
        y < 0 ||
        x >= GRID_WIDTH ||
        y >= GRID_HEIGHT) {

        return;
    }


    var pixel =
        pixel_fields[x][GRID_HEIGHT - 1 - y];


    pixel.hidden = false;


    if (state) {

        pixel.fillColor = color.black;

    } else {

        pixel.fillColor = color.white;
    }
}


/*
 * Draw the whole game
 */
function draw() {

    var x;
    var y;


    /*
     * Clear board
     */

    for (x = 0; x < GRID_WIDTH; x++) {

        for (y = 0; y < GRID_HEIGHT; y++) {

            set_pixel(x, y, false);
        }
    }


    /*
     * Draw snake
     */

    for (var i = 0; i < snake.length; i++) {

        x = snake[i][0];
        y = snake[i][1];

        set_pixel(x, y, true);
    }
}


/*
 * Move snake
 */
function move_snake() {

    var head_x = snake[0][0];

    var head_y = snake[0][1];


    var new_x =
        head_x + direction_x;

    var new_y =
        head_y + direction_y;


    /*
     * Add new head
     */

    snake.unshift([
        new_x,
        new_y
    ]);


    /*
     * Remove tail
     */

    snake.pop();


    draw();
}


/*
 * Keyboard controls
 */
function handle_input(event) {

    if (event.change == "w") {

        direction_x = 0;
        direction_y = 1;
    }

    if (event.change == "a") {

        direction_x = -1;
        direction_y = 0;
    }

    if (event.change == "s") {

        direction_x = 0;
        direction_y = -1;
    }

    if (event.change == "d") {

        direction_x = 1;
        direction_y = 0;
    }
}


game_init();

app.execMenuItem("FitPage");