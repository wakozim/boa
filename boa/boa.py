import random
import queue
from typing import List
from enum import IntEnum, auto
import math

from .raylib import *


FIELD_COLOR_FIRST  = Color(0x3B, 0x83, 0x1D, 0xFF)
FIELD_COLOR_SECOND = Color(0x2E, 0x65, 0x18, 0xFF)
FIELD_FRAME_COLOR  = Color(0x0, 0x0, 0x0, 0xff)
BACKGROUND_COLOR   = Color(0x20, 0x20, 0x20, 0xFF)


VELOCITY = Vector2(1, 1)
CELL_SIZE = Vector2(75, 75)
COLS = 15
ROWS = 10
FIELD_SIZE = CELL_SIZE * Vector2(COLS, ROWS)
FIELD_FRAME_SIZE = Vector2(30, 30)



class Direction(IntEnum):
    LEFT  = auto(0)
    DOWN  = auto()
    RIGHT = auto()
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
        self.dir: Direction = Direction.RIGHT
        self.hue = 40
        self.line_hue = 10

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

    def is_body(self, cell: Vector2) -> bool:
        for body_cell in self:
            if body_cell == cell:
                return True
        return False

    def update_colors(self, dt: float) -> None:
        self.hue = (self.hue + dt * 10) % 360
        self.line_hue = (self.line_hue + dt * 10) % 360

    @property
    def color(self) -> Color:
        return color_from_hsv(self.hue, 0.60, 0.75)

    @property
    def line_color(self) -> Color:
        #return self.color
        return color_from_hsv(self.line_hue, 0.60, 0.50)


class Particle:

    def __init__(self, pos: Vector2, color: Color) -> None:
        self.pos = pos
        self.velocity: Vector2 = Vector2(random.randint(-400, 400),
                                         random.randint(-400, 400))
        self.radius: float = 10 + random.random() * 15
        self.max_lifetime = random.random()
        self.lifetime = self.max_lifetime
        self.initial_color = color

    def __bool__(self) -> bool:
        return self.lifetime > 0.0

    @property
    def color(self) -> Color:
        alpha = self.max_lifetime / self.lifetime
        return color_alpha(self.initial_color, alpha)

    def update(self, dt: float) -> None:
        if self:
            self.lifetime -= dt
            self.pos += self.velocity * dt


class Game:

    STEP_INTERVAL = 0.125

    def __init__(self):
       self.reset_game()

    def reset_game(self):
        self.next_dirs = queue.Queue()

        self.snake = Snake()
        self.snake.append(Vector2(0, 0))
        self.snake.append(Vector2(1, 0))
        self.snake.append(Vector2(2, 0))

        self.game_over = False
        self.pause = False
        self.step_cooldown = 0
        self.score = 0

        self.apple = None
        self.new_apple()

        self.particles: List[Particle] = []

    def random_cell(self):
        cell = Vector2()
        cell.x = random.randint(0, COLS - 1)
        cell.y = random.randint(0, ROWS - 1)
        return cell

    def cell_step(self, a: Vector2, b: Vector2) -> Vector2:
        c: Vector2 = a + b
        c.x %= COLS
        c.y %= ROWS
        return c

    def cells_dir(self, a: Vector2, b: Vector2) -> Vector2:
        for direction, vector in directions.items():
            if self.cell_step(a, vector) == b:
                return direction

    def opposite_dir(self, direction: Direction) -> Direction:
        return (direction + 2) % len(directions)

    def new_apple(self):
        if len(self.snake) == ROWS*COLS:
            return None

        new_apple = None
        while True:
            new_apple = self.random_cell()
            if not self.snake.is_body(new_apple):
                break
        self.apple = new_apple

    def generate_particles(self):
        for cell in self.snake:
            for _ in range(10):
                pos = cell * CELL_SIZE
                self.particles.append(Particle(pos, self.snake.color))


def render_field(texture: RenderTexture) -> None:
    begin_texture_mode(texture)
    for y in range(ROWS):
        for x in range(COLS):
            pos = Vector2(x, y) * CELL_SIZE
            index = (x + y) % 2 == 0
            color = FIELD_COLOR_FIRST if index else FIELD_COLOR_SECOND
            draw_rectangle_v(pos, CELL_SIZE, color)
    end_texture_mode()


def render_snake(texture: RenderTexture, game: Game) -> None:
    begin_texture_mode(texture)

    t = game.step_cooldown / game.STEP_INTERVAL

    tail = game.snake.tail
    prev_cell = game.snake.cells[1] if len(game.snake) > 1 else None
    tail_dir = game.cells_dir(tail, prev_cell) if prev_cell else game.snake.dir
    tail_len = (CELL_SIZE * directions[tail_dir]) * (1 - t)
    tail_size = CELL_SIZE - Vector2(math.fabs(tail_len.x), math.fabs(tail_len.y))
    pos = tail * CELL_SIZE
    if (tail_dir == Direction.RIGHT or tail_dir == Direction.DOWN):
        pos += tail_len

    draw_rectangle_v(pos, tail_size, game.snake.color)

    for index in range(1, len(game.snake) - 1):
        prev_cell = game.snake[index - 1] if index > 0 else None
        cell = game.snake[index]
        next_cell = game.snake[index + 1]

        pos = cell * CELL_SIZE
        draw_rectangle_v(pos, CELL_SIZE, game.snake.color)

        pos = cell*CELL_SIZE + CELL_SIZE/2

        size = Vector2(20, 20)

        dir1 = directions[game.cells_dir(prev_cell, cell)]
        start_pos = pos - (CELL_SIZE/2 * dir1)
        draw_line_ex(start_pos, pos, 25, game.snake.line_color)

        dir2 = game.cells_dir(cell, next_cell)
        draw_line_ex(pos, pos+(CELL_SIZE/2 * directions[dir2]), 25, game.snake.line_color)

    # draw boa head
    head = game.snake.head
    prev_cell = game.snake.cells[-2] if len(game.snake) > 1 else None
    head_dir = game.cells_dir(head, prev_cell) if prev_cell else game.opposite_dir(game.snake.dir)
    head_len = (CELL_SIZE * directions[head_dir]) * (t)
    head_size = CELL_SIZE - Vector2(math.fabs(head_len.x), math.fabs(head_len.y))
    pos = head * CELL_SIZE
    if (head_dir == Direction.RIGHT or head_dir == Direction.DOWN):
        pos += head_len

    draw_rectangle_v(pos, head_size, game.snake.color)

    end_texture_mode


def render_particles(game: Game, dt: float) -> None:
    for particle in game.particles:
        particle.update(dt)
        if particle:
            draw_circle_v(particle.pos, particle.radius, particle.color)


def update_game(game: Game, dt: int) -> None:
    if is_key_pressed(KeyboardKey.SPACE):
        game.pause = not game.pause
    elif is_key_pressed(KeyboardKey.R):
        game.reset_game()
        return None

    if game.pause:
        return None

    game.snake.update_colors(dt)

    if not game.game_over:

        if is_key_pressed(KeyboardKey.W):
            game.next_dirs.put(Direction.UP)
        elif is_key_pressed(KeyboardKey.D):
            game.next_dirs.put(Direction.RIGHT)
        elif is_key_pressed(KeyboardKey.S):
            game.next_dirs.put(Direction.DOWN)
        elif is_key_pressed(KeyboardKey.A):
            game.next_dirs.put(Direction.LEFT)

        game.step_cooldown -= dt

        if game.step_cooldown <= 0.0:
            game.step_cooldown = game.STEP_INTERVAL

            if not game.next_dirs.empty():
                next_dir = game.next_dirs.get(block=False)
                if game.snake.dir != game.opposite_dir(next_dir):
                    game.snake.dir = next_dir

            snake_step = directions[game.snake.dir]
            new_head = game.cell_step(game.snake.head, snake_step)

            if game.snake.head == game.apple:
                game.snake.append(new_head)
                game.new_apple()
                game.score += 1
            elif game.snake.is_body(new_head):
                game.generate_particles()
                game.game_over = True
            else:
                game.snake.append(new_head)
                game.snake.pop(0)


def main() -> int:
    set_trace_log_level(TraceLogLevel.WARNING)

    set_target_fps(60)
    init_window(FIELD_SIZE.x, FIELD_SIZE.y, 'Boa')

    game_over = False

    screen: RenderTexture = load_render_texture(
            COLS*CELL_SIZE.x,
            ROWS*CELL_SIZE.y
    )
    set_texture_filter(screen.texture, TextureFilter.BILINEAR)

    game = Game()

    while not window_should_close():
        begin_drawing()

        screen_size = Vector2(get_screen_width(), get_screen_height())

        clear_background(BACKGROUND_COLOR)
        dt = get_frame_time()

        render_field(screen)
        begin_texture_mode(screen)

        # draw apple
        if game.apple is not None:
            pos = game.apple * CELL_SIZE
            draw_rectangle_v(pos, CELL_SIZE, RED)

        if game.game_over:
            render_particles(game, dt)
            font_size = 50
            text_width = measure_text("Game Over", font_size)
            draw_text("Game Over", screen_size.x/2 - text_width/2, screen_size.y/2 - font_size/2, font_size, RED)
        else:
            render_snake(screen, game)
            font_size = 40
            text_width = measure_text(f"Score: {game.score}", font_size)
            draw_text(f"Score: {game.score}", 30, 30, font_size, BLACK)


        end_texture_mode()

        field_pos = (screen_size * 0.5) - (FIELD_SIZE * 0.5)

        draw_rectangle_v(
                field_pos - FIELD_FRAME_SIZE * 0.5,
                FIELD_SIZE + FIELD_FRAME_SIZE,
                FIELD_FRAME_COLOR
        )
        draw_texture_pro(
                screen.texture,
                Rectangle(0,
                          0,
                          screen.texture.width,
                          -screen.texture.height),
                Rectangle(field_pos.x,
                          field_pos.y,
                          screen.texture.width,
                          screen.texture.height),
                Vector2(0, 0),
                0,
                WHITE
        )

        update_game(game, dt)

        end_drawing()

    close_window()


if __name__ == '__main__':
    main()
