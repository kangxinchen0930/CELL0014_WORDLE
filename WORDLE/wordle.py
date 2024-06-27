#pip3 install tabulate
#pip3 install colorama

import random
import time
import datetime
from tabulate import tabulate
from colorama import Fore, Style, init

init()

def print_menu():
    print('WELCOME TO WORDLE!\n')
    print('You have 6 chances to guess a 5-letter word.')

def load_word_set(wordlength):
    word_set = []
    # from dict.txt load words and append into word_set
    with open('dict.txt') as f:
        words = f.read().splitlines()  # split dict.txt into list of words
        for word in words:
            if len(word) == wordlength:  # append those words with the desired wordlength into word_set
                word_set.append(word)
    return word_set

def get_valid_attempts(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 1 or value > 6:
                raise ValueError  # this will send it to the print message and back to the input option
            break
        except ValueError:
            print(Fore.RED + 'Sorry, please type in a valid number from 1 to 6.' + Style.RESET_ALL)
            continue
    return value

def get_valid_wordlength(prompt):
    while True:
        try:
            value = int(input(prompt))
            check_word_in_word_set = load_word_set(value)
            if len(check_word_in_word_set) == 0:
                raise ValueError  # this will send it to the print message and back to the input option
            break
        except ValueError:
            print(Fore.RED + 'Oops! There is no word with this length. Please try again.' + Style.RESET_ALL)
            continue
    return value

def get_frequency_dict(randomword: str):
    # function to find the frequency of characters in the word using a dict
    result = {}  # creating an empty dictionary
    for i in range(len(randomword)):
        c = randomword[i]  # c = character of randomword
        if c in result:  # Count the characters in the dict
            result[c] += 1
        else:
            result[c] = 1
    return result

def play_wordle(guess: str, randomword: str, wordlength: int):
    # hints to get closer to the randomword
    frequency_map = get_frequency_dict(randomword)
    for c in range(wordlength):
        # guess = user's guess
        # randomword = secret word
        # c = character
        if guess[c] == randomword[c]:  # for correct character and position
            print(Fore.GREEN + f'{guess[c]}- in word and in correct spot' + Style.RESET_ALL)
            frequency_map[guess[c]] = frequency_map[guess[c]] - 1
        elif (guess[c] in randomword) and (frequency_map[guess[c]] > 0):  # for correct character but wrong position
            print(Fore.YELLOW + f'{guess[c]}- in word but in wrong spot' + Style.RESET_ALL)
            frequency_map[guess[c]] = frequency_map[guess[c]] - 1
        else:  # for incorrect character
            print(Fore.RED + f'{guess[c]}- not in word' + Style.RESET_ALL)

def print_statistics(total_num_games, won_num_games, current_streak, max_streak):
    print(f'Played: {total_num_games}')
    print(f'Won%: {(won_num_games / total_num_games) * 100:.2f}')
    print(f'Current streak: {current_streak}')
    print(f'Maximum streak: {max_streak}')
    print('-------- Guess distribution -------')
    data = [["Attempts used", "Games won"],
            ["1", guess_distribution[0]],
            ["2", guess_distribution[1]],
            ["3", guess_distribution[2]],
            ["4", guess_distribution[3]],
            ["5", guess_distribution[4]],
            ["6", guess_distribution[5]]]
    print(tabulate(data, tablefmt='plain'))
    print('-----------------------------------')

def time_until_tomorrow():
    now = datetime.datetime.now()
    midnight = datetime.datetime.combine(now.date() + datetime.timedelta(days=1), datetime.time())  # code for midnight (00:00:00)
    return (midnight - now).seconds

def countdown(t):
    while t:  # loop runs until time becomes 0.
        # divmod() to calculate the number of hours, minutes and seconds.
        mins, secs = divmod(t, 60)
        hours, mins = divmod(mins, 60)
        timer = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)

        #print(timer, end='\r')  # force the cursor to go back to the start
        print('\r', timer, end='')

        time.sleep(1)  # reduce time by 1
        t -= 1

    print('\nA new word is available!\n')
    print('-----------------------------------')


total_num_games = 0
won_num_games = 0
current_streak = 0
max_streak = 0
guess_distribution = [0, 0, 0, 0, 0, 0]

while True:

    attempts = 6  # default number of attempts
    wordlength = 5  # default wordlength for wordle

    print_menu()

    control = input('Would you like to adjust the game difficulty? (y/[n]) \n')

    # allow user to adjust the number of guesses and wordlength
    if control.lower().startswith("y"):
        attempts = get_valid_attempts('Choose the number of attempts from 1 to 6.\n')
        print(f'Your choice: {attempts}')

        wordlength = get_valid_wordlength('Choose the length of your WORDLE.\n')
        print(f'Your choice: {wordlength}')

    # load word_set with selected wordlength
    word_set = load_word_set(wordlength)

    # one random word per calendar day
    random.seed(datetime.date.today().toordinal())
    randomword = random.choice(word_set)
    # randomword = secret word/wordle

    i_attempts = attempts  # store initial attempts
    while attempts > 0:

        guess = input(f'Attempt {attempts}- Type your guess.\n').upper()  # user's guess

        # ask user to input the guess again if they input a word that exceeds wordlength or does not exist
        if len(guess) != wordlength:
            print(Fore.RED + f'Word must be {wordlength} characters long.' + Style.RESET_ALL)
            continue

        if guess not in word_set:
            print(Fore.RED + 'Not in word list, please type in a valid word.' + Style.RESET_ALL)
            continue

        print('-----------------------------------')
        # play_wordle function to tell the user how close they are to winning the game
        play_wordle(guess, randomword, wordlength)
        print('-----------------------------------')

        # if user guesses the word and wins the game
        if guess == randomword:
            print("\nYou won!\n")

            n_guesses = i_attempts - attempts + 1  # attempts/guesses used by user
            print(f'You used up {n_guesses} guesses.\n')

            # print game statistics
            print('----Your game statistics are:----')
            total_num_games += 1
            won_num_games += 1  # update the winning games
            current_streak += 1
            if current_streak > max_streak:  # if the current streak is larger than maximum streak
                max_streak = current_streak  # update the maximum streak
            guess_distribution[n_guesses - 1] += 1  # add in to guess distribution

            print_statistics(total_num_games, won_num_games, current_streak, max_streak)

            # tell the user when will the next word be generated
            print('\nThe time left until your next Wordle:')
            countdown(time_until_tomorrow())
            break

        elif guess != randomword and attempts > 1:
            attempts -= 1
            print(f'\nTry again, You have {attempts} guesses left...\n')
            continue

        elif attempts == 1:
            attempts -= 1
            print(f'\nYou used up all your attempts. You lost. The correct word is {randomword}.\n')

            # print game statistics
            print('----Your game statistics are:----')
            total_num_games += 1
            current_streak = 0  # return the streak to 0

            print_statistics(total_num_games, won_num_games, current_streak, max_streak)

            # tell the user when will the next word be generated
            print('\nThe time left until your next Wordle is:')
            countdown(