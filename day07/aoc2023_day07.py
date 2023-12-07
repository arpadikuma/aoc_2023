import os
import sys
import time

file_path = './07.txt'

if sys.argv and len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    if os.path.exists(file_path):
        file_path = file_path
    else:
        file_path = input('enter the list of hands and bids: ')


card_order = ['23456789TJQKA']
card_order_new = ['J23456789TQKA']


def parse_card_info(card_info):
    hand, bid = card_info.split(" ")
    return hand, int(bid)

def evaluate_hand(card_bid):
    hand_info = {}
    for card in card_bid[0]:
        if card in hand_info.keys():
            hand_info[card] += 1
        else:
            hand_info[card] = 1
    return card_bid + (int("".join([str(x) for x in sorted(hand_info.values())])),)
    return hand_info


def eval_hand(hand):
    values = [card for card in hand[0]]

    if any(values.count(value) == 5 for value in set(values)):
        return 7
    elif any(values.count(value) == 4 for value in set(values)):
        return 6
    elif any(values.count(value) == 3 for value in set(values)) and any(values.count(value) == 2 for value in set(values)):
        return 5
    elif any(values.count(value) == 3 for value in set(values)):
        return 4
    # elif sum(values.count(value) == 2 for value in set(values)) == 2:
    elif len([1 for value in set(values) if values.count(value) == 2]) == 2:
        return 3
    elif any(values.count(value) == 2 for value in set(values)):
        return 2
    else:
        return 1


def eval_joker_hand(hand):
    values = [card for card in hand[0]]

    if any(values.count(value) == 5 for value in set(values)):
        hand_value = 7
    elif any(values.count(value) == 4 for value in set(values)):
        if values.count('J') in [1, 4]:
            hand_value = 7
        else:
            hand_value = 6
    elif any(values.count(value) == 3 for value in set(values)) and any(values.count(value) == 2 for value in set(values)):
        if values.count('J') in [2, 3]:
            hand_value = 7
        else:
            hand_value = 5
    elif any(values.count(value) == 3 for value in set(values)):
        if values.count('J') in [1, 3]:
            hand_value = 6
        else:
            hand_value = 4
    # elif sum(values.count(value) == 2 for value in set(values)) == 2:
    elif len([1 for value in set(values) if values.count(value) == 2]) == 2:
        if values.count('J') == 1:
            hand_value = 5
        elif values.count('J') == 2:
            hand_value = 6
        else:
            hand_value = 3
    elif any(values.count(value) == 2 for value in set(values)):
        if values.count('J') in [1, 2]:
            hand_value = 4
        else:
            hand_value = 2
    else:
        if values.count('J') == 1:
            hand_value = 2
        else:
            hand_value = 1
    # print(hand[0], hand_value)
    return hand_value


def group_hands(card_tuple):
    # string, bid, hand_type = card_tuple
    # return [hand_order.index(group) for group in hand_type], card_tuple
    pass

def main():
    with open(file_path, 'r') as f:
        text = f.read()
        card_list = []
        
        card_data = [row for row in text.split('\n') if len(row) > 6]
        for card_info in card_data:
            card_list.append(parse_card_info(card_info))
    return card_list

if __name__ == "__main__":
    card_list = main()

    # part 1
    cards_sorted = sorted(card_list, key=lambda x: (eval_hand(x), [card_order[0].index(card[0]) for card in x[0]]))
    scores = sum([(n+1)*card[1] for n, card in enumerate(cards_sorted)])

    print(f"total winnings without Joker: {scores}")
    # part 2
    cards_sorted = sorted(card_list, key=lambda x: (eval_joker_hand(x), [card_order_new[0].index(card[0]) for card in x[0]]))
    scores = sum([(n+1)*card[1] for n, card in enumerate(cards_sorted)])

    print(f"total winnings with Joker instead of Jack: {scores}")
