import numpy as np
import os
import sys

file_path = './09.txt'

if sys.argv and len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    if os.path.exists(file_path):
        file_path = file_path
    else:
        file_path = input('enter the OASIS report file: ')


def find_diff(input_data):
    diff = np.diff(np.array(input_data))
    diff_hist = {0:np.array(input_data), 1: diff}
    count = 1
    while not np.all(diff == 0):
        diff = np.diff(diff)
        count += 1
        diff_hist[count] = diff
    return diff, count, diff_hist


def extrapolate_missing(diff_hist, mode='last'):
    keys = [key for key in diff_hist.keys()][::-1]
    diff = 0
    if mode == 'last':
        for key in keys:
            # correct value, but negative... not sure yet why:
            # diff = np.diff(np.array([diff_hist[key][-1], diff]))[0] 
            
            if diff == 0 and np.diff(diff_hist[key][-2:])[0] == 0:
                diff = diff_hist[key][-1]
            else:
                diff += np.diff(diff_hist[key][-2:])[-1]
            if key == 0:
                diff += diff_hist[key][-1]

    elif mode == 'first':
        for key in keys:
            diff = np.diff(np.array([diff, np.flip(diff_hist[key])[-1]]))[-1]

    return diff


def main(mode='first'):
    with open(file_path) as f:
        text = f.read()
        histories = text.split("\n")
    
        extrapolated_sum = 0
        for history in histories:
            data = [int(val) for val in history.split(" ")]
            diff, count, diffhist = find_diff(data)
            extrapolated_val = extrapolate_missing(diffhist, mode=mode)
            extrapolated_sum += extrapolated_val
        return extrapolated_sum

if __name__ == "__main__":
    print(f"sum of the extrapolated last values: {main('last')}")
    print(f"sum of the backwards extrapolated values: {main('first')}")
