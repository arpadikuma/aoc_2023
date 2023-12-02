import os
import sys

file_path = './02.txt'
mode = 'power'

if sys.argv and len(sys.argv) > 1:
    file_path = sys.argv[1]
    if len(sys.argv) > 2:
        mode = sys.argv[2]
else:
    if os.path.exists(file_path):
        file_path = file_path
    else:
        file_path = input('enter the relative path & filename to the encrypted calibration values file: ')
        while mode not in ["power", "compare"]:
            mode = input('enter the mode: "power" or "compare": ').lower()
        else:
            print('Invalid input, defaulting to "power"')
            mode = "power"

comparison_dict = {
    'red': 12,
    'green': 13,
    'blue': 14
}

def compare_row(row, dict=comparison_dict, mode='compare'):
    game_id = row.split(":")[0].split(" ")[1]
    draws_list = row.split(":")[1].split(";")
    color_dict = {
        'red': [],
        'green': [],
        'blue': []
    }
    for draw in draws_list:
        cubes = draw.split(",")
        for cube_color in cubes:
            color_num, color = cube_color.strip().split(" ")
            color_dict[color].append(int(color_num))
    if mode == 'compare':
        score = 0
        for key, value in dict.items():
            if value >= max(color_dict[key]):
                score += 1
        if score == 3:
            return int(game_id)
        else:
            return 0
    elif mode == 'power':
        v_power = 1
        for values in color_dict.values():
            v_power *= max(values)
        return v_power

def parse_game_rows(filepath, mode):
    with open(filepath) as f:
        games = f.read()
        # for row in rows:
        #     print(row.split(":")[0][-1])
        rows = games.split('\n')
        rows_list = []
        for row in rows:
            row = row.replace("\n", "")
            # print(compare_row(row))
            rows_list.append(compare_row(row, mode=mode))
    return rows_list

if __name__ == "__main__":
    print(sum(parse_game_rows(file_path, mode)))
