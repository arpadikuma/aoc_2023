from math import lcm
import os
import sys

file_path = './08.txt'

if sys.argv and len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    if os.path.exists(file_path):
        file_path = file_path
    else:
        file_path = input('enter the navigation file: ')

LR_MAP = { 'R':1, 'L':0 }

def parse_map(text):
    map_dict = {}
    directions, map_data = text.split("\n\n")

    for map_step in map_data.split("\n"):
        map_loc, next_locs = map_step.split(" = ")
        next_locs = next_locs[1:-1].split(", ")
        map_dict[map_loc] = next_locs

    return directions, map_dict
    

def navigate_locs(current, goal, directions, map_dict, mode='hooman'):
    counter = 0
    direction_idx = 0
    loop_count = 0
    loop_dict = {}
    loop_current = current
    
    def update_map(map_curr, goal, nav_count, dir_index, directions, map_dict):
        map_curr = map_dict[map_curr][LR_MAP[directions[dir_index]]]
        if dir_index < len(directions) - 1:
            dir_index += 1
        else:
            dir_index = 0
        nav_count += 1
        return nav_count, map_curr, dir_index
    
    if mode == 'hooman':
        while current != goal:
            counter, current, direction_idx = update_map(current, goal, counter, direction_idx, directions, map_dict)
        return counter, current
    elif mode == 'ghost':
        while loop_count < 5:
            while loop_current[-1] != goal:
                counter, loop_current, direction_idx = update_map(loop_current, goal, counter, direction_idx, directions, map_dict)
            loop_count += 1
            loop_dict[current + f' #{loop_count}'] = counter  
    
        return counter, loop_current, loop_dict


def calc_total_steps(loops):
    waypoints_list = []
    for x in loops:
        waypoints_list.extend(set(x.values()))

    total_steps = lcm(*waypoints_list)
    return total_steps


def calc_navigation_path(start, end, directions, map_dict, mode='hooman'):
    if mode == 'hooman':
        counter = 0
        direction_idx = 0
        counter, start = navigate_locs(start, end, directions, map_dict, mode=mode)

        return counter

    elif mode == 'ghost':
        start_positions = [x for x in map_dict.keys() if x[-1] == start]
        loop_list = []
        for start in start_positions:
            counter = 0
            direction_idx = 0
            counter, start, loop_dict = navigate_locs(start, end, directions, map_dict, mode=mode)
            loop_list.append(loop_dict)
        total_steps = calc_total_steps(loop_list)
        return total_steps

def main():
    with open(file_path) as f:
        text = f.read()
        directions, map_dict = parse_map(text)

        # human mode
        map_loc = 'AAA'
        end_loc = 'ZZZ'
        steps = calc_navigation_path(map_loc, end_loc, directions, map_dict)

        # ghost mode 
        start_letter = 'A'
        goal_letter = 'Z'
        total_steps = calc_navigation_path(start_letter, goal_letter, directions, map_dict, mode='ghost')

        return steps, total_steps

if __name__ == "__main__":
    steps, total_steps = main()

    print(f"total steps required to reach ZZZ: {steps}")    
    print(f"total steps for all paths to converge on Z simultaneously: {total_steps}")
