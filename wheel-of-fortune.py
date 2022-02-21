import time
import requests
from humanfriendly import format_timespan

# Call the Generator Fun API, which returns a cliche/phrase
response = requests.request("GET", "https://generatorfun.com/consumeapi.php?api=2337")

# Remove double quotes and extraneous space character, then convert phrase to all caps
phrase = response.text.replace("\"", "")
phrase = phrase.rstrip()
phrase = phrase.upper()

# Create a string that will store the unsolved version of phrase
blanks = ""

# Iterate through each character in phrase (including spaces)
for character in phrase:

    # If character is a space, insert space character in string
    if character.isspace() is True:
        blanks += " "

    # If character is a special character, insert special character in string
    elif character in "~`!@#$%^&*()-+={}[]:;'|\/?<>,.":
        blanks += character

    # If character is a letter, insert underscore in string
    else:
        blanks += "_"

# Create a list for the solved phrase and unsolved phrase (so they will be mutable)
solved_phrase = list(phrase)
unsolved_phrase = list(blanks)

# Temporarily format the unsolved phrase as a string, so it can be printed neatly
unsolved_phrase_string = "".join(unsolved_phrase)

print("Here is your phrase...")
print(unsolved_phrase_string)

# Create a list that will store every letter the player guesses
guessed_letters = []

# Start a timer
start_time = time.time()

# Define a function that calculates how long the player takes to solve the phrase
def elapsed_time(start_time):

    # Calculate elapsed time by subtracting start time from current time, rounding to the nearest second
    elapsed_time = round(time.time() - start_time)
    print("Nice! You solved this phrase in " + format_timespan(elapsed_time) + ".")

# While there are still missing characters in the phrase...
while "_" in unsolved_phrase:

    # Prompt the player to enter a letter or solve the phrase
    guessed_letter = input("Enter a letter, or type SOLVE to solve the phrase...\n")

    # If the player enters a non-letter, multiple characters, a letter they've already entered,
    # or if they want to solve the phrase...
    while guessed_letter.isalpha() is False \
            or len(guessed_letter) > 1 \
            or guessed_letter.upper() in guessed_letters \
            or guessed_letter.upper() == "SOLVE":

        # If the player wants to solve the phrase...
        if guessed_letter.upper() == "SOLVE":
            solve_attempt = input("Go ahead and solve the phrase...\n")

            # If the player solves the phrase...
            if solve_attempt.upper() == phrase.upper():

                # Call the elapsed_time function
                elapsed_time(start_time)
                quit()

            # If the player doesn't solve the phrase...
            else:
                print("That is not the correct answer.")
                break

        # If the player enters a non-letter...
        if guessed_letter.isalpha() is False:
            guessed_letter = input("You must enter a letter from the alphabet. Try again...\n")

        # If the player enters multiple characters...
        if len(guessed_letter) > 1:
            guessed_letter = input("You must enter a single character. Try again...\n")

        # If the player enters a letter they've already entered...
        if guessed_letter.upper() in guessed_letters:
            guessed_letter = input("You've already entered that letter. Try another letter...\n")

    # Add the player's guessed letter to the list of guessed letters
    guessed_letters.append(guessed_letter.upper())

    # Iterate through each index/letter in the solved phrase
    for index, solved_letter in enumerate(solved_phrase):

        # If the player's guessed letter matches the current letter...
        if guessed_letter.upper() == solved_letter.upper():

            # Add the letter to the corresponding index in the unsolved phrase
            unsolved_phrase[index] = solved_letter

    # Skip the following if statement if the player just made a failed attempt at solving the phrase
    if guessed_letter.upper() != "SOLVE":

        # If the player's guessed letter is not in the phrase
        if guessed_letter.upper() not in solved_phrase:
            print("Unfortunately, " + guessed_letter.upper() + " is not in this phrase.")

        # If the player's guessed letter is in the phrase
        else:
            print("Well done! " + guessed_letter.upper() + " is in this phrase.")

    # Temporarily format the unsolved phrase as a string, so it can be printed neatly
    unsolved_phrase_string = "".join(unsolved_phrase)
    print(unsolved_phrase_string)

# Call the elapsed_time function
elapsed_time(start_time)