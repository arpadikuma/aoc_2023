import os
import sys
import time

file_path = './06.txt'

if sys.argv and len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    if os.path.exists(file_path):
        file_path = file_path
    else:
        file_path = input('enter the relative path & filename to the time and distance sheet: ')


def make_lists(text):
    lines = text.split("\n")
    times_list = [int(x) for x in lines[0].split(':')[1].strip().split(" ") if x.isdigit()]
    distances_list = [int(y) for y in lines[1].split(':')[1].strip().split(" ") if y.isdigit()]

    return times_list, distances_list


def count_races(times_list, dist_list):
    counters = []
    for n, race_time in enumerate(times_list):
        counter = 0
        for x in list(range(race_time)):
            dist = x * (race_time - x)
            if dist > dist_list[n]:
                counter += 1
        counters.append(counter)
    return counters


def convert_lists(times_list, dist_list):
    total_time = int(''.join([str(x) for x in times_list]))
    total_dist = int(''.join([str(x) for x in dist_list]))

    return total_time, total_dist


def main():
    with open(file_path, 'r') as f:
        text = f.read()

        times_list, distances_list = make_lists(text)

        # part 1
        counters = count_races(times_list, distances_list)
        sum = 1
        for count in counters:
            sum *= count
        print(f"sum of ways to win: {sum}")

        # part 2
        total_time, total_dist = convert_lists(times_list, distances_list)
        big_count = count_races([total_time], [total_dist])[0]
        print(f"total number of ways to win the long race: {big_count}")

if __name__ == "__main__":
    main()
