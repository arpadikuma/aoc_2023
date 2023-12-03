import os
import sys

file_path = './03.txt'
mode = 'gears'

if sys.argv and len(sys.argv) > 1:
    file_path = sys.argv[1]
    if len(sys.argv) > 2:
        mode = sys.argv[2]
else:
    if os.path.exists(file_path):
        file_path = file_path
    else:
        file_path = input('enter the relative path & filename to the engine schematic file: ')
        while mode not in ["gears", "parts"]:
            mode = input('enter the mode: "gears" or "parts": ').lower()
        else:
            print('Invalid input, defaulting to "gears"')
            mode = "gears"

part_number_dict = {}

def find_part(row, line, rows):
    idx_list = []
    for n, char in enumerate(row):
        if not char.isdigit() and char!='.':
            idx_data = create_index_list(n, line, rows)
            idx_list.extend(idx_data)

    return idx_list


def create_index_list(idx, line, rows):
    num_rows = len(rows)
    num_cols = len(rows[0])
    char = rows[line][idx]

    # create list of tuples of indices to check
    index_list = []
    
    if 0 <= line <= num_rows and 0 <= idx <= num_cols:
        if idx > 0:
            index_list.append((int(line), int(idx)-1, (line, idx, char)))
        if idx < num_cols - 1:
            index_list.append((int(line), int(idx)+1, (line, idx, char)))
        if line > 0:
            index_list.append((int(line)-1, int(idx), (line, idx, char)))
        if line < num_rows - 1:
            index_list.append((int(line)+1, int(idx), (line, idx, char)))
        if line > 0 and idx > 0:
            index_list.append((int(line)-1, int(idx)-1, (line, idx, char)))
        if line > 0 and idx < num_cols - 1:
            index_list.append((int(line)-1, int(idx)+1, (line, idx, char)))
        if line < num_rows - 1 and idx > 0:
            index_list.append((int(line)+1, int(idx)-1, (line, idx, char)))
        if line < num_rows - 1 and idx < num_cols - 1:
            index_list.append((int(line)+1, int(idx)+1, (line, idx, char)))

    return index_list


def full_part_number(row, col, char_info, rows):
    if 0 <= col <= len(rows[row]):
        start_idx = col
        end_idx = col

    while start_idx > 0 and rows[row][start_idx-1].isdigit():
        start_idx -= 1
    while end_idx < len(rows[row])-1 and rows[row][end_idx+1].isdigit():
        end_idx += 1

    return rows[row][start_idx:end_idx+1], start_idx, char_info


def check_dict_for_gears(dict):
    gear_ratio_dict = {}
    for k, v in dict.items():
        if len(v) == 2:
            gear_ratio_dict[k] = int(v[0][0]) * int(v[1][0])

    return gear_ratio_dict


def get_part_numbers(idx_list, rows, mode, dict=part_number_dict):
    for row_col in idx_list:
        char = rows[row_col[0]][row_col[1]]
        if char.isdigit():
            part_number, start_idx, char_info = full_part_number(row_col[0], row_col[1], row_col[2], rows)

            if mode == "parts":
                if str(row_col[0])+"."+str(start_idx) in dict:
                    pass
                else:
                    dict[str(row_col[0])+"."+str(start_idx)] = int(part_number)
            elif mode == "gears":
                if char_info in dict and type(dict[char_info]) == list:
                    if (part_number, start_idx) in dict[char_info]:
                        pass
                    else:
                        dict[char_info].append((part_number, start_idx))
                else:
                    dict[char_info] = [(part_number, start_idx)]

    return dict

def main():
    with open(file_path) as f:
        text = f.read()
        rows = text.split('\n')
        max_line = len(rows)
        max_char = len(rows[0])
        for n, row in enumerate(rows):
            # print(f"row #{n}")
            idx_list = find_part(row, n, rows)
            # print(n, idx_list)
            if idx_list is not None:
                full_dict = get_part_numbers(idx_list, rows, mode)
        if mode == "parts":
            # print(full_dict)
            return sum(full_dict.values())
        elif mode == "gears":
            ratio_dict = check_dict_for_gears(full_dict)
            return sum(ratio_dict.values())


if __name__ == "__main__":
    print (main())
