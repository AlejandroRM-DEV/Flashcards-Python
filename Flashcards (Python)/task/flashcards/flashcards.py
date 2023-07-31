import json
import random
import sys
from pathlib import Path
from io import StringIO


class Logger:
    def __init__(self):
        self.log_file = None
        self.stdout = sys.stdout
        self.stdin = sys.stdin
        self.output_buffer = StringIO()
        self.input_buffer = StringIO()

    def write(self, message):
        self.output_buffer.write(message + "\n")
        self.stdout.write(message + "\n")

    def readline(self):
        user_input = self.stdin.readline().strip()
        self.input_buffer.write(user_input)
        return user_input

    def save_log(self, file_name):
        with open(file_name, "a") as log_file:
            log_file.write(self.output_buffer.getvalue())
            log_file.write(self.input_buffer.getvalue())


class Flashcards:
    def __init__(self):
        self.cards = []
        self.logger = Logger()

    def search(self, key, value):
        for card in self.cards:
            if card[key] == value:
                return card

        return None

    def add(self):
        self.logger.write("The term for card:")
        term = self.logger.readline()
        while self.search("term", term):
            self.logger.write(f"The term \"{term}\" already exists. Try again:")
            term = self.logger.readline()

        self.logger.write("The definition for card:")
        definition = self.logger.readline()
        while self.search("definition", definition):
            self.logger.write(f"The definition \"{definition}\" already exists. Try again:")
            definition = self.logger.readline()

        self.cards.append({"term": term, "definition": definition, "mistakes": 0})
        self.logger.write(f"The pair ({term}:{definition}) has been added.")

    def remove(self):
        self.logger.write("Which card?")
        term = self.logger.readline()
        card = self.search("term", term)
        if card:
            self.cards.remove(card)
            self.logger.write("The card has been removed.")
        else:
            self.logger.write(f"Can't remove {term}: there is no such card.")

    def ask(self):
        self.logger.write("How many times to ask?")
        number_of_cards = int(self.logger.readline())
        for card in random.choices(self.cards, k=number_of_cards):
            self.logger.write(f"Print the definition of \"{card['term']}\":")
            answer = self.logger.readline()
            card_found = self.search("definition", answer)

            if not card_found:
                self.logger.write(f"Wrong. The right answer is {card['definition']}.")
                card['mistakes'] = card['mistakes'] + 1
            elif card["term"] == card_found["term"]:
                self.logger.write("Correct!")
            else:
                self.logger.write(f"Wrong. The right answer is {card['definition']}, "
                                  f"but your definition is correct for {card_found['term']}")
                card['mistakes'] = card['mistakes'] + 1

    def export(self):
        self.logger.write("File name:")
        filename = self.logger.readline()
        with open(Path(filename), "w") as file:
            file.write(json.dumps(self.cards))
            self.logger.write(f"{len(self.cards)} cards have been saved")

    def import_cards(self):
        try:
            self.logger.write("File name:")
            filename = self.logger.readline()
            with open(Path(filename), "r") as file:
                data = file.read()
                self.cards = json.loads(data)
                self.logger.write(f"{len(self.cards)} cards have been loaded")
        except:
            self.logger.write("File not found.")

    def log(self):
        self.logger.write("File name:")
        filename = self.logger.readline()
        self.logger.save_log(filename)
        print("The log has been saved.")

    def hardest(self):
        highest = 0
        for card in self.cards:
            if card["mistakes"] > highest:
                highest = card["mistakes"]

        if highest == 0:
            self.logger.write("There are no cards with errors.")
            return

        highest_cards = list(filter(lambda card: card["mistakes"] == highest, self.cards))
        if len(highest_cards) == 1:
            self.logger.write(f"The hardest card is {highest_cards[0]['term']}. "
                              f"You have {highest} errors answering it")
        else:
            self.logger.write(f"The hardest card is {','.join([c['term'] for c in highest_cards ])}. "
                  f"You have {highest} errors answering it")


    def reset(self):
        for card in self.cards:
            card["mistakes"] = 0
        self.logger.write("Card statistics have been reset.")

    def run(self):
        run = True
        while run:
            self.logger.write("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
            action = self.logger.readline()
            print(action)
            if action == "add":
                self.add()
            elif action == "remove":
                self.remove()
            elif action == "import":
                self.import_cards()
            elif action == "export":
                self.export()
            elif action == "ask":
                self.ask()
            elif action == "log":
                self.log()
            elif action == "hardest card":
                self.hardest()
            elif action == "reset stats":
                self.reset()
            elif action == "exit":
                self.logger.write("bye bye")
                run = False


if __name__ == "__main__":
    flashcards = Flashcards()
    flashcards.run()


