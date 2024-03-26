def create_staircase(words):
    step = 1
    subsets = []
    while len(words) != 0:
        if len(words) >= step:
            subsets.append(words[0:step])
            words = words[step:]
            step += 1
        else:
            return False
    return subsets

def decode(message_file):
    file_dict = {}
    with open(message_file, 'r') as file:
        for i in file.readlines():
            number, word = i.strip().split()
            file_dict[int(number)] = word
    file_dict = dict(sorted(file_dict.items()))
    pyramid = create_staircase(list(file_dict.values()))
    message = [line[-1] for line in pyramid]
    decoded_mesage = ' '.join(message)
    return decoded_mesage

print(decode("coding_qual_input.txt"))
print()