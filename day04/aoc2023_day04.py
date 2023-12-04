import os
import sys

file_path = './04.txt'

if sys.argv and len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    if os.path.exists(file_path):
        file_path = file_path
    else:
        file_path = input('enter the relative path & filename to the pile of colorful cards: ')

def splitting_card(card):
    card_no, card_numbers_list = card.split(":")
    card_no = int(card_no.replace(' ','')[4:])
    winning_numbers_str, having_numbers_str = card_numbers_list.strip().replace('  ', ' ').split("|")
    winning_numbers = winning_numbers_str.strip().split(" ")
    winning_numbers = [int(win_num) for win_num in winning_numbers]
    having_numbers = having_numbers_str.strip().split(" ")
    having_numbers = [int(have_num) for have_num in having_numbers]
    return card_no, winning_numbers, having_numbers


def check_wins(wins, haves):
    matches = 0
    for number in wins:
        if number in haves:
            matches += 1
    points = 2**(matches-1) if matches > 0 else 0
    return matches, points


def copies_count(cards, copies_dict):
    for i, card in enumerate(cards):
        card_no, wins, haves = splitting_card(card)
        # print(card)
        # print(f"check_wins({wins}, {haves})")
        matches, points = check_wins(wins, haves)
        # print(f"{matches} m with {points} p")
        modifier = copies_dict[card_no]
        # print(modifier)
        if points > 0:
            for j in range(1, matches+1):
                if j in copies_dict:
                    # print(f'increasing dict {j} by 1')
                    copies_dict[card_no+j] += 1*modifier
                else:
                    print(f'creating dict {j}')
                    copies_dict[card_no+j] = 1*modifier
    return copies_dict


def main():
    with open(file_path) as f:
        all_cards = f.read().split("\n")
        point_sum = 0
        card_list = []
        card_dict = {}
        copies_dict = {x+1:1 for x in range(len(all_cards))}
        # copies_dict = {}
        for card in all_cards:
            card_no, winning_list, having_list = splitting_card(card)
            # card_dict[card_no] = 
            card_list.append([card_no, winning_list, having_list])
            # print(card_no)
            matches, points = check_wins(winning_list, having_list)
            # print(f"{matches} wins with {points} points")
            point_sum += points
        copies_dict = copies_count(all_cards, copies_dict)
    

    print(f"The total points are: {point_sum}")
    print(f"The total amount of cards is: {sum(copies_dict.values())}")


if __name__ == "__main__":
    main()

