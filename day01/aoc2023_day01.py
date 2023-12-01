import sys

if sys.argv and len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    file_path = input('enter the relative path & filename to the encrypted calibration values file: ')

number_dict = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

def extract_num(text, dict=number_dict, reverse=False):
    if reverse == True: # reversed option for the last digit
        dict = {key[::-1]:value for key, value in dict.items()}    # invert the number mapping dictionary's keys
        text = text[::-1]    # inver the text
    spelled_out_number = ""
    for n, char in enumerate(text):
        if char.isdigit():
            return char
        elif char.isalpha():
            for subchar in text[n:]:
                if subchar.isalpha():
                    spelled_out_number += subchar
                if spelled_out_number in dict.keys():
                    return dict[spelled_out_number]
            spelled_out_number = ""

def sum_calibration_values(filepath):
    with open(filepath) as f:
        text = f.read()
        textlines = text.split('\n')
        for n, line in enumerate(textlines):
            num_first = extract_num(line)
            num_last = extract_num(line, reverse=True)
            textlines[n] = int(num_first + num_last)
        return sum(textlines)

print(sum_calibration_values(file_path))