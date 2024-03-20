from termcolor import colored
import json
from collections import Counter
import random 

my_file = open ('dictionary.json','r')
my_dict = json.load(my_file)
my_words = list(my_dict.keys())
my_words = [x.lower() for x in my_words if len(x)==5 and x.isalpha()]
my_definitions = list(my_dict.values())
my_def_words = []
for my_defs in my_definitions:
    my_defs= my_defs.strip()
    my_defs= my_defs.split()
    my_defs = [x.lower() for x in my_defs if len(x)==5 and x.isalpha()]
    my_def_words.append(my_defs)
my_def_words = [word for mini_list in my_def_words for word in mini_list]
my_occurances = dict(Counter(my_def_words))
my_nums = list(my_occurances.values())
my_nums.sort()
wordle_words = [x for x in my_occurances if my_occurances[x]>=my_nums[85*len(my_nums)//100]]
allowable_words= list(set(my_def_words).union(set(my_words)))
# End section for setting wordle_words and allowable_words variables

def letter_color(wordle_word,my_guessing_word):
    #Returns a word with the proper coloring for the most recent guess
    word_colored = ['grey','grey','grey','grey','grey']
    checked_letters=[]
    for count in range(0,len(word_colored)):
        if my_guessing_word[count]==wordle_word[count]: #Checks if letter is correct and in right place and changes to green
            word_colored[count]='green'
            checked_letters.append(my_guessing_word[count])
        elif my_guessing_word[count] in wordle_word and my_guessing_word[count]!=wordle_word[count]:    # checks if each letter is in the wordle_word but not in the right place, and changes to yellow.
            word_colored[count]='yellow'
    for count in range(0,len(word_colored)): #This turns a letter back to grey if the letter has already been turned green somewhere in the word. Also keeps a letter yellow if there's more than one of the letter chosen in the wordle_word and one should be green while the other should be yellow.
        if word_colored[count]=='yellow' and my_guessing_word[count] in checked_letters and wordle_word.count(my_guessing_word[count])==1:
            word_colored[count]='grey'   
    return word_colored

def show_alphabet(wordle_word,my_guessing_word,alphabet_color): 
    #This is a program for returning an array of 26 colors that can be applied to an alphabet and printed out
    alphabet= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    wordle_word=wordle_word.upper()
    my_guessing_word = my_guessing_word.upper()
    for count in range(0,len(wordle_word)):
        if alphabet_color[alphabet.index(my_guessing_word[count])]=='green': #This leaves the [count] letter of the alphabet alone if it is already green and keeps it green
            continue
        if my_guessing_word[count]==wordle_word[count]:
            alphabet_color[alphabet.index(my_guessing_word[count])]='green'
        elif my_guessing_word[count] in wordle_word and my_guessing_word[count]!=wordle_word[count]:
            alphabet_color[alphabet.index(my_guessing_word[count])]='yellow'
        elif my_guessing_word[count] not in wordle_word:
            alphabet_color[alphabet.index(my_guessing_word[count])]='grey'
    return alphabet_color


game_finished = False
the_wordle=random.choice(wordle_words)
tries=0
alphabet_colors=[]
alphabet= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
for l in alphabet:
    alphabet_colors.append('white')

while game_finished == False:
    my_guessing_word = input('Please input your word, or input "q" to quit: ')
    alphabet= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if my_guessing_word =='q':
        print('Thanks for playing!')
        game_finished = True
    else:
        if tries>=5 and my_guessing_word!=the_wordle:
            print('That was too many attempts, try again tomorrow.')
            game_finished=True
        if my_guessing_word==the_wordle:
            print('You have won!')
            game_finished=True
        if my_guessing_word in allowable_words:
            new_colors=letter_color(the_wordle,my_guessing_word)
            alphabet_colors=show_alphabet(the_wordle,my_guessing_word,alphabet_colors)
            tries+=1
            for count in range(0,len(my_guessing_word)): #Prints the guessed word
                print(colored(my_guessing_word[count].upper(),new_colors[count]),end='')
            print()
            for count in range(0,len(alphabet)): #prints the alphabet
                print(colored(alphabet[count].upper(),alphabet_colors[count]),end=' ')
        else:
            print('you entered an incorrect word')
