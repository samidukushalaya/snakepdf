#include <stdlib.h>
#include <time.h>
#include <emscripten/emscripten.h>

#define SNAKE_HEAD_CHAR 'O'
#define SNAKE_BODY_CHAR 'o'
#define SPACE_CHAR ' '
#define WALL_CHAR '#'
#define FOOD_CHAR '@'

typedef struct {
    int x;
    int y;
} vec2d;

#define WIDTH 20
#define HEIGHT 10
#define MAX_SNAKE_SIZE (WIDTH * HEIGHT)

char frameBuffer[WIDTH][HEIGHT];

int snakeSize = 0;
vec2d foodPos;
vec2d snake[MAX_SNAKE_SIZE];

int gameOver = 0;


int manhattanDistance(
    const int x1,
    const int y1,
    const int x2,
    const int y2
) {
    int xDiff = x2 - x1;
    int yDiff = y2 - y1;

    if (xDiff < 0)
        xDiff = -xDiff;

    if (yDiff < 0)
        yDiff = -yDiff;

    return xDiff + yDiff;
}


int randInRange(const int lower, const int upper) {
    return (rand() % (upper - lower + 1)) + lower;
}


void clearBuffer(void) {
    int x;
    int y;

    for (x = 0; x < WIDTH; x++) {
        for (y = 0; y < HEIGHT; y++) {
            frameBuffer[x][y] = WALL_CHAR;
        }
    }

    for (y = 1; y < HEIGHT - 1; y++) {
        for (x = 1; x < WIDTH - 1; x++) {
            frameBuffer[x][y] = SPACE_CHAR;
        }
    }
}


int checkCollision(const int x, const int y) {

    /* Wall collision */
    if (x >= WIDTH - 1 ||
        x <= 0 ||
        y >= HEIGHT - 1 ||
        y <= 0) {

        return 1;
    }

    /* Snake body collision */
    for (int i = 0; i < snakeSize; i++) {

        if (x == snake[i].x &&
            y == snake[i].y) {

            return 1;
        }
    }

    return 0;
}


void createFood(void) {

    int xfood;
    int yfood;

    do {
        xfood = randInRange(1, WIDTH - 2);
        yfood = randInRange(1, HEIGHT - 2);

    } while (checkCollision(xfood, yfood));

    foodPos.x = xfood;
    foodPos.y = yfood;
}


void snakeAddPart(const int x, const int y) {

    if (snakeSize >= MAX_SNAKE_SIZE)
        return;

    snake[snakeSize].x = x;
    snake[snakeSize].y = y;

    snakeSize++;
}


void snakeMove(const int xmove, const int ymove) {

    const int xNewHead = snake[0].x + xmove;
    const int yNewHead = snake[0].y + ymove;

    if (checkCollision(xNewHead, yNewHead)) {
        gameOver = 1;
        return;
    }

    /*
     * Food eaten.
     *
     * Save the old tail position before moving
     * the snake. This gives the new body segment
     * a valid position.
     */
    int grow = 0;

    if (xNewHead == foodPos.x &&
        yNewHead == foodPos.y) {

        grow = 1;
    }

    int oldTailX = snake[snakeSize - 1].x;
    int oldTailY = snake[snakeSize - 1].y;

    if (grow) {
        snakeAddPart(oldTailX, oldTailY);
        createFood();
    }

    /* Move body */
    for (int i = snakeSize - 1; i >= 1; i--) {

        snake[i].x = snake[i - 1].x;
        snake[i].y = snake[i - 1].y;
    }

    /* Move head */
    snake[0].x = xNewHead;
    snake[0].y = yNewHead;
}


void snakeThink(void) {

    const vec2d destinations[4] = {
        { snake[0].x + 1, snake[0].y },
        { snake[0].x - 1, snake[0].y },
        { snake[0].x, snake[0].y + 1 },
        { snake[0].x, snake[0].y - 1 }
    };

    vec2d bestMove;

    int bestDistance = -1;

    for (int i = 0; i < 4; i++) {

        int dist = manhattanDistance(
            destinations[i].x,
            destinations[i].y,
            foodPos.x,
            foodPos.y
        );

        if (dist < bestDistance ||
            bestDistance == -1) {

            if (!checkCollision(
                    destinations[i].x,
                    destinations[i].y)) {

                bestDistance = dist;
                bestMove = destinations[i];
            }
        }
    }

    if (bestDistance != -1) {

        snakeMove(
            bestMove.x - snake[0].x,
            bestMove.y - snake[0].y
        );

    } else {

        gameOver = 1;
    }
}


void gameToBuffer(void) {

    /* Reset board */
    clearBuffer();

    /* Food */
    frameBuffer[foodPos.x][foodPos.y] = FOOD_CHAR;

    /* Snake */
    for (int i = 0; i < snakeSize; i++) {

        if (i == 0) {
            frameBuffer[
                snake[i].x
            ][
                snake[i].y
            ] = SNAKE_HEAD_CHAR;

        } else {
            frameBuffer[
                snake[i].x
            ][
                snake[i].y
            ] = SNAKE_BODY_CHAR;
        }
    }
}


void resetGame(void) {

    snakeSize = 0;
    gameOver = 0;

    srand((unsigned int)time(NULL));

    /*
     * Start the snake in the middle.
     */
    int startX = WIDTH / 2;
    int startY = HEIGHT / 2;

    snakeAddPart(startX, startY);
    snakeAddPart(startX - 1, startY);
    snakeAddPart(startX - 2, startY);

    createFood();

    gameToBuffer();
}


/*
 * Called from JavaScript.
 */
EMSCRIPTEN_KEEPALIVE
void initGame(void) {

    resetGame();
}


/*
 * Advance the game by one step.
 *
 * JavaScript will call this repeatedly
 * using its own timer.
 */
EMSCRIPTEN_KEEPALIVE
void updateGame(void) {

    if (gameOver)
        return;

    snakeThink();

    gameToBuffer();
}


/*
 * Get one board cell.
 *
 * JavaScript can call:
 *
 * getCell(x, y)
 *
 * and receive:
 *
 * '#' = wall
 * ' ' = empty
 * 'O' = snake head
 * 'o' = snake body
 * '@' = food
 */
EMSCRIPTEN_KEEPALIVE
int getCell(const int x, const int y) {

    if (x < 0 ||
        x >= WIDTH ||
        y < 0 ||
        y >= HEIGHT) {

        return 0;
    }

    return frameBuffer[x][y];
}


EMSCRIPTEN_KEEPALIVE
int getWidth(void) {
    return WIDTH;
}


EMSCRIPTEN_KEEPALIVE
int getHeight(void) {
    return HEIGHT;
}


EMSCRIPTEN_KEEPALIVE
int getSnakeSize(void) {
    return snakeSize;
}


EMSCRIPTEN_KEEPALIVE
int isGameOver(void) {
    return gameOver;
}