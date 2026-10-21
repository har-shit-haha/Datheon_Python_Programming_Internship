import random
from pathlib import Path

MAX_ATTEMPTS = 6
WORD_LIST_FILE = Path(__file__).with_name("wordlist.txt")

HANGMAN_STAGES = [
    r"""
     +---+
     |   |
         |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
     |   |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|   |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
    /    |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
    / \  |
    =========
    """
]


def load_words():
    """Load alphabetic words from wordlist.txt beside this script."""
    try:
        with WORD_LIST_FILE.open("r", encoding="utf-8") as file:
            words = [
                line.strip().upper()
                for line in file
                if line.strip().isalpha() and len(line.strip()) >= 4
            ]
    except OSError:
        print("Could not find wordlist.txt.")
        print("Keep wordlist.txt in the same folder as hangman.py.")
        return []

    return words


def play_hangman():
    words = load_words()
    if not words:
        return

    secret_word = random.choice(words)
    guessed_letters = set()
    incorrect_guesses = 0

    print("=" * 35)
    print("       WELCOME TO HANGMAN")
    print("=" * 35)

    while incorrect_guesses < MAX_ATTEMPTS:
        print(HANGMAN_STAGES[incorrect_guesses])

        masked_word = " ".join(
            letter if letter in guessed_letters else "_"
            for letter in secret_word
        )
        print("Word:", masked_word)
        print(f"Attempts remaining: {MAX_ATTEMPTS - incorrect_guesses}")
        print(
            "Guessed letters:",
            " ".join(sorted(guessed_letters)) if guessed_letters else "None"
        )

        guess = input("Guess a letter: ").strip().upper()

        if len(guess) != 1 or not guess.isalpha() or not guess.isascii():
            print("Invalid input. Enter one English letter (A-Z).\\n")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter. No attempt is lost.\\n")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            print("Correct guess!\\n")
        else:
            incorrect_guesses += 1
            print("Incorrect guess!\\n")

        if all(letter in guessed_letters for letter in secret_word):
            print(HANGMAN_STAGES[incorrect_guesses])
            print("Word:", " ".join(secret_word))
            print("Congratulations! You guessed the word!")
            return

    print(HANGMAN_STAGES[MAX_ATTEMPTS])
    print("You lost!")
    print("The correct word was:", secret_word)


if __name__ == "__main__":
    play_hangman()
