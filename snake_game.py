import curses
import random
import time

# Dimensions of the game board
HEIGHT = 20
WIDTH = 40

# Time per game loop iteration in seconds
TICK = 0.1
FLASH_DURATION = 10  # seconds of flashing when apple is eaten

DIRECTIONS = {
    curses.KEY_UP: (-1, 0),
    curses.KEY_DOWN: (1, 0),
    curses.KEY_LEFT: (0, -1),
    curses.KEY_RIGHT: (0, 1),
}

COLORS = [
    curses.COLOR_RED,
    curses.COLOR_GREEN,
    curses.COLOR_BLUE,
    curses.COLOR_MAGENTA,
    curses.COLOR_CYAN,
    curses.COLOR_YELLOW,
    curses.COLOR_WHITE,
]


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(int(TICK * 1000))
    curses.start_color()

    # Create color pairs
    for idx, c in enumerate(COLORS, start=1):
        curses.init_pair(idx, c, curses.COLOR_BLACK)

    # Initial snake and apple
    snake = [(HEIGHT // 2, WIDTH // 2 + i) for i in range(3)]
    direction = DIRECTIONS[curses.KEY_LEFT]
    apple = place_apple(snake)
    flash_counter = 0

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        if key in DIRECTIONS:
            new_dir = DIRECTIONS[key]
            # Prevent the snake from reversing
            if (new_dir[0] != -direction[0] or new_dir[1] != -direction[1]):
                direction = new_dir

        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Check collisions
        if (
            new_head[0] < 0 or new_head[0] >= HEIGHT or
            new_head[1] < 0 or new_head[1] >= WIDTH or
            new_head in snake
        ):
            break  # Game over

        snake.insert(0, new_head)

        if new_head == apple:
            apple = place_apple(snake)
            flash_counter = int(FLASH_DURATION / TICK)
        else:
            snake.pop()

        draw_board(stdscr, snake, apple, flash_counter)
        if flash_counter > 0:
            flash_counter -= 1
        time.sleep(TICK)

    stdscr.nodelay(False)
    stdscr.addstr(HEIGHT // 2, WIDTH // 2 - 5, "GAME OVER")
    stdscr.getch()


def place_apple(snake):
    positions = [(y, x) for y in range(HEIGHT) for x in range(WIDTH) if (y, x) not in snake]
    return random.choice(positions)


def draw_board(stdscr, snake, apple, flash_counter):
    stdscr.clear()

    # Draw border
    for x in range(WIDTH + 2):
        stdscr.addch(0, x, '#')
        stdscr.addch(HEIGHT + 1, x, '#')
    for y in range(1, HEIGHT + 1):
        stdscr.addch(y, 0, '#')
        stdscr.addch(y, WIDTH + 1, '#')

    # Draw apple
    stdscr.addch(apple[0] + 1, apple[1] + 1, '@')

    # Determine color pair
    color_pair = 0
    if flash_counter > 0:
        idx = flash_counter % len(COLORS)
        color_pair = curses.color_pair(idx + 1)
    else:
        color_pair = curses.color_pair(1)

    for y, x in snake:
        stdscr.addch(y + 1, x + 1, 'O', color_pair)

    stdscr.refresh()


if __name__ == '__main__':
    curses.wrapper(main)
