from itertools import combinations
import os
import sys

file_path = './11.txt'
multipliers = [2, 1000000]

if sys.argv and len(sys.argv) > 1:
    file_path = sys.argv[1]
    if len(sys.argv) > 2:
        multipliers.append(int(sys.argv[2]))
else:
    if os.path.exists(file_path):
        file_path = file_path
    else:
        file_path = input('enter the galaxy chart: ')


def turn_cw(map_data):
    return list(map(list, zip(*list(reversed(map_data)))))


# def turn_ccw(map_data):
#     return list(reversed(list(map(list, zip(*map_data)))))


def count_pairs(flat_map):
    sum_galaxies = flat_map.count('#')
    pair_count = sum(list(range(sum_galaxies)))

    return sum_galaxies, pair_count


def flatten_map(map_data):
    flat_map = "".join(["".join(row) for row in map_data])

    return flat_map


# def unflatten(flat_map_data):
#     unflattened_map = [list(x) for x in flat_map_data.split(" ")]

#     return unflattened_map


def find_empty_rows(map_data):
    insertion_dict = {
        'rows': [],
        'cols': []
    }
    for i, map_file in enumerate([map_data, turn_cw(map_data)]):
        insert_list = []
        # display(map_file)
        for n, row in enumerate(map_file):
            if len(set(row)) == 1:
                insert_list.append(n)
                insertion_dict[list(insertion_dict.keys())[i]].append(n)
    return insertion_dict


def calc_dist(empty_rows, multiplier, *xy):
    x, y = xy

    row_mult = 0
    col_mult = 0
    for i in empty_rows['rows']:
        if y[0] > x[0]:
            if i in range(x[0], y[0]):
                row_mult += 1
        else:
            if i in range(y[0], x[0]):
                row_mult += 1
    for i in empty_rows['cols']:
        if y[1] > x[1]:
            if i in range(x[1], y[1]):
                col_mult +=1
        else:
            if i in range(y[1], x[1]):
                col_mult +=1

    if col_mult > 0:
        col_mult = multiplier*col_mult - col_mult
    if row_mult > 0:
        row_mult = multiplier*row_mult - row_mult
    
    zy = abs(y[0] - x[0]) + row_mult
    zx = abs(y[1] - x[1]) + col_mult

    return zy, zx


def calc_galaxy_positions(map_data, char='#'):
    n = len(map_data)
    m = len(map_data[0])
    galaxies, pairs = count_pairs(flatten_map(map_data))
    galaxy_positions = [idx for idx, x in enumerate(flatten_map(map_data)) if x == char]
    positions_2d = []
    for pos in galaxy_positions:
        positions_2d.append((pos//m, pos%m))

    return positions_2d


def main():
    with open(file_path, 'r') as f:
        galaxy_map = [[x.strip() for x in row.strip()] for row in f.readlines()]
    
        empty_rows = find_empty_rows(galaxy_map)
        galaxy_pairings = list(combinations(calc_galaxy_positions(galaxy_map), 2))
        result_dict = {}
        for multiplier in multipliers:
            sum_distances = sum([sum(x) for x in list(map(lambda pairing, e_rows=empty_rows, multi_x=multiplier: calc_dist(e_rows, multi_x, *pairing), galaxy_pairings))])
            result_dict[multiplier] = sum_distances
        return result_dict
    
if __name__ == "__main__":
    results = main()
    for k, v in results.items():
        print(f"Sum of distances for expansion rate {k}: {v}")
