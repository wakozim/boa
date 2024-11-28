import random
from typing import List
from enum import IntEnum, auto

from .raylib import *


VELOCITY  = Vector2(1, 1)
CELL_SIZE = Vector2(50, 50)
COLS      = 10
ROWS      = 10


class Direction(IntEnum):
    LEFT  = auto()
    RIGHT = auto()
    DOWN  = auto()
    UP    = auto()


directions = {
    Direction.LEFT:  Vector2(-1, 0),
    Direction.RIGHT: Vector2(1, 0),
    Direction.DOWN:  Vector2(0, 1),
    Direction.UP:    Vector2(0, -1)
}


class Snake:

    def __init__(self):
        self.cells: List[Vector2] = []
        self.dir: Direction = Direction.LEFT

    @property
    def head(self) -> Vector2:
        return self.cells[-1]

    @head.setter
    def head(self, head: Vector2) -> None:
        self.cells[-1] = head

    @property
    def tail(self) -> Vector2:
        return self.cells[0]

    @tail.setter
    def tail(self, tail: Vector2) -> None:
        self.cells[0] = tail

    def pop(self, index: int = -1):
        return self.cells.pop(index)

    def append(self, cell: Vector2):
        self.cells.append(cell)

    def __len__(self) -> int:
        return len(self.cells)

    def __getitem__(self, index: int) -> Vector2:
        return self.cells[index]

    def __iter__(self):
        for cell in self.cells:
            yield cell


def gen_apple():
    if len(snake) == ROWS*COLS:
        return None

    new_apple = None
    while True:
        new_apple = Vector2(random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        for cell in snake.cells:
            if cell == new_apple:
                break
        else:
            break

    return new_apple


snake: Snake = Snake()
snake.append(Vector2(3, 1))
snake.append(Vector2(2, 1))
snake.append(Vector2(1, 1))


def main() -> int:
    set_trace_log_level(TraceLogLevel.WARNING)

    set_target_fps(60)
    init_window(800, 600, 'Hello from Python')

    apple = gen_apple()

    STEP_INTERVAL = 0.15
    time = 0
    move = False
    game_over = False
    pause = False


    def cell_step(a, b):
        c = a + b
        c.x %= COLS
        c.y %= ROWS
        return c


    while not window_should_close():
        begin_drawing()

        clear_background(BLACK)
        dt = get_frame_time()

        if game_over:
            pass
        else:
            if not pause:
                time += dt

            if time >= STEP_INTERVAL:
                move = True
                time = 0

            # draw board
            for y in range(ROWS):
                for x in range(COLS):
                    pos = Vector2(x, y) * CELL_SIZE
                    color = BLACK if (x + y) % 2 == 0 else WHITE
                    draw_rectangle_v(pos, CELL_SIZE, color)

            # draw apple
            if apple:
                pos = apple * CELL_SIZE
                draw_rectangle_v(pos, CELL_SIZE, RED)

            # draw snake
            for index in range(0, len(snake) - 1):
                prev_cell = snake[index - 1] if index > 0 else None
                cell = snake[index]
                next_cell = snake[index + 1]

                pos = cell * CELL_SIZE
                draw_rectangle_v(pos, CELL_SIZE, GREEN)

                pos = (cell * CELL_SIZE) + Vector2(5, 5)
                draw_rectangle_v(pos, CELL_SIZE - Vector2(10, 10), DARKGREEN)

                diff1 = cell - prev_cell if prev_cell else None
                diff2 = cell - next_cell
                for diff in [diff1, diff2]:
                    if diff == directions[Direction.RIGHT]:
                        pos = (cell * CELL_SIZE) + Vector2(0, 5)
                    elif diff == directions[Direction.LEFT]:
                        pos = (cell * CELL_SIZE) + Vector2(10, 5)
                    elif diff == directions[Direction.UP]:
                        pos = (cell * CELL_SIZE) + Vector2(5, 10)
                    elif diff == directions[Direction.DOWN]:
                        pos = (cell * CELL_SIZE) + Vector2(5, 0)

                    draw_rectangle_v(pos, CELL_SIZE - Vector2(10, 10), DARKGREEN)

            # draw boa head
            pos = snake.head * CELL_SIZE
            draw_rectangle_v(pos, CELL_SIZE, GREEN)

            if move:
                move = False
                if snake.head == apple:
                    apple = gen_apple()
                else:
                    snake.pop(0)
                new_head = snake.head + directions[snake.dir]
                new_head.x = new_head.x % COLS
                new_head.y = new_head.y % ROWS
                snake.append(new_head)

            if is_key_pressed(KeyboardKey.SPACE):
                pause = not pause

            if not pause:
                if is_key_pressed(KeyboardKey.W):
                    if snake.dir != Direction.DOWN:
                        snake.dir = Direction.UP
                elif is_key_pressed(KeyboardKey.D):
                    if snake.dir != Direction.LEFT:
                        snake.dir = Direction.RIGHT
                elif is_key_pressed(KeyboardKey.S):
                    if snake.dir != Direction.UP:
                        snake.dir = Direction.DOWN
                elif is_key_pressed(KeyboardKey.A):
                    if snake.dir != Direction.RIGHT:
                        snake.dir = Direction.LEFT

        end_drawing()


    close_window()

if __name__ == '__main__':
    main()
