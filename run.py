import sys
import time
import curses


ALL_MAPS = []
CURRENT_LEVEL = 0


def parse_maps():
    global CURRENT_LEVEL, ALL_MAPS
    maps_file = open('maps', 'r')
    maps_file_contents = maps_file.read()
    # each map is 40x20
    # '*' is the wall
    # 'o' character is you
    current_map = {
        'you': (0, 0),
        'initial_you': (0, 0),
        'map': []
    }
    for y, line in enumerate(maps_file_contents.split('\n')):
        if y % 20 == 0 and len(current_map['map']) != 0:
            ALL_MAPS.append(current_map)
            current_map = {
                'you': (0, 0),
                'initial_you': (0, 0),
                'map': []
            }
        current_map['map'].append(line)
        for x, c in enumerate(line):
            if c == 'o':
                current_map['you'] = (x, y % 20)
                current_map['initial_you'] = (x, y % 20)


def clear_screen(win):
    win.clear()


def draw_screen(win):
    global CURRENT_LEVEL, ALL_MAPS
    clear_screen(win)
    for y, line in enumerate(ALL_MAPS[CURRENT_LEVEL]['map']):
        win.addstr(y, 0, line)
    win.addstr(len(ALL_MAPS[CURRENT_LEVEL]['map']), 0, f'Level {CURRENT_LEVEL + 1}')


def get_current_map_and_position():
    global CURRENT_LEVEL, ALL_MAPS
    current_map = ALL_MAPS[CURRENT_LEVEL]['map']
    current_pos = ALL_MAPS[CURRENT_LEVEL]['you']
    return current_map, current_pos


def get_initial_map_position():
    global CURRENT_LEVEL, ALL_MAPS
    initial_position = ALL_MAPS[CURRENT_LEVEL]['initial_you']
    return initial_position


def set_current_pos(pos_x, pos_y):
    global CURRENT_LEVEL, ALL_MAPS
    ALL_MAPS[CURRENT_LEVEL]['you'] = (pos_x, pos_y)


def replace_char(string, index, char):
    return string[:index] + char + string[index + 1:]


def go_up():
    current_map, current_pos = get_current_map_and_position()
    current_pos_x, current_pos_y = current_pos
    if current_pos_y > 0 and current_map[current_pos_y - 1][current_pos_x] != '*':
        current_map[current_pos_y] = replace_char(current_map[current_pos_y], current_pos_x, ' ')
        current_pos_y -= 1
        current_map[current_pos_y] = replace_char(current_map[current_pos_y], current_pos_x, 'o')
        set_current_pos(current_pos_x, current_pos_y)


def go_down():
    current_map, current_pos = get_current_map_and_position()
    current_pos_x, current_pos_y = current_pos
    if current_pos_y < 19 and current_map[current_pos_y + 1][current_pos_x] != '*':
        current_map[current_pos_y] = replace_char(current_map[current_pos_y], current_pos_x, ' ')
        current_pos_y += 1
        current_map[current_pos_y] = replace_char(current_map[current_pos_y], current_pos_x, 'o')
        set_current_pos(current_pos_x, current_pos_y)


def go_right():
    current_map, current_pos = get_current_map_and_position()
    current_pos_x, current_pos_y = current_pos
    if current_pos_x < 39 and current_map[current_pos_y][current_pos_x + 1] != '*':
        current_map[current_pos_y] = replace_char(current_map[current_pos_y], current_pos_x, ' ')
        current_pos_x += 1
        current_map[current_pos_y] = replace_char(current_map[current_pos_y], current_pos_x, 'o')
        set_current_pos(current_pos_x, current_pos_y)


def go_left():
    current_map, current_pos = get_current_map_and_position()
    current_pos_x, current_pos_y = current_pos
    if current_pos_x > 0 and current_map[current_pos_y][current_pos_x - 1] != '*':
        current_map[current_pos_y] = replace_char(current_map[current_pos_y], current_pos_x, ' ')
        current_pos_x -= 1
        current_map[current_pos_y] = replace_char(current_map[current_pos_y], current_pos_x, 'o')
        set_current_pos(current_pos_x, current_pos_y)


def check_if_level_finished():
    global CURRENT_LEVEL, ALL_MAPS
    _, current_position = get_current_map_and_position()
    initial_position = get_initial_map_position()

    current_pos_x, current_pos_y = current_position
    initial_pos_x, initial_pos_y = initial_position

    if current_pos_x in [0, 39] or current_pos_y in [0, 19]:
        if current_pos_x != initial_pos_x and current_pos_y != initial_pos_y:
            # next level!
            # ALL_MAPS
            CURRENT_LEVEL += 1
            if CURRENT_LEVEL >= len(ALL_MAPS):
                sys.exit()
            set_current_pos(*get_initial_map_position())


def run_loop(win):
    win.nodelay(1)
    while True:
        draw_screen(win)
        char = win.getch()
        win.addstr(str(char))
        if char == curses.KEY_UP:
            go_up()
            check_if_level_finished()
        if char == curses.KEY_DOWN:
            go_down()
            check_if_level_finished()
        if char == curses.KEY_RIGHT:
            go_right()
            check_if_level_finished()
        if char == curses.KEY_LEFT:
            go_left()
            check_if_level_finished()
        time.sleep(0.1)


def main(win):
    parse_maps()
    run_loop(win)


if __name__ == '__main__':
    curses.wrapper(main)
