from math import lcm
import os
import sys

file_path = './10.txt'

if sys.argv and len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    if os.path.exists(file_path):
        file_path = file_path
    else:
        file_path = input('enter the pipe schematic: ')


neighbor_tiles = {
    'top': ('7', '|', 'F', None),
    'bottom': ('J', None, 'L', '|'),
    'left': ('-', 'L', None, 'F'),
    'right': (None, 'J', '-', '7')
}

dir_idx = ['left', 'top', 'right', 'bottom']


def get_next_tile(n, m, direction, pipe_map, c=0):
    tile = None
    if direction == 'left':
        if m > 0:
            m = m-1
            tile = pipe_map[n][m]
    elif direction == 'right':
        if m < len(pipe_map[n])-1:
            m = m+1
            tile = pipe_map[n][m]
    elif direction == 'top':
        if n > 0:
            n = n-1
            tile = pipe_map[n][m]
    elif direction == 'bottom':
        if n < len(pipe_map)-1:
            n = n+1
            tile = pipe_map[n][m]

    if tile == 'S':
        return tile, 'stop', n, m, c+1
    elif tile in neighbor_tiles[direction]:
        return tile, direction, n, m, c+1
    else:
        return None, direction, n, m, c+1


def which_way(tile, direction):
    if tile in neighbor_tiles[direction]:
        # print(f'next tile: {tile} - next direction: {dir_idx[neighbor_tiles[direction].index(tile)]}')
        return dir_idx[neighbor_tiles[direction].index(tile)]


def start_search(n, m, pipe_map):
    tile_list = [(n, m)]
    if pipe_map[n][m-1] in neighbor_tiles['left']:
        tile = pipe_map[n][m-1]
        direction = 'left'
        print('starting search left')
        c = 0
        m = m-1
        while tile != None:
            direction = which_way(tile, direction)
            tile_list.append((n, m))
            tile, direction, n, m, c = get_next_tile(n, m, direction, pipe_map, c)
            if tile == 'S':
                return c, tile_list

    if pipe_map[n][m+1] in neighbor_tiles['right']:
        tile = pipe_map[n][m+1]
        direction = 'right'
        print('starting search right')
        c = 0
        m = m+1
        while tile != None:
            direction = which_way(tile, direction)
            tile_list.append((n, m))
            # print(n, m+1, direction, c)
            tile, direction, n, m, c = get_next_tile(n, m, direction, pipe_map, c)
            if tile == 'S':
                return c, tile_list

    if pipe_map[n-1][m] in neighbor_tiles['top']:
        tile = pipe_map[n-1][m]
        direction = 'top'
        print('starting search up')
        c = 0
        n = n-1
        while tile != None:
            direction = which_way(tile, direction)
            tile_list.append((n, m))
            tile, direction, n, m, c = get_next_tile(n, m, direction, pipe_map, c)
            if tile == 'S':
                return c, tile_list

    if pipe_map[n+1][m] in neighbor_tiles['bottom']:
        tile = pipe_map[n+1][m]
        direction = 'bottom'
        print('starting search bottom')
        c = 0
        n = n+1
        while tile != None:
            direction = which_way(tile, direction)
            tile_list.append((n, m))
            tile, direction, n, m, c = get_next_tile(n, m, direction, pipe_map, c)
            if tile == 'S':
                return c, tile_list


def shoelace_pick(tile_list):
    # shoelace formula for area
    tile_list = list(reversed(tile_list))
    coord_list = []
    for n, m in enumerate(tile_list):
        y = m[0]
        x = m[1]
        if n == len(tile_list)-1:
            yn = tile_list[0][0]
            xn = tile_list[0][1]
        else:
            yn = tile_list[n+1][0]
            xn = tile_list[n+1][1]
        calculation = (xn + x) * (yn - y)
        coord_list.append(calculation)

    # pick's theorem
    area = (abs(sum(coord_list)))//2

    enclosed = area - len(tile_list)/2 + 1
    return enclosed

def main_10():
    with open(file_path, 'r') as f:
        pipe_map = [[x.strip() for x in row.strip()] for row in f.readlines()]
        for n, row in enumerate(pipe_map):
            for m, tile in enumerate(row):
                if tile == 'S':
                    c, tile_list = start_search(n, m, pipe_map)
                    return c, tile_list

if __name__ == "__main__":
    c, tile_list = main_10()
    print(f'reached the start point after {c+1} steps;\nhalfway point is {(c+1)//2}!')
    enclosed_area = shoelace_pick(tile_list)
    print(f"The enclosed area size is {int(enclosed_area)}!")
