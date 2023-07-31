print("Input the number of cards:")
number_of_cards = int(input())
cards = []
for n in range(1, number_of_cards + 1):
    print(f"The term for card #{n}:")
    term = input()
    print(f"The definition for card #{n}:")
    definition = input()
    cards.append({"term": term, "definition": definition})

for card in cards:
    print(f"Print the definition of \"{card['term']}\":")
    answer = input()
    if answer == card["definition"]:
        print("Correct!")
    else:
        print(f"Wrong. The right answer is {card['definition']}.")
