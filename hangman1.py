import random
import os

# Hangman art for each stage of the game
hangman_art = [r'''
       +---+
           |
           |
           |
          ===''', r'''
       +---+
       O   |
           |
           |
          ===''', r'''
       +---+
       O   |
       |   |
           |
          ===''', r'''
       +---+
       O   |
      /|   |
           |
          ===''', r'''
       +---+
       O   |
      /|\  |
           |
          ===''', r'''
       +---+
       O   |
      /|\  |
      /    |
          ===''', r'''
       +---+
       O   |
      /|\  |
      / \  |
          ===''']

# ASCII art for the intro screen
intro_art = '''
  _   _                                         
 | | | |                                        
 | |_| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  _  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | | | | (_| | | | | (_| | | | | | | (_| | | | |
 \_| |_/\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_| 
                     __/ |                       
                    |___/                        
'''

# Welcome message displayed at the start of the game
welcome_message = '''
                 Welcome to the game
                    HANGMAN MAN!
Try to guess the word and avoid becoming a hanged man!
'''

# Function to display the intro screen and welcome message
def display_intro():
    print(intro_art)
    print(welcome_message)

# Function to dynamically scale hangman art based on remaining lives
def get_hangman_art(lives, max_lives):
    stage = int((len(hangman_art) - 1) * (1 - (lives / max_lives)))
    return hangman_art[stage]

# Function to display the current hint (correct guesses so far)
def display_hint(hint):
    print(" ".join(hint))

# Function to display the correct answer
def display_answer(answer):
    print(" ".join(answer))

# Load words from file
def load_words(file_path):
    if not os.path.isfile(file_path):
        print(f"File {file_path} not found.")
        exit()
    try:
        with open(file_path, "r") as file:
            words = [line.strip() for line in file if line.strip()]
            if not words:
                print("No valid words found in the file.")
                exit()
            return words
    except Exception as e:
        print(f"Error reading file: {e}")
        exit()

# Function to handle level selection
def select_difficulty():
    while True:
        difficulty = input("Choose difficulty (easy, medium, hard): ").lower()
        if difficulty == "easy":
            return 7
        elif difficulty == "medium":
            return 5
        elif difficulty == "hard":
            return 3
        else:
            print("Invalid input. Please choose again.")

# Main game function
def main():
    display_intro()

    # Load words from file
    words = load_words("countries-and-capitals.txt")

    # Choose difficulty level
    lives = select_difficulty()
    max_lives = lives  # Store max lives for art scaling

    # Choose a random word for the player to guess
    answer = random.choice(words)  # Example: "Zambia | Lusaka"

    # Initialize hint: underscores for letters, keep spaces and special characters
    hint = ["_" if char.isalpha() else char for char in answer]

    wrong_guesses = 0
    guessed_letters = set()
    wrong_letters = []

    while True:
        print(f"Lives remaining: {lives - wrong_guesses}")
        print(get_hangman_art(lives - wrong_guesses, max_lives))  # Dynamic ASCII art
        display_hint(hint)  # Display the hint with correct spacing and symbols
        print("Wrong letters:", ", ".join(sorted(wrong_letters)))
        guess = input("Enter a letter (or type 'quit' to exit): ").lower()

        # Check if the user wants to quit
        if guess == "quit":
            print("Goodbye!")
            break

        # Validate input: ensure it's a single letter
        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue

        # Check if the letter was already guessed
        if guess in guessed_letters:
            print(f"You already guessed '{guess}'. Try a different letter.")
            continue

        guessed_letters.add(guess)

        # Check if the guessed letter is in the answer
        if guess in answer.lower():  # Match ignoring case
            # Reveal all occurrences of the letter in the hint
            for i, char in enumerate(answer):
                if char.lower() == guess:
                    hint[i] = char  # Keep original case from the answer
        else:
            if guess not in wrong_letters:
                wrong_guesses += 1
                wrong_letters.append(guess)

        # Ensure wrong guesses don't exceed available lives
        if wrong_guesses >= lives:
            print(get_hangman_art(0, max_lives))  # Final ASCII art
            print("Correct answer was:")
            display_answer(answer)  # Show answer with spaces
            print("YOU LOSE!")
            break

        # Check if the player has guessed the entire word
        if "_" not in hint:
            print(get_hangman_art(lives - wrong_guesses, max_lives))
            display_answer(answer)  # Show answer with spaces
            print("YOU WIN!")
            print(f"You guessed the word in {len(guessed_letters)} attempts!")
            break

# Entry point of the script
if __name__ == "__main__":
    main()
