import os
import sys
import time

file_path = './05.txt'

if sys.argv and len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    if os.path.exists(file_path):
        file_path = file_path
    else:
        file_path = input('enter the relative path & filename to the pile of colorful cards: ')

def split_and_dict(text):
    str_list = text.strip().split("\n\n")

    if len(str_list) < 4:
        print("Invalid input format.")
        return None
    
    seed_list = str_list[0].strip().split(": ")[1].split(" ")
    seed_list = [int(x) for x in seed_list]

    full_map = {}

    for maps_str in str_list[1:]:
        try:
            map_name, map_data = maps_str.strip().split(":\n")
            # print(map_name, map_data)
            # print(maps_str.strip().split(":\n"))
            full_map[map_name] = create_map_dict(map_data)
        except Exception as e:
            print(f"Error processing map: {map_name}")
            print(f"Error details: {e}")
            
    return seed_list, full_map


def create_map_dict(maps_str):
    map_dict = {'destination': [], 'source': []}
    maps_list = maps_str.strip().split("\n")

    for maps in maps_list:
        map_list = maps.strip().split(' ')
        # print(map_list)
        dest_map = [(int(map_list[0]), int(map_list[2]))]
        src_map = [(int(map_list[1]), int(map_list[2]))]
        # dest_map = [i for i in range(int(map_list[0]), int(map_list[0])+int(map_list[2]))]
        # src_map = [i for i in range(int(map_list[1]), int(map_list[1])+int(map_list[2]))]

        map_dict['destination'].extend(dest_map)
        map_dict['source'].extend(src_map)
    return(map_dict)


def map_soil(seed, full_dict, reversed):
    item_list = [seed]

    mapping_keys = full_dict.keys()
    if reversed == True:
        mapping_keys = [mapping_key for mapping_key in full_dict.keys()][::-1]

    for mapping_key in mapping_keys:
        item_list.append(find_mapping(item_list[-1], mapping_key, full_dict, reversed))

    return item_list[-1]


def find_mapping(item_no, mapping_key, full_dict, reversed):
    src_key = 'source'
    dest_key = 'destination'

    if reversed == True:
        (src_key, dest_key) = (dest_key, src_key)
    
    map_ranges = [[x, x+y] for x, y in full_dict[mapping_key][src_key]]
    for n, idx_range in enumerate(map_ranges):
        if idx_range[0] <= item_no < idx_range[1]:
            item_diff = item_no-idx_range[0]

            next_item = full_dict[mapping_key][dest_key][n][0]+item_diff

            return next_item
    else:
        next_item = item_no

        return next_item


def closest_location(seed_list, full_dict):
    location_list = []

    for seed in seed_list:
        location_list.append(map_soil(seed, full_dict, reversed=False))

    return min(location_list)


def closest_batch_location(seed_list, full_dict, max_location=999999999):
    location_list = []
    
    seed_list_len = len(seed_list)
    c = 0
    seed_ranges = []
    while c < seed_list_len:
        if c%2==0:
            seed_ranges.append((seed_list[c], seed_list[c]+seed_list[c+1]))
        c+=1
    # print(seed_ranges)    ###
    location_list = list(range(0, max_location))

    for location in location_list:
        seed_num = map_soil(location, full_dict, reversed=True)
        for seed_range in seed_ranges:
            if seed_range[0] <= seed_num < seed_range[1]:
                return seed_num, location


def main():
    with open(file_path) as f:
        text = f.read()
        seed_list, full_map = split_and_dict(text)

        time_0 = time.time()
        closest_loc = closest_location(seed_list, full_map)
        time_1 = time.time() - time_0
        print(f"The closest location in part 1 is: {closest_loc}\ntime taken: {time_1} ms")

        time_2 = time.time()
        best_seed, best_loc = closest_batch_location(seed_list, full_map)
        time_3 = time.time() - time_2
        print(f"The closest location for the seed batches in part 2 is: {best_loc}\ntime taken: {time_3} ms")

if __name__ == "__main__":
    main()

